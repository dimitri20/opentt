from typing import Dict, List, Tuple, Optional, Callable
from ortools.sat.python import cp_model
from dataclasses import dataclass
import time

from app.solver.data_loader import InstitutionData, ActivityData


@dataclass
class SolverResult:
    status: str  # "OPTIMAL", "FEASIBLE", "INFEASIBLE", "UNKNOWN"
    assignments: List[Dict]
    objective_value: float
    solve_time: float
    statistics: Dict


class TimetableSolver:
    """Timetable solver using Google OR-Tools CP-SAT"""
    
    def __init__(self, data: InstitutionData):
        self.data = data
        self.model = cp_model.CpModel()
        self.variables: Dict[Tuple[int, int, int, int], cp_model.IntVar] = {}
        self.soft_penalties = []
        
    def build_model(self):
        """Build the CP-SAT model"""
        print("🔧 Building CP-SAT model...")
        self._create_variables()
        self._add_hard_constraints()
        self._add_soft_constraints()
        self._set_objective()
        print(f"✅ Model built: {len(self.variables)} variables")
        
    def _create_variables(self):
        """Create decision variables for each (activity, day, period, room) combination"""
        for activity in self.data.activities:
            for day in self.data.days:
                for period in self.data.periods:
                    for room in self.data.rooms:
                        var_name = f"x_a{activity.id}_d{day.id}_p{period.id}_r{room.id}"
                        var = self.model.NewBoolVar(var_name)
                        self.variables[(activity.id, day.id, period.id, room.id)] = var
    
    def _add_hard_constraints(self):
        """Add hard constraints that must be satisfied"""
        print("🔒 Adding hard constraints...")
        
        # 1. Each activity must be assigned exactly once
        for activity in self.data.activities:
            slots = [
                self.variables[(activity.id, day.id, period.id, room.id)]
                for day in self.data.days
                for period in self.data.periods
                for room in self.data.rooms
            ]
            self.model.Add(sum(slots) == 1)
        
        # 2. Teacher conflicts: A teacher can't teach two activities at the same time
        for teacher in self.data.teachers:
            teacher_activities = [a for a in self.data.activities if teacher.id in a.teacher_ids]
            for day in self.data.days:
                for period in self.data.periods:
                    slots = [
                        self.variables[(activity.id, day.id, period.id, room.id)]
                        for activity in teacher_activities
                        for room in self.data.rooms
                    ]
                    if slots:
                        self.model.Add(sum(slots) <= 1)
        
        # 3. Student group conflicts: A group can't attend two activities at the same time
        for group in self.data.student_groups:
            group_activities = [a for a in self.data.activities if group.id in a.group_ids]
            for day in self.data.days:
                for period in self.data.periods:
                    slots = [
                        self.variables[(activity.id, day.id, period.id, room.id)]
                        for activity in group_activities
                        for room in self.data.rooms
                    ]
                    if slots:
                        self.model.Add(sum(slots) <= 1)
        
        # 4. Room conflicts: A room can only host one activity at a time
        for room in self.data.rooms:
            for day in self.data.days:
                for period in self.data.periods:
                    slots = [
                        self.variables[(activity.id, day.id, period.id, room.id)]
                        for activity in self.data.activities
                    ]
                    self.model.Add(sum(slots) <= 1)
        
        # 5. Room capacity constraints
        for activity in self.data.activities:
            if activity.total_student_count > 0:
                for day in self.data.days:
                    for period in self.data.periods:
                        for room in self.data.rooms:
                            if room.capacity < activity.total_student_count:
                                # Can't assign this activity to this room
                                self.model.Add(
                                    self.variables[(activity.id, day.id, period.id, room.id)] == 0
                                )
        
        # 6. Teacher not available constraints
        for constraint in self.data.constraints.teacher_not_available:
            teacher_activities = [
                a for a in self.data.activities 
                if constraint.teacher_id in a.teacher_ids
            ]
            for activity in teacher_activities:
                for room in self.data.rooms:
                    self.model.Add(
                        self.variables[(activity.id, constraint.day_id, constraint.period_id, room.id)] == 0
                    )
        
        # 7. Room not available constraints
        for constraint in self.data.constraints.room_not_available:
            for activity in self.data.activities:
                self.model.Add(
                    self.variables[(activity.id, constraint.day_id, constraint.period_id, constraint.room_id)] == 0
                )
        
        print("✅ Hard constraints added")
    
    def _add_soft_constraints(self):
        """Add soft constraints (preferences) that are weighted in the objective"""
        print("🎯 Adding soft constraints...")
        
        # Teacher max hours per day (soft constraint with penalty)
        for constraint in self.data.constraints.teacher_max_hours_daily:
            teacher_activities = [
                a for a in self.data.activities 
                if constraint.teacher_id in a.teacher_ids
            ]
            
            for day in self.data.days:
                # Count hours this teacher works on this day
                hours_vars = [
                    self.variables[(activity.id, day.id, period.id, room.id)]
                    for activity in teacher_activities
                    for period in self.data.periods
                    for room in self.data.rooms
                ]
                
                if hours_vars:
                    # Create a penalty variable if hours exceed max
                    overflow = self.model.NewIntVar(0, len(self.data.periods), f"overflow_t{constraint.teacher_id}_d{day.id}")
                    self.model.Add(sum(hours_vars) - constraint.max_hours <= overflow)
                    
                    # Add weighted penalty to objective
                    penalty = self.model.NewIntVar(0, constraint.weight * len(self.data.periods), f"penalty_t{constraint.teacher_id}_d{day.id}")
                    self.model.Add(penalty == overflow * constraint.weight)
                    self.soft_penalties.append(penalty)
        
        print(f"✅ Soft constraints added: {len(self.soft_penalties)} penalty variables")
    
    def _set_objective(self):
        """Set the objective function to minimize penalties"""
        if self.soft_penalties:
            self.model.Minimize(sum(self.soft_penalties))
            print("🎯 Objective: Minimize total penalty")
        else:
            print("ℹ️  No soft constraints, finding any feasible solution")
    
    def solve(
        self, 
        time_limit_seconds: int = 300,
        progress_callback: Optional[Callable[[int, float, str], None]] = None
    ) -> SolverResult:
        """Solve the timetable problem"""
        print(f"🚀 Starting solver (time limit: {time_limit_seconds}s)...")
        
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = time_limit_seconds
        solver.parameters.num_search_workers = 8
        solver.parameters.log_search_progress = True
        
        # Add solution callback if provided
        if progress_callback:
            callback = SolutionCallback(progress_callback)
            status = solver.Solve(self.model, callback)
        else:
            status = solver.Solve(self.model)
        
        solve_time = solver.WallTime()
        
        # Map status to string
        status_map = {
            cp_model.OPTIMAL: "OPTIMAL",
            cp_model.FEASIBLE: "FEASIBLE",
            cp_model.INFEASIBLE: "INFEASIBLE",
            cp_model.MODEL_INVALID: "MODEL_INVALID",
            cp_model.UNKNOWN: "UNKNOWN",
        }
        status_str = status_map.get(status, "UNKNOWN")
        
        print(f"✅ Solver finished: {status_str} in {solve_time:.2f}s")
        
        # Extract solution if found
        assignments = []
        if status in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            assignments = self._extract_solution(solver)
        
        # Get statistics
        statistics = {
            "status": status_str,
            "branches": solver.NumBranches(),
            "conflicts": solver.NumConflicts(),
            "wall_time": solve_time,
            "best_bound": solver.BestObjectiveBound() if self.soft_penalties else 0,
        }
        
        return SolverResult(
            status=status_str,
            assignments=assignments,
            objective_value=solver.ObjectiveValue() if status in (cp_model.OPTIMAL, cp_model.FEASIBLE) else 0,
            solve_time=solve_time,
            statistics=statistics,
        )
    
    def _extract_solution(self, solver: cp_model.CpSolver) -> List[Dict]:
        """Extract the solution from the solver"""
        assignments = []
        
        for activity in self.data.activities:
            for day in self.data.days:
                for period in self.data.periods:
                    for room in self.data.rooms:
                        var = self.variables[(activity.id, day.id, period.id, room.id)]
                        if solver.Value(var) == 1:
                            assignments.append({
                                "activity_id": activity.id,
                                "activity_name": activity.name,
                                "day_id": day.id,
                                "day_name": day.name,
                                "period_id": period.id,
                                "period_name": period.name,
                                "room_id": room.id,
                                "room_name": room.name,
                            })
        
        print(f"📋 Solution: {len(assignments)} activity assignments")
        return assignments


class SolutionCallback(cp_model.CpSolverSolutionCallback):
    """Callback to report progress during solving"""
    
    def __init__(self, progress_fn: Callable[[int, float, str], None]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.progress_fn = progress_fn
        self.solution_count = 0
        self.start_time = time.time()
    
    def on_solution_callback(self):
        """Called every time a new solution is found"""
        self.solution_count += 1
        elapsed = time.time() - self.start_time
        objective = self.ObjectiveValue()
        
        message = f"Solution #{self.solution_count} found (objective: {objective})"
        self.progress_fn(self.solution_count, elapsed, message)
