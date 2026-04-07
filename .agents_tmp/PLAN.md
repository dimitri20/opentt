# 1. OBJECTIVE

Build **OpenTT** - a complete open-source timetable management system for schools and universities. The system will use Google OR-Tools CP-SAT solver to automatically generate conflict-free schedules based on institution constraints. The goal is to create a production-ready, full-stack web application with comprehensive CRUD operations, a sophisticated constraint solver, real-time progress tracking, and an intuitive user interface for managing and viewing timetables.

# 2. CONTEXT SUMMARY

## Technology Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic (migrations), Celery (async tasks), Redis (task queue & pub/sub)
- **Database**: PostgreSQL 16
- **Solver**: Google OR-Tools CP-SAT (constraint programming solver)
- **Frontend**: React 18, TypeScript, Vite, TanStack Query, React Router v6, shadcn/ui, Tailwind CSS
- **Infrastructure**: Docker Compose with 5 services (api, worker, db, redis, frontend/nginx)
- **Testing**: pytest (backend unit/integration), Playwright (E2E)

## System Architecture
- **API Layer**: RESTful endpoints for all resources (institutions, teachers, rooms, activities, constraints)
- **Worker Layer**: Celery workers process long-running solver jobs asynchronously
- **Solver Layer**: Builds CP-SAT model from database constraints, solves with time limits, publishes progress
- **Frontend Layer**: SPA with TanStack Query for server state, React Router for navigation, shadcn/ui components

## Data Model Overview
The system manages 20+ interconnected tables:
- **Institution setup**: institutions, days_of_week, periods, academic_years
- **Resources**: buildings, rooms, subjects, teachers
- **Students**: student_years → groups → subgroups (3-level hierarchy)
- **Activities**: activities with many-to-many relationships to teachers, groups, subgroups, rooms, tags
- **Constraints**: 17+ constraint types (teacher availability, max hours, gaps, preferred times, room availability, etc.)
- **Solver jobs**: solve_jobs table stores job status, solution JSON, and statistics

## Key Constraints
- **Hard constraints** (must be satisfied): no teacher/student/room conflicts, availability restrictions, room capacity
- **Soft constraints** (weighted penalties): preferred times, max hours/gaps, room preferences, activity ordering

## Dependencies
- OR-Tools solver requires proper modeling of boolean variables (activity × day × period × room)
- Celery requires Redis for broker and result backend
- Frontend requires API to be running and accessible
- Docker Compose orchestrates all services with proper networking and health checks

## Starting Point
The workspace is currently empty. The project will be built from scratch in the `./opentt/` directory with the following structure:
```
opentt/
├── backend/
│   ├── app/
│   │   ├── api/routes/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── solver/
│   │   └── services/
│   ├── tests/
│   ├── alembic/
│   ├── main.py
│   └── celery_app.py
├── frontend/
│   └── src/
├── docker-compose.yml
└── README.md
```

# 3. APPROACH OVERVIEW

The implementation will follow a **bottom-up, incremental approach** that builds foundational layers first, then adds complexity progressively. This approach minimizes rework and allows for early validation of core functionality.

## Implementation Strategy

### Phase 1: Foundation (Database & API Infrastructure)
Build the complete data model and basic API infrastructure before any solver work. This allows frontend development to start in parallel with solver implementation.

**Rationale**: The database schema is the contract between all layers. Getting it right early prevents costly refactoring later.

### Phase 2: Core API Layer (CRUD Operations)
Implement all CRUD endpoints for resources before tackling the solver. This ensures data can be entered, retrieved, and validated independently of solving.

**Rationale**: A working CRUD API enables UI development and testing with realistic data while solver work proceeds independently.

### Phase 3: Solver Implementation (Hard Constraints First)
Build the CP-SAT model incrementally:
1. Define variables (activity assignments)
2. Implement hard constraints (conflicts, availability)
3. Verify feasibility with small test dataset
4. Add soft constraints with weighted penalties
5. Implement progress tracking and job management

**Rationale**: Hard constraints must be satisfied for any valid solution. Proving the solver works with hard constraints first de-risks the project. Soft constraints can be added iteratively.

### Phase 4: Frontend (Data Entry → Visualization)
Build UI components in order of user workflow:
1. Institution setup (days, periods, rooms, teachers)
2. Activity management
3. Constraint configuration
4. Solve interface with progress tracking
5. Timetable visualization with multiple views

**Rationale**: Users must input data before they can solve or view results. Following the natural workflow ensures each component can be tested as it's built.

### Phase 5: Integration & Polish
1. Docker Compose orchestration
2. Export functionality (HTML, CSV)
3. WebSocket real-time updates
4. Comprehensive testing (unit, integration, E2E)
5. Documentation

**Rationale**: Integration issues are easier to debug once all components work independently.

## Key Technical Decisions

### OR-Tools Model Design
- Use **BoolVar for each possible assignment**: `x[activity, day, period, room]`
- Use **auxiliary variables for soft constraints**: gap counters, hour counters
- Store solution as **JSON array of assignments**: `[{activity_id, day_id, period_id, room_id}, ...]`
- Use **CpSolver.SolutionCallback** to publish progress every 5 seconds

### API Design Pattern
- **Resource-based routing**: `/institutions/{id}/{resource}/`
- **Nested relationships**: Groups belong to years, subgroups to groups
- **Pydantic v2 schemas**: Separate Create, Update, Read schemas per resource
- **SQLAlchemy 2.0 async**: Use async session for non-blocking I/O

### Async Job Management
- **Celery for solver jobs**: Long-running tasks handled by worker pool
- **Redis pub/sub for progress**: Solver publishes updates, frontend subscribes via WebSocket
- **Job status polling**: Frontend polls `/solve/{job_id}` for status updates
- **Graceful timeout**: Solver stops after time_limit_seconds, returns best solution found

### Frontend State Management
- **TanStack Query for server state**: Automatic caching, refetching, mutations
- **React Context for UI state**: Selected institution, view filters
- **Optimistic updates**: UI updates immediately, rolls back on error

## Alternative Approaches Considered

### Alternative 1: Top-Down (Solver First)
Build the solver with hardcoded data, then add database/API later.
- **Rejected**: Requires dummy data, hard to test realistically, difficult to parallelize work

### Alternative 2: Monolithic Implementation
Build everything at once, test at the end.
- **Rejected**: High risk of integration issues, no incremental validation, harder to debug

### Alternative 3: SQLAlchemy Sync API
Use synchronous SQLAlchemy instead of async.
- **Rejected**: FastAPI performs better with async I/O, especially under load

## Risk Mitigation

1. **Solver Complexity**: Start with minimal hard constraints, validate with tiny dataset (3 teachers, 10 activities), then add constraints incrementally
2. **Performance**: Set reasonable time limits (300s default), use multi-threading (`num_search_workers=cpu_count()`)
3. **Data Complexity**: Implement cascade deletes and foreign key constraints at database level to maintain referential integrity
4. **Frontend Complexity**: Use shadcn/ui components to avoid building UI from scratch, focus on business logic

# 4. IMPLEMENTATION STEPS

## Step 1: Project Initialization and Structure Setup

**Goal**: Create the project directory structure and initialize all configuration files.

**Method**:
1. Create `opentt/` directory at workspace root
2. Initialize backend Python project:
   - Create `backend/` with subdirectories: `app/`, `tests/`, `alembic/`
   - Create `app/` subdirectories: `api/routes/`, `core/`, `models/`, `schemas/`, `services/`, `solver/`
   - Create `backend/requirements.txt` with all dependencies:
     - `fastapi`, `uvicorn[standard]`, `sqlalchemy[asyncio]`, `alembic`, `psycopg[binary]`
     - `pydantic>=2.0`, `pydantic-settings`, `celery`, `redis`, `ortools`
     - `python-jose[cryptography]`, `passlib[bcrypt]`, `python-multipart`
   - Create `backend/pyproject.toml` for project metadata
3. Initialize frontend project:
   - Create `frontend/` and run `npm create vite@latest . -- --template react-ts`
   - Install dependencies: `react-router-dom`, `@tanstack/react-query`, `axios`
   - Install shadcn/ui: `npx shadcn-ui@latest init`
   - Add shadcn components: `table`, `button`, `dialog`, `form`, `input`, `select`, `tabs`, `badge`, `card`
4. Create `.gitignore` for Python, Node, and IDE files
5. Create `README.md` with project overview

**Reference**: `/opentt/` (new root directory)

---

## Step 2: Database Models and Schema Definition

**Goal**: Define all SQLAlchemy ORM models with proper relationships and constraints.

**Method**:
1. Create `backend/app/core/database.py`:
   - Define `DATABASE_URL` from environment
   - Create `async_engine` with `create_async_engine`
   - Create `AsyncSessionLocal` sessionmaker
   - Define `get_db()` dependency for FastAPI
2. Create base model in `backend/app/models/base.py`:
   - Define `Base = declarative_base()`
   - Add common fields: `id`, `created_at`, `updated_at`
3. Implement all models in `backend/app/models/`:
   - `institution.py`: Institution, AcademicYear, DayOfWeek, Period
   - `building.py`: Building, Room
   - `subject.py`: Subject, ActivityTag
   - `teacher.py`: Teacher
   - `student.py`: StudentYear, StudentGroup, StudentSubgroup
   - `activity.py`: Activity, ActivityTeacher (assoc table), ActivityStudentGroup, ActivityStudentSubgroup, ActivityTag (assoc), ActivityPreferredRoom
   - `constraint_*.py`: One file per constraint category (teacher, student, activity, room)
   - `solve_job.py`: SolveJob model with JSON columns for solution and stats
4. Define relationships:
   - Use `relationship()` with `back_populates`
   - Use `lazy="selectin"` for commonly accessed relationships
   - Add `cascade="all, delete-orphan"` where appropriate
5. Add proper indexes on foreign keys and commonly queried fields

**Reference**: `backend/app/models/`

---

## Step 3: Alembic Migration Setup

**Goal**: Initialize Alembic and create initial migration with all tables.

**Method**:
1. Run `alembic init alembic` in backend directory
2. Edit `alembic.ini`:
   - Set `sqlalchemy.url` to use environment variable
3. Edit `alembic/env.py`:
   - Import all models from `app.models`
   - Set `target_metadata = Base.metadata`
   - Configure async engine for migrations
4. Create initial migration:
   - Run `alembic revision --autogenerate -m "Initial schema"`
   - Review generated migration, ensure all tables and foreign keys are present
   - Test migration: `alembic upgrade head`
5. Add `alembic/versions/.gitkeep` to track directory

**Reference**: `backend/alembic/`

---

## Step 4: Pydantic Schemas

**Goal**: Define Pydantic v2 schemas for request/response validation.

**Method**:
1. Create schema files in `backend/app/schemas/` matching model structure
2. For each resource, define three schema classes:
   - `{Resource}Create`: Fields required for creation (no id, no timestamps)
   - `{Resource}Update`: Optional fields for updates
   - `{Resource}Read`: All fields including id, timestamps, relationships
3. Use Pydantic v2 features:
   - `ConfigDict(from_attributes=True)` for ORM mode
   - `Field(...)` for validation and descriptions
   - Nested schemas for relationships (e.g., `ActivityRead` includes `List[TeacherRead]`)
4. Create composite schemas for complex operations:
   - `ActivityWithRelations`: Activity + teachers + groups + rooms
   - `SolveJobRead`: Includes solution details and statistics
5. Add validator functions for business logic:
   - Validate time ranges (start_time < end_time)
   - Validate capacity constraints
   - Validate weight ranges (0-100)

**Reference**: `backend/app/schemas/`

---

## Step 5: Core Configuration and Settings

**Goal**: Set up application configuration, security, and utilities.

**Method**:
1. Create `backend/app/core/config.py`:
   - Use `pydantic_settings.BaseSettings`
   - Define all environment variables: DATABASE_URL, REDIS_URL, SECRET_KEY, CELERY_BROKER_URL, etc.
   - Set defaults for development
2. Create `backend/app/core/security.py`:
   - Implement JWT token creation/validation (optional for now, can add auth later)
   - Password hashing utilities
3. Create `backend/app/core/deps.py`:
   - `get_db()` dependency for database sessions
   - `get_current_institution()` dependency (validates institution_id exists)
4. Create `backend/app/core/exceptions.py`:
   - Custom exception classes: `NotFoundException`, `ConflictException`, `ValidationException`
   - Exception handlers for FastAPI

**Reference**: `backend/app/core/`

---

## Step 6: Service Layer Implementation

**Goal**: Implement business logic for all CRUD operations.

**Method**:
1. Create service classes in `backend/app/services/`:
   - One service per domain: `institution_service.py`, `teacher_service.py`, `room_service.py`, etc.
2. Each service implements standard CRUD operations:
   - `create()`: Insert new record, handle relationships
   - `get_by_id()`: Fetch single record with eager loading
   - `get_multi()`: List with pagination (skip, limit)
   - `update()`: Partial update with Pydantic model
   - `delete()`: Soft or hard delete, handle cascades
3. Add specialized methods:
   - `ActivityService.create_with_relations()`: Create activity with teachers/groups in single transaction
   - `ConstraintService.get_by_type()`: Fetch all constraints of a specific type
   - `InstitutionService.get_with_setup()`: Fetch institution with days, periods, rooms
4. Use async/await throughout
5. Handle exceptions and return None or raise custom exceptions

**Reference**: `backend/app/services/`

---

## Step 7: API Routes - Basic Resources

**Goal**: Implement REST endpoints for all basic resources.

**Method**:
1. Create route files in `backend/app/api/routes/`:
   - `institutions.py`, `teachers.py`, `rooms.py`, `subjects.py`, `buildings.py`
   - `students.py` (years, groups, subgroups)
   - `activities.py`, `activity_tags.py`
2. For each resource, implement standard endpoints:
   ```python
   POST   /institutions/{institution_id}/{resource}/           # Create
   GET    /institutions/{institution_id}/{resource}/           # List
   GET    /institutions/{institution_id}/{resource}/{id}       # Get by ID
   PUT    /institutions/{institution_id}/{resource}/{id}       # Update
   DELETE /institutions/{institution_id}/{resource}/{id}       # Delete
   ```
3. Use FastAPI features:
   - Dependency injection for `get_db()` and services
   - Automatic OpenAPI docs
   - Response models with Pydantic schemas
   - Status codes: 200, 201, 204, 404, 422
4. Add query parameters for filtering/pagination:
   - `skip: int = 0`, `limit: int = 100`
5. Create `backend/app/api/routes/__init__.py` to export all routers

**Reference**: `backend/app/api/routes/`

---

## Step 8: API Routes - Constraints

**Goal**: Implement endpoints for all 17+ constraint types.

**Method**:
1. Create `backend/app/api/routes/constraints.py`
2. Implement generic constraint endpoints:
   ```python
   POST   /institutions/{id}/constraints/{constraint_type}/       # Create
   GET    /institutions/{id}/constraints/{constraint_type}/       # List
   GET    /institutions/{id}/constraints/{constraint_type}/{cid}  # Get
   PUT    /institutions/{id}/constraints/{constraint_type}/{cid}  # Update
   DELETE /institutions/{id}/constraints/{constraint_type}/{cid}  # Delete
   GET    /institutions/{id}/constraints/                         # List all types
   ```
3. Use `constraint_type` path parameter to route to appropriate model
4. Map constraint types to models:
   ```python
   CONSTRAINT_MAP = {
       "teacher_not_available": TeacherNotAvailable,
       "teacher_max_hours_daily": TeacherMaxHoursDaily,
       # ... all 17 types
   }
   ```
5. Validate constraint_type against CONSTRAINT_MAP
6. Implement constraint-specific validation in schemas

**Reference**: `backend/app/api/routes/constraints.py`

---

## Step 9: FastAPI Main Application Setup

**Goal**: Wire up all routes and configure the FastAPI app.

**Method**:
1. Create `backend/app/main.py`:
   - Initialize FastAPI app with title, version, description
   - Configure CORS middleware (allow all origins in dev)
   - Add exception handlers from `core.exceptions`
   - Include all routers with appropriate prefixes:
     ```python
     app.include_router(institutions.router, prefix="/api/institutions", tags=["institutions"])
     app.include_router(teachers.router, prefix="/api", tags=["teachers"])
     # ... all routers
     ```
2. Add root endpoint: `GET /` returns `{"message": "OpenTT API"}`
3. Add health check: `GET /health` returns `{"status": "ok"}`
4. Configure Uvicorn in main:
   ```python
   if __name__ == "__main__":
       uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
   ```

**Reference**: `backend/app/main.py`

---

## Step 10: OR-Tools Solver - Data Loading

**Goal**: Create utilities to load institution data from database for solver.

**Method**:
1. Create `backend/app/solver/data_loader.py`
2. Define data classes using `@dataclass`:
   ```python
   @dataclass
   class DayData:
       id: int
       name: str
       order_index: int
   
   @dataclass
   class PeriodData:
       id: int
       name: str
       start_time: time
       end_time: time
       order_index: int
   
   @dataclass
   class ActivityData:
       id: int
       subject_id: int
       duration: int
       teacher_ids: List[int]
       student_group_ids: List[int]
       preferred_room_ids: List[int]
   
   @dataclass
   class InstitutionData:
       institution_id: int
       days: List[DayData]
       periods: List[PeriodData]
       rooms: List[RoomData]
       activities: List[ActivityData]
       constraints: ConstraintData
   ```
3. Implement `async def load_institution_data(institution_id: int, db: AsyncSession) -> InstitutionData`:
   - Load all days, periods, rooms, teachers, activities
   - Load all constraint records grouped by type
   - Build ActivityData objects with relationships resolved
   - Sort by order_index where applicable
4. Add caching to avoid redundant queries

**Reference**: `backend/app/solver/data_loader.py`

---

## Step 11: OR-Tools Solver - Model Building (Hard Constraints)

**Goal**: Implement the CP-SAT model with all hard constraints.

**Method**:
1. Create `backend/app/solver/model.py`
2. Define `TimetableModel` class:
   ```python
   class TimetableModel:
       def __init__(self, data: InstitutionData):
           self.data = data
           self.model = cp_model.CpModel()
           self.variables = {}
           self.soft_penalties = []
       
       def build(self) -> cp_model.CpModel:
           self._create_variables()
           self._add_hard_constraints()
           self._add_soft_constraints()
           self._set_objective()
           return self.model
   ```
3. Implement `_create_variables()`:
   - For each activity, day, period, room: create `BoolVar` named `x_a{aid}_d{did}_p{pid}_r{rid}`
   - Store in dict: `self.variables[(activity_id, day_id, period_id, room_id)] = var`
4. Implement hard constraints in `_add_hard_constraints()`:
   
   a. **Each activity assigned exactly once**:
   ```python
   for activity in activities:
       self.model.Add(sum(self.variables[(activity.id, d, p, r)] 
                          for d, p, r in all_slots) == 1)
   ```
   
   b. **Teacher conflict** (no teacher in 2 places at same time):
   ```python
   for teacher_id in teacher_ids:
       for day, period in day_period_combinations:
           activities_with_teacher = [a for a in activities if teacher_id in a.teacher_ids]
           self.model.Add(sum(self.variables[(a.id, day, period, r)] 
                              for a in activities_with_teacher 
                              for r in rooms) <= 1)
   ```
   
   c. **Student conflict** (similar to teacher):
   ```python
   for group_id in student_group_ids:
       for day, period in day_period_combinations:
           activities_with_group = [a for a in activities if group_id in a.student_group_ids]
           self.model.Add(sum(...) <= 1)
   ```
   
   d. **Room conflict**:
   ```python
   for room in rooms:
       for day, period in day_period_combinations:
           self.model.Add(sum(self.variables[(a.id, day, period, room.id)] 
                              for a in activities) <= 1)
   ```
   
   e. **Teacher not available**:
   ```python
   for constraint in teacher_not_available_constraints:
       teacher_activities = [a for a in activities if constraint.teacher_id in a.teacher_ids]
       for activity in teacher_activities:
           for room in rooms:
               self.model.Add(self.variables[(activity.id, constraint.day_id, 
                                              constraint.period_id, room.id)] == 0)
   ```
   
   f. **Students not available** (similar pattern)
   
   g. **Room not available** (similar pattern)
   
   h. **Room capacity**:
   ```python
   # Calculate students per activity, enforce room capacity
   for activity in activities:
       student_count = calculate_student_count(activity)
       for day, period in day_period_combinations:
           for room in rooms:
               if room.capacity < student_count:
                   self.model.Add(self.variables[(activity.id, day, period, room.id)] == 0)
   ```

5. Add helper methods:
   - `_get_activities_for_teacher(teacher_id)` 
   - `_get_activities_for_group(group_id)`
   - `_calculate_student_count(activity)`

**Reference**: `backend/app/solver/model.py`

---

## Step 12: OR-Tools Solver - Soft Constraints

**Goal**: Add weighted soft constraints to the objective function.

**Method**:
1. Extend `_add_soft_constraints()` in `model.py`:
   
   a. **Teacher max hours per day**:
   ```python
   for constraint in teacher_max_hours_daily:
       teacher_activities = self._get_activities_for_teacher(constraint.teacher_id)
       for day in days:
           hours_worked = sum(self.variables[(a.id, day.id, p.id, r.id)] 
                             for a in teacher_activities 
                             for p in periods 
                             for r in rooms)
           violation_var = self.model.NewIntVar(0, len(periods), f"teacher_{constraint.teacher_id}_day_{day.id}_violation")
           self.model.Add(violation_var >= hours_worked - constraint.max_hours)
           self.soft_penalties.append(violation_var * constraint.weight)
   ```
   
   b. **Teacher max gaps per day**:
   ```python
   # For each teacher, day: count gaps between assigned periods
   # Gap = period between first and last class where teacher is not teaching
   for constraint in teacher_max_gaps:
       for day in days:
           # Create first_period and last_period variables
           # Count periods where teacher has no class between first and last
           # Penalize if gaps > max_gaps
   ```
   
   c. **Students max hours per day** (similar to teacher)
   
   d. **Students max gaps per day** (similar to teacher)
   
   e. **Activity preferred starting time**:
   ```python
   for constraint in activity_preferred_time_constraints:
       # If activity NOT at preferred (day, period), add penalty
       not_preferred = 1 - sum(self.variables[(constraint.activity_id, constraint.day_id, 
                                                constraint.period_id, r.id)] 
                               for r in rooms)
       penalty_var = self.model.NewBoolVar(f"pref_time_penalty_{constraint.id}")
       self.model.Add(penalty_var == not_preferred)
       self.soft_penalties.append(penalty_var * constraint.weight)
   ```
   
   f. **Activity preferred room** (similar pattern)
   
   g. **Activities same starting time**:
   ```python
   for constraint in activities_same_time:
       activity_ids = constraint.activity_ids  # JSON list
       # Enforce all activities start at same (day, period)
       # If violated, add penalty
   ```
   
   h. **Min days between activities**:
   ```python
   for constraint in min_days_constraints:
       activity_ids = constraint.activity_ids
       # Use auxiliary variables to track day assignments
       # Penalize if activities scheduled within min_days
   ```

2. Implement `_set_objective()`:
   ```python
   def _set_objective(self):
       if self.soft_penalties:
           total_penalty = sum(self.soft_penalties)
           self.model.Minimize(total_penalty)
   ```

**Reference**: `backend/app/solver/model.py`

---

## Step 13: OR-Tools Solver - Solution Callback and Progress

**Goal**: Implement progress tracking during solving.

**Method**:
1. Create `backend/app/solver/callback.py`:
   ```python
   class ProgressCallback(cp_model.CpSolverSolutionCallback):
       def __init__(self, redis_client, job_id):
           super().__init__()
           self.redis = redis_client
           self.job_id = job_id
           self.last_update = time.time()
           self.solution_count = 0
       
       def on_solution_callback(self):
           self.solution_count += 1
           now = time.time()
           if now - self.last_update >= 5.0:  # Update every 5 seconds
               progress = {
                   "job_id": self.job_id,
                   "solution_count": self.solution_count,
                   "objective": self.ObjectiveValue(),
                   "wall_time": self.WallTime(),
               }
               self.redis.publish(f"solver_progress_{self.job_id}", json.dumps(progress))
               self.last_update = now
   ```

2. Create `backend/app/solver/runner.py`:
   ```python
   def solve_timetable(data: InstitutionData, time_limit: int, job_id: str) -> dict:
       # Build model
       model_builder = TimetableModel(data)
       model = model_builder.build()
       
       # Configure solver
       solver = cp_model.CpSolver()
       solver.parameters.max_time_in_seconds = time_limit
       solver.parameters.num_search_workers = os.cpu_count() or 4
       solver.parameters.log_search_progress = True
       
       # Create callback
       redis_client = redis.Redis.from_url(settings.REDIS_URL)
       callback = ProgressCallback(redis_client, job_id)
       
       # Solve
       status = solver.Solve(model, callback)
       
       # Extract solution
       solution = None
       if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
           solution = extract_solution(solver, model_builder.variables, data)
       
       return {
           "status": status,
           "solution": solution,
           "stats": {
               "objective_value": solver.ObjectiveValue() if solution else None,
               "wall_time": solver.WallTime(),
               "num_solutions": callback.solution_count,
           },
           "error": None if solution else "No feasible solution found"
       }
   
   def extract_solution(solver, variables, data) -> List[dict]:
       assignments = []
       for (activity_id, day_id, period_id, room_id), var in variables.items():
           if solver.Value(var) == 1:
               assignments.append({
                   "activity_id": activity_id,
                   "day_id": day_id,
                   "period_id": period_id,
                   "room_id": room_id,
               })
       return assignments
   ```

**Reference**: `backend/app/solver/runner.py`, `backend/app/solver/callback.py`

---

## Step 14: Celery Integration

**Goal**: Set up Celery for async solver job execution.

**Method**:
1. Create `backend/celery_app.py`:
   ```python
   from celery import Celery
   from app.core.config import settings
   
   celery_app = Celery(
       "opentt",
       broker=settings.CELERY_BROKER_URL,
       backend=settings.REDIS_URL,
   )
   
   celery_app.conf.update(
       task_serializer="json",
       result_serializer="json",
       accept_content=["json"],
       timezone="UTC",
       enable_utc=True,
   )
   ```

2. Create `backend/app/solver/tasks.py`:
   ```python
   from celery import Task
   from app.celery_app import celery_app
   from app.solver.data_loader import load_institution_data
   from app.solver.runner import solve_timetable
   from app.core.database import AsyncSessionLocal
   from app.models.solve_job import SolveJob
   
   @celery_app.task(bind=True)
   def solve_institution_timetable(self, institution_id: int, job_id: int, time_limit: int):
       try:
           # Load data
           async with AsyncSessionLocal() as db:
               data = await load_institution_data(institution_id, db)
               
               # Update job status
               job = await db.get(SolveJob, job_id)
               job.status = "running"
               job.started_at = datetime.utcnow()
               await db.commit()
           
           # Solve
           result = solve_timetable(data, time_limit, str(job_id))
           
           # Save result
           async with AsyncSessionLocal() as db:
               job = await db.get(SolveJob, job_id)
               job.status = "completed" if result["solution"] else "failed"
               job.finished_at = datetime.utcnow()
               job.solution = result["solution"]
               job.stats = result["stats"]
               job.error_text = result["error"]
               await db.commit()
               
       except Exception as e:
           async with AsyncSessionLocal() as db:
               job = await db.get(SolveJob, job_id)
               job.status = "failed"
               job.finished_at = datetime.utcnow()
               job.error_text = str(e)
               await db.commit()
   ```

3. Note: Since Celery doesn't support async tasks natively, wrap async code properly:
   ```python
   import asyncio
   
   def run_async(coro):
       loop = asyncio.get_event_loop()
       return loop.run_until_complete(coro)
   ```

**Reference**: `backend/celery_app.py`, `backend/app/solver/tasks.py`

---

## Step 15: Solve Endpoints

**Goal**: Implement API endpoints to trigger and monitor solver jobs.

**Method**:
1. Add solve endpoints in `backend/app/api/routes/solve.py`:
   ```python
   @router.post("/institutions/{institution_id}/solve/", response_model=SolveJobRead)
   async def create_solve_job(
       institution_id: int,
       time_limit: int = 300,
       db: AsyncSession = Depends(get_db)
   ):
       # Create job record
       job = SolveJob(
           institution_id=institution_id,
           status="pending",
           time_limit_seconds=time_limit,
       )
       db.add(job)
       await db.commit()
       await db.refresh(job)
       
       # Enqueue Celery task
       solve_institution_timetable.delay(institution_id, job.id, time_limit)
       
       return job
   
   @router.get("/institutions/{institution_id}/solve/{job_id}/", response_model=SolveJobRead)
   async def get_solve_job(
       institution_id: int,
       job_id: int,
       db: AsyncSession = Depends(get_db)
   ):
       job = await db.get(SolveJob, job_id)
       if not job or job.institution_id != institution_id:
           raise HTTPException(404, "Job not found")
       return job
   ```

2. Add WebSocket endpoint for live progress:
   ```python
   @router.websocket("/ws/{job_id}")
   async def websocket_progress(websocket: WebSocket, job_id: int):
       await websocket.accept()
       redis_client = redis.Redis.from_url(settings.REDIS_URL)
       pubsub = redis_client.pubsub()
       pubsub.subscribe(f"solver_progress_{job_id}")
       
       try:
           for message in pubsub.listen():
               if message["type"] == "message":
                   await websocket.send_text(message["data"])
       except WebSocketDisconnect:
           pubsub.unsubscribe(f"solver_progress_{job_id}")
   ```

**Reference**: `backend/app/api/routes/solve.py`

---

## Step 16: Export Endpoints

**Goal**: Implement CSV and HTML export functionality.

**Method**:
1. Create `backend/app/api/routes/export.py`:
   ```python
   @router.get("/institutions/{institution_id}/export/csv/")
   async def export_csv(
       institution_id: int,
       job_id: int,
       db: AsyncSession = Depends(get_db)
   ):
       # Load solution
       job = await db.get(SolveJob, job_id)
       if not job or not job.solution:
           raise HTTPException(404, "Solution not found")
       
       # Load institution data
       data = await load_institution_data(institution_id, db)
       
       # Generate CSV
       output = io.StringIO()
       writer = csv.writer(output)
       writer.writerow(["Activity", "Subject", "Teacher", "Group", "Day", "Period", "Room"])
       
       for assignment in job.solution:
           # Resolve IDs to names
           activity = next(a for a in data.activities if a.id == assignment["activity_id"])
           day = next(d for d in data.days if d.id == assignment["day_id"])
           # ... resolve others
           writer.writerow([activity.name, subject.name, teacher.name, ...])
       
       return Response(content=output.getvalue(), media_type="text/csv",
                       headers={"Content-Disposition": "attachment; filename=timetable.csv"})
   
   @router.get("/institutions/{institution_id}/export/html/")
   async def export_html(institution_id: int, job_id: int, db: AsyncSession = Depends(get_db)):
       # Similar to CSV, but generate HTML table
       html = generate_html_timetable(job.solution, data)
       return Response(content=html, media_type="text/html")
   ```

2. Create helper in `backend/app/services/export_service.py`:
   ```python
   def generate_html_timetable(solution: List[dict], data: InstitutionData) -> str:
       # Build HTML with tables grouped by class/teacher/room
       # Use Jinja2 template or string formatting
       html = """
       <!DOCTYPE html>
       <html>
       <head><title>Timetable</title><style>...</style></head>
       <body>
           <h1>Timetable</h1>
           <table>
               <thead>
                   <tr><th>Day</th><th>Period</th><th>Activity</th><th>Room</th></tr>
               </thead>
               <tbody>
                   <!-- rows -->
               </tbody>
           </table>
       </body>
       </html>
       """
       return html
   ```

**Reference**: `backend/app/api/routes/export.py`, `backend/app/services/export_service.py`

---

## Step 17: Frontend - Project Setup and Routing

**Goal**: Initialize frontend with routing and basic layout.

**Method**:
1. Configure Vite in `frontend/vite.config.ts`:
   - Set server port to 3000
   - Configure proxy: `/api` → `http://localhost:8000`
2. Set up React Router in `frontend/src/main.tsx`:
   ```tsx
   import { BrowserRouter, Routes, Route } from 'react-router-dom'
   import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
   
   const queryClient = new QueryClient()
   
   ReactDOM.createRoot(document.getElementById('root')!).render(
     <QueryClientProvider client={queryClient}>
       <BrowserRouter>
         <Routes>
           <Route path="/" element={<Dashboard />} />
           <Route path="/institutions/:id/*" element={<InstitutionLayout />}>
             <Route path="setup" element={<Setup />} />
             <Route path="teachers" element={<Teachers />} />
             <Route path="rooms" element={<Rooms />} />
             {/* ... all pages */}
           </Route>
         </Routes>
       </BrowserRouter>
     </QueryClientProvider>
   )
   ```

3. Create `frontend/src/components/Layout.tsx`:
   - App shell with navigation sidebar
   - Breadcrumbs
   - Header with institution selector

**Reference**: `frontend/src/main.tsx`, `frontend/src/components/Layout.tsx`

---

## Step 18: Frontend - API Client Setup

**Goal**: Set up Axios client and TanStack Query hooks.

**Method**:
1. Create `frontend/src/api/client.ts`:
   ```typescript
   import axios from 'axios'
   
   export const apiClient = axios.create({
     baseURL: '/api',
     headers: {
       'Content-Type': 'application/json',
     },
   })
   
   apiClient.interceptors.response.use(
     response => response,
     error => {
       // Handle errors globally
       console.error('API Error:', error)
       return Promise.reject(error)
     }
   )
   ```

2. Create query hooks in `frontend/src/api/`:
   - `useInstitutions.ts`: CRUD hooks for institutions
   - `useTeachers.ts`: CRUD hooks for teachers
   - `useRooms.ts`, `useActivities.ts`, etc.
   
   Example:
   ```typescript
   // frontend/src/api/useTeachers.ts
   import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
   import { apiClient } from './client'
   
   export function useTeachers(institutionId: number) {
     return useQuery({
       queryKey: ['teachers', institutionId],
       queryFn: async () => {
         const { data } = await apiClient.get(`/institutions/${institutionId}/teachers/`)
         return data
       },
     })
   }
   
   export function useCreateTeacher(institutionId: number) {
     const queryClient = useQueryClient()
     return useMutation({
       mutationFn: async (teacher: CreateTeacher) => {
         const { data } = await apiClient.post(`/institutions/${institutionId}/teachers/`, teacher)
         return data
       },
       onSuccess: () => {
         queryClient.invalidateQueries({ queryKey: ['teachers', institutionId] })
       },
     })
   }
   ```

**Reference**: `frontend/src/api/`

---

## Step 19: Frontend - CRUD Pages (Teachers, Rooms, Subjects)

**Goal**: Implement data entry pages with tables and forms.

**Method**:
1. Create `frontend/src/pages/Teachers.tsx`:
   - Use shadcn `Table` component to display teachers
   - Add "New Teacher" button that opens shadcn `Dialog` with form
   - Form uses shadcn `Form`, `Input`, `Button` components
   - On submit, call `useCreateTeacher` mutation
   - Add edit/delete buttons per row
   
   Example structure:
   ```tsx
   export function Teachers() {
     const { id } = useParams()
     const { data: teachers, isLoading } = useTeachers(Number(id))
     const [dialogOpen, setDialogOpen] = useState(false)
     
     return (
       <div>
         <h1>Teachers</h1>
         <Button onClick={() => setDialogOpen(true)}>New Teacher</Button>
         <Table>
           <TableHeader>
             <TableRow>
               <TableHead>Name</TableHead>
               <TableHead>Email</TableHead>
               <TableHead>Actions</TableHead>
             </TableRow>
           </TableHeader>
           <TableBody>
             {teachers?.map(teacher => (
               <TableRow key={teacher.id}>
                 <TableCell>{teacher.first_name} {teacher.last_name}</TableCell>
                 <TableCell>{teacher.email}</TableCell>
                 <TableCell>
                   <Button variant="ghost" onClick={() => handleEdit(teacher)}>Edit</Button>
                   <Button variant="ghost" onClick={() => handleDelete(teacher.id)}>Delete</Button>
                 </TableCell>
               </TableRow>
             ))}
           </TableBody>
         </Table>
         
         <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
           <DialogContent>
             <TeacherForm onSuccess={() => setDialogOpen(false)} />
           </DialogContent>
         </Dialog>
       </div>
     )
   }
   ```

2. Create similar pages:
   - `Rooms.tsx`
   - `Subjects.tsx`
   - `Buildings.tsx`
   - `ActivityTags.tsx`

3. Create reusable form components in `frontend/src/components/forms/`:
   - `TeacherForm.tsx`
   - `RoomForm.tsx`
   - etc.

**Reference**: `frontend/src/pages/`, `frontend/src/components/forms/`

---

## Step 20: Frontend - Setup Page (Days & Periods)

**Goal**: Allow configuring days of the week and time periods.

**Method**:
1. Create `frontend/src/pages/Setup.tsx`:
   - Split into two sections: Days and Periods
   - Days section:
     - Display list of days with order_index
     - Allow adding/removing/reordering days
     - Common preset: Monday-Friday
   - Periods section:
     - Display list with start_time, end_time, order_index
     - Allow adding/editing periods
     - Validate start < end, no overlaps
   
2. Use shadcn `Tabs` to organize sections
3. Add drag-and-drop for reordering (use `@dnd-kit/core`)

**Reference**: `frontend/src/pages/Setup.tsx`

---

## Step 21: Frontend - Students Page (Hierarchical View)

**Goal**: Display and manage the three-level student hierarchy.

**Method**:
1. Create `frontend/src/pages/Students.tsx`:
   - Display years in expandable cards/accordion
   - Each year shows its groups
   - Each group shows its subgroups
   - Add buttons at each level to create child entities
   
   Structure:
   ```tsx
   <Accordion>
     {years.map(year => (
       <AccordionItem key={year.id} value={year.id}>
         <AccordionTrigger>{year.name}</AccordionTrigger>
         <AccordionContent>
           <Button onClick={() => createGroup(year.id)}>Add Group</Button>
           {groups.filter(g => g.year_id === year.id).map(group => (
             <Card key={group.id}>
               <CardHeader>{group.name}</CardHeader>
               <CardContent>
                 <Button onClick={() => createSubgroup(group.id)}>Add Subgroup</Button>
                 {subgroups.filter(s => s.group_id === group.id).map(subgroup => (
                   <Badge key={subgroup.id}>{subgroup.name}</Badge>
                 ))}
               </CardContent>
             </Card>
           ))}
         </AccordionContent>
       </AccordionItem>
     ))}
   </Accordion>
   ```

2. Implement nested API hooks in `frontend/src/api/useStudents.ts`

**Reference**: `frontend/src/pages/Students.tsx`

---

## Step 22: Frontend - Activities Page

**Goal**: Manage activities with their relationships.

**Method**:
1. Create `frontend/src/pages/Activities.tsx`:
   - Table with columns: Subject, Duration, Teachers, Groups, Rooms, Actions
   - Teachers/Groups shown as comma-separated or badges
   - "New Activity" button opens multi-step dialog:
     - Step 1: Basic info (subject, duration)
     - Step 2: Select teachers (multi-select)
     - Step 3: Select student groups/subgroups (multi-select)
     - Step 4: Select preferred rooms (multi-select)
   
2. Use shadcn `Select` with multiple mode
3. Create `frontend/src/components/forms/ActivityForm.tsx`:
   - Use react-hook-form for validation
   - Handle relationships with array fields

**Reference**: `frontend/src/pages/Activities.tsx`

---

## Step 23: Frontend - Constraints Page

**Goal**: Manage all constraint types in a tabbed interface.

**Method**:
1. Create `frontend/src/pages/Constraints.tsx`:
   - Use shadcn `Tabs` with one tab per constraint category:
     - "Teacher" tab: teacher_not_available, max_hours_daily, max_gaps, etc.
     - "Student" tab: students_not_available, max_hours_daily, etc.
     - "Activity" tab: preferred_time, preferred_room, same_time, etc.
     - "Room" tab: room_not_available
   
2. Each tab shows:
   - List of existing constraints of that type
   - "Add Constraint" button
   - Form specific to that constraint type
   
3. Create constraint-specific forms:
   - `TeacherNotAvailableForm.tsx`: Select teacher, day, period, weight
   - `MaxHoursForm.tsx`: Select teacher/group, max hours, weight
   - `PreferredTimeForm.tsx`: Select activity, day, period, weight
   
4. Display weight as slider (0-100)

**Reference**: `frontend/src/pages/Constraints.tsx`, `frontend/src/components/forms/constraint/`

---

## Step 24: Frontend - Solve Page

**Goal**: Interface to trigger solving and display progress.

**Method**:
1. Create `frontend/src/pages/Solve.tsx`:
   - Input field for time_limit (default 300 seconds)
   - "Start Solving" button
   - Progress section:
     - Shows job status (pending, running, completed, failed)
     - Progress bar (animated while running)
     - Live updates: solution count, current objective, wall time
     - "View Timetable" button (appears when completed)
   
2. Implement WebSocket connection:
   ```tsx
   const [jobId, setJobId] = useState<number | null>(null)
   const [progress, setProgress] = useState<Progress | null>(null)
   
   useEffect(() => {
     if (!jobId) return
     
     const ws = new WebSocket(`ws://localhost:8000/ws/${jobId}`)
     ws.onmessage = (event) => {
       const data = JSON.parse(event.data)
       setProgress(data)
     }
     
     return () => ws.close()
   }, [jobId])
   
   const handleSolve = async () => {
     const job = await createSolveJob.mutateAsync({ time_limit })
     setJobId(job.id)
   }
   ```

3. Display statistics when completed:
   - Total assignments
   - Objective value (penalty sum)
   - Solve time

**Reference**: `frontend/src/pages/Solve.tsx`

---

## Step 25: Frontend - Timetable Viewer

**Goal**: Display the solution as an interactive grid.

**Method**:
1. Create `frontend/src/pages/Timetable.tsx`:
   - Tabs for different views: "By Class", "By Teacher", "By Room", "By Day"
   - Dropdown to select which class/teacher/room to view
   - Grid component that renders days × periods
   
2. Create `frontend/src/components/TimetableGrid.tsx`:
   ```tsx
   interface TimetableGridProps {
     assignments: Assignment[]
     days: Day[]
     periods: Period[]
     filter?: { type: 'teacher' | 'group' | 'room', id: number }
   }
   
   export function TimetableGrid({ assignments, days, periods, filter }: TimetableGridProps) {
     // Filter assignments by type
     const filtered = filter 
       ? assignments.filter(a => matchesFilter(a, filter))
       : assignments
     
     return (
       <table className="timetable-grid">
         <thead>
           <tr>
             <th>Period</th>
             {days.map(day => <th key={day.id}>{day.name}</th>)}
           </tr>
         </thead>
         <tbody>
           {periods.map(period => (
             <tr key={period.id}>
               <td>{period.name}</td>
               {days.map(day => {
                 const cell = filtered.find(a => a.day_id === day.id && a.period_id === period.id)
                 return (
                   <td key={day.id} className={cell ? 'filled' : 'empty'}>
                     {cell && (
                       <div className="activity-cell" style={{ background: cell.subject.color }}>
                         <div className="subject">{cell.subject.short_name}</div>
                         <div className="teacher">{cell.teacher.short_name}</div>
                         <div className="room">{cell.room.short_name}</div>
                       </div>
                     )}
                   </td>
                 )
               })}
             </tr>
           ))}
         </tbody>
       </table>
     )
   }
   ```

3. Add CSS for grid styling:
   - Fixed-width columns
   - Colored cells by subject
   - Hover effects
   - Responsive layout

**Reference**: `frontend/src/pages/Timetable.tsx`, `frontend/src/components/TimetableGrid.tsx`

---

## Step 26: Frontend - Dashboard

**Goal**: Create landing page with overview and quick actions.

**Method**:
1. Create `frontend/src/pages/Dashboard.tsx`:
   - List of institutions with quick links
   - Recent solve jobs table (institution, status, timestamp)
   - Quick stats cards:
     - Total institutions
     - Total activities
     - Recent solutions count
   - "Create Institution" button

2. Use shadcn `Card` components for stats
3. Add links to institution pages

**Reference**: `frontend/src/pages/Dashboard.tsx`

---

## Step 27: Docker Compose Setup

**Goal**: Orchestrate all services with Docker Compose.

**Method**:
1. Create `opentt/docker-compose.yml`:
   ```yaml
   version: '3.8'
   
   services:
     db:
       image: postgres:16
       environment:
         POSTGRES_USER: opentt
         POSTGRES_PASSWORD: opentt
         POSTGRES_DB: opentt
       ports:
         - "5432:5432"
       volumes:
         - postgres_data:/var/lib/postgresql/data
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U opentt"]
         interval: 10s
         timeout: 5s
         retries: 5
     
     redis:
       image: redis:7
       ports:
         - "6379:6379"
       healthcheck:
         test: ["CMD", "redis-cli", "ping"]
         interval: 10s
         timeout: 5s
         retries: 5
     
     api:
       build:
         context: ./backend
         dockerfile: Dockerfile
       command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql+asyncpg://opentt:opentt@db:5432/opentt
         - REDIS_URL=redis://redis:6379/0
         - CELERY_BROKER_URL=redis://redis:6379/0
       depends_on:
         db:
           condition: service_healthy
         redis:
           condition: service_healthy
       volumes:
         - ./backend:/app
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
         interval: 30s
         timeout: 10s
         retries: 3
     
     worker:
       build:
         context: ./backend
         dockerfile: Dockerfile
       command: celery -A app.celery_app worker --loglevel=info --concurrency=2
       environment:
         - DATABASE_URL=postgresql+asyncpg://opentt:opentt@db:5432/opentt
         - REDIS_URL=redis://redis:6379/0
         - CELERY_BROKER_URL=redis://redis:6379/0
       depends_on:
         - db
         - redis
       volumes:
         - ./backend:/app
     
     frontend:
       build:
         context: ./frontend
         dockerfile: Dockerfile
       ports:
         - "3000:80"
       depends_on:
         - api
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:80"]
         interval: 30s
         timeout: 10s
         retries: 3
   
   volumes:
     postgres_data:
   ```

2. Create `opentt/backend/Dockerfile`:
   ```dockerfile
   FROM python:3.12-slim
   
   WORKDIR /app
   
   # Install system dependencies
   RUN apt-get update && apt-get install -y \
       gcc \
       postgresql-client \
       && rm -rf /var/lib/apt/lists/*
   
   # Install Python dependencies
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Copy application
   COPY . .
   
   # Run migrations on startup (in entrypoint script)
   COPY entrypoint.sh /entrypoint.sh
   RUN chmod +x /entrypoint.sh
   
   ENTRYPOINT ["/entrypoint.sh"]
   ```

3. Create `opentt/backend/entrypoint.sh`:
   ```bash
   #!/bin/bash
   set -e
   
   # Wait for database
   until pg_isready -h db -U opentt; do
     echo "Waiting for database..."
     sleep 2
   done
   
   # Run migrations
   alembic upgrade head
   
   # Execute command
   exec "$@"
   ```

4. Create `opentt/frontend/Dockerfile`:
   ```dockerfile
   FROM node:20 as builder
   
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build
   
   FROM nginx:alpine
   COPY --from=builder /app/dist /usr/share/nginx/html
   COPY nginx.conf /etc/nginx/conf.d/default.conf
   ```

5. Create `opentt/frontend/nginx.conf`:
   ```nginx
   server {
     listen 80;
     server_name localhost;
     
     location / {
       root /usr/share/nginx/html;
       try_files $uri $uri/ /index.html;
     }
     
     location /api {
       proxy_pass http://api:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
     }
     
     location /ws {
       proxy_pass http://api:8000;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "upgrade";
     }
   }
   ```

6. Create `opentt/.env.example`:
   ```env
   # Database
   POSTGRES_USER=opentt
   POSTGRES_PASSWORD=opentt
   POSTGRES_DB=opentt
   DATABASE_URL=postgresql+asyncpg://opentt:opentt@db:5432/opentt
   
   # Redis
   REDIS_URL=redis://redis:6379/0
   CELERY_BROKER_URL=redis://redis:6379/0
   
   # Application
   SECRET_KEY=change-me-in-production
   DEBUG=True
   ```

**Reference**: `opentt/docker-compose.yml`, Dockerfiles, entrypoint scripts

---

## Step 28: Backend Testing - Unit Tests

**Goal**: Write pytest tests for models, services, and solver.

**Method**:
1. Create `backend/tests/conftest.py`:
   ```python
   import pytest
   import asyncio
   from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
   from app.core.database import Base
   from app.models import *
   
   @pytest.fixture(scope="session")
   def event_loop():
       loop = asyncio.get_event_loop_policy().new_event_loop()
       yield loop
       loop.close()
   
   @pytest.fixture
   async def db_session():
       engine = create_async_engine("sqlite+aiosqlite:///:memory:")
       async with engine.begin() as conn:
           await conn.run_sync(Base.metadata.create_all)
       
       async with AsyncSession(engine) as session:
           yield session
       
       await engine.dispose()
   
   @pytest.fixture
   async def sample_institution(db_session):
       institution = Institution(name="Test School", slug="test-school")
       db_session.add(institution)
       await db_session.commit()
       return institution
   ```

2. Create test files:
   - `backend/tests/test_models.py`:
     ```python
     async def test_create_institution(db_session):
         inst = Institution(name="Test", slug="test")
         db_session.add(inst)
         await db_session.commit()
         assert inst.id is not None
     
     async def test_activity_relationships(db_session, sample_institution):
         teacher = Teacher(institution_id=sample_institution.id, first_name="John", last_name="Doe")
         subject = Subject(institution_id=sample_institution.id, name="Math")
         db_session.add_all([teacher, subject])
         await db_session.commit()
         
         activity = Activity(institution_id=sample_institution.id, subject_id=subject.id, duration=1)
         activity.teachers.append(teacher)
         db_session.add(activity)
         await db_session.commit()
         
         assert len(activity.teachers) == 1
     ```
   
   - `backend/tests/test_services.py`:
     ```python
     from app.services.teacher_service import TeacherService
     
     async def test_teacher_crud(db_session, sample_institution):
         service = TeacherService(db_session)
         
         teacher = await service.create({
             "institution_id": sample_institution.id,
             "first_name": "Jane",
             "last_name": "Smith",
             "email": "jane@example.com"
         })
         assert teacher.id is not None
         
         retrieved = await service.get_by_id(teacher.id)
         assert retrieved.email == "jane@example.com"
     ```
   
   - `backend/tests/test_solver.py`:
     ```python
     from app.solver.model import TimetableModel
     from app.solver.data_loader import InstitutionData, ActivityData, DayData, PeriodData, RoomData
     
     def test_solver_simple_case():
         # Create minimal dataset
         data = InstitutionData(
             institution_id=1,
             days=[DayData(id=1, name="Monday", order_index=0)],
             periods=[
                 PeriodData(id=1, name="Period 1", start_time=time(8, 0), end_time=time(9, 0), order_index=0),
                 PeriodData(id=2, name="Period 2", start_time=time(9, 0), end_time=time(10, 0), order_index=1),
             ],
             rooms=[RoomData(id=1, name="Room A", capacity=30)],
             activities=[
                 ActivityData(id=1, subject_id=1, duration=1, teacher_ids=[1], student_group_ids=[1], preferred_room_ids=[1]),
                 ActivityData(id=2, subject_id=2, duration=1, teacher_ids=[2], student_group_ids=[1], preferred_room_ids=[1]),
             ],
             constraints=ConstraintData(teacher_not_available=[], ...)
         )
         
         model = TimetableModel(data)
         cp_model = model.build()
         
         from ortools.sat.python import cp_model as cp
         solver = cp.CpSolver()
         solver.parameters.max_time_in_seconds = 10
         status = solver.Solve(cp_model)
         
         assert status in [cp.OPTIMAL, cp.FEASIBLE]
     ```

3. Run tests: `pytest backend/tests/ -v`

**Reference**: `backend/tests/`

---

## Step 29: Frontend Testing - E2E with Playwright

**Goal**: Write end-to-end test for the happy path.

**Method**:
1. Install Playwright: `npm install -D @playwright/test`
2. Initialize: `npx playwright install`
3. Create `frontend/e2e/happy-path.spec.ts`:
   ```typescript
   import { test, expect } from '@playwright/test'
   
   test('complete timetable workflow', async ({ page }) => {
     // Navigate to app
     await page.goto('http://localhost:3000')
     
     // Create institution
     await page.click('text=Create Institution')
     await page.fill('input[name="name"]', 'Test School')
     await page.fill('input[name="slug"]', 'test-school')
     await page.click('button:has-text("Create")')
     
     // Wait for navigation to institution page
     await expect(page).toHaveURL(/\/institutions\/\d+/)
     
     // Add 2 teachers
     await page.click('a:has-text("Teachers")')
     await page.click('button:has-text("New Teacher")')
     await page.fill('input[name="first_name"]', 'John')
     await page.fill('input[name="last_name"]', 'Doe')
     await page.fill('input[name="email"]', 'john@example.com')
     await page.click('button:has-text("Save")')
     
     // Repeat for second teacher
     // ... similar steps
     
     // Add 2 rooms
     await page.click('a:has-text("Rooms")')
     await page.click('button:has-text("New Room")')
     await page.fill('input[name="name"]', 'Room A')
     await page.fill('input[name="capacity"]', '30')
     await page.click('button:has-text("Save")')
     // ... repeat
     
     // Add 1 subject
     await page.click('a:has-text("Subjects")')
     // ... similar steps
     
     // Add 4 activities
     await page.click('a:has-text("Activities")')
     for (let i = 0; i < 4; i++) {
       await page.click('button:has-text("New Activity")')
       // Fill form
       await page.click('button:has-text("Save")')
     }
     
     // Start solve
     await page.click('a:has-text("Solve")')
     await page.fill('input[name="time_limit"]', '60')
     await page.click('button:has-text("Start Solving")')
     
     // Wait for completion (max 90 seconds)
     await page.waitForSelector('text=completed', { timeout: 90000 })
     
     // View timetable
     await page.click('button:has-text("View Timetable")')
     
     // Verify grid has 4 filled cells
     const filledCells = await page.locator('.activity-cell').count()
     expect(filledCells).toBeGreaterThanOrEqual(4)
     
     // Verify no conflicts: check each row+column has unique teachers
     // (This requires more complex logic - iterate cells and check)
     const cells = await page.locator('.activity-cell').all()
     const cellData = await Promise.all(cells.map(cell => cell.textContent()))
     
     // Check no duplicate teachers in same time slot
     // (Implementation depends on exact HTML structure)
   })
   ```

4. Add script to `package.json`:
   ```json
   {
     "scripts": {
       "test:e2e": "playwright test"
     }
   }
   ```

**Reference**: `frontend/e2e/happy-path.spec.ts`

---

## Step 30: Documentation and README

**Goal**: Write comprehensive setup and usage documentation.

**Method**:
1. Update `opentt/README.md`:
   ```markdown
   # OpenTT - Open Timetable

   An open-source timetable scheduling system for schools and universities, powered by Google OR-Tools CP-SAT solver.

   ## Features
   - Complete CRUD interface for institutions, teachers, rooms, students, activities
   - 17+ constraint types (availability, max hours, gaps, preferred times, etc.)
   - Automatic timetable generation using constraint programming
   - Real-time solver progress tracking
   - Multiple timetable views (by class, teacher, room, day)
   - Export to HTML and CSV

   ## Tech Stack
   - Backend: Python 3.12, FastAPI, SQLAlchemy, Celery, Redis, OR-Tools
   - Frontend: React 18, TypeScript, Vite, TanStack Query, shadcn/ui
   - Database: PostgreSQL 16
   - Infrastructure: Docker Compose

   ## Quick Start

   ### Prerequisites
   - Docker and Docker Compose
   - (Optional) Node.js 20+ and Python 3.12+ for local development

   ### Running with Docker Compose

   1. Clone the repository:
      ```bash
      git clone <repo-url>
      cd opentt
      ```

   2. Copy environment file:
      ```bash
      cp .env.example .env
      ```

   3. Start all services:
      ```bash
      docker compose up -d
      ```

   4. Wait for services to be healthy (check with `docker compose ps`)

   5. Run database migrations:
      ```bash
      docker compose exec api alembic upgrade head
      ```

   6. Access the application:
      - Frontend: http://localhost:3000
      - API docs: http://localhost:8000/docs
      - Redis: localhost:6379
      - PostgreSQL: localhost:5432

   ### Local Development

   #### Backend
   ```bash
   cd backend
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

   Start Celery worker:
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

   #### Frontend
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

   ## Usage

   1. **Create Institution**: Set up your school/university with name and timezone
   2. **Configure Setup**: Define days of week and time periods
   3. **Add Resources**: Create teachers, rooms, buildings, subjects
   4. **Add Students**: Create student years, groups, and subgroups
   5. **Define Activities**: Create activities linking subjects, teachers, and student groups
   6. **Set Constraints**: Add availability constraints, max hours, preferred times, etc.
   7. **Solve**: Click "Solve" to generate the timetable (may take seconds to minutes)
   8. **View**: Explore the generated timetable in various views
   9. **Export**: Download as HTML or CSV

   ## Testing

   ### Backend Tests
   ```bash
   cd backend
   pytest tests/ -v
   ```

   ### Frontend Tests
   ```bash
   cd frontend
   npm run test:e2e
   ```

   ## Architecture

   ### Database Schema
   - 20+ tables modeling institutions, resources, activities, and constraints
   - Proper foreign key relationships and cascade deletes
   - JSON columns for solver results and activity relationships

   ### Solver Algorithm
   - Uses Google OR-Tools CP-SAT (Constraint Programming - SAT solver)
   - Models timetabling as boolean satisfaction problem
   - Hard constraints: no conflicts, availability
   - Soft constraints: preferences weighted by penalty
   - Multi-threaded solving with progress callbacks

   ### API Design
   - RESTful endpoints following resource-based patterns
   - Async I/O with SQLAlchemy async
   - Pydantic v2 schemas for validation
   - WebSocket for real-time progress updates

   ## Contributing
   See CONTRIBUTING.md

   ## License
   MIT License - see LICENSE file
   ```

2. Create `opentt/CONTRIBUTING.md` with development guidelines
3. Create `opentt/docs/` directory with:
   - `API.md`: API endpoint documentation
   - `SOLVER.md`: Solver algorithm explanation
   - `DATABASE.md`: Database schema documentation

**Reference**: `opentt/README.md`, `opentt/docs/`

---

## Step 31: Final Integration and Testing

**Goal**: Ensure all components work together end-to-end.

**Method**:
1. Start all services:
   ```bash
   cd opentt
   docker compose up --build
   ```

2. Verify all containers are healthy:
   ```bash
   docker compose ps
   ```

3. Test complete workflow manually:
   - Create institution via UI
   - Add test data (2 teachers, 2 rooms, 1 subject, 4 activities)
   - Add 1-2 constraints
   - Click solve
   - Wait for completion
   - Verify timetable displays correctly
   - Test export functions

4. Run all automated tests:
   ```bash
   # Backend tests
   docker compose exec api pytest tests/ -v
   
   # Frontend E2E tests
   cd frontend
   npm run test:e2e
   ```

5. Check for acceptance criteria:
   - ✅ docker compose up starts with no errors
   - ✅ Can create institution and all resources
   - ✅ Can add at least 5 constraint types
   - ✅ Solve shows live progress and displays result
   - ✅ No overlaps in timetable grid
   - ✅ Export HTML works
   - ✅ All pytest tests pass
   - ✅ README has clear instructions
   - ✅ E2E test passes

6. Performance benchmarks:
   - Test with small dataset: 3 teachers, 10 activities, 5 days × 6 periods
   - Should find feasible solution in < 30 seconds
   - Test with medium dataset: 20 teachers, 100 activities
   - Document solve times

7. Fix any issues found during integration testing

**Reference**: Entire project

---

## Step 32: Deployment Preparation

**Goal**: Prepare the application for production deployment.

**Method**:
1. Update `docker-compose.yml` for production:
   - Remove volume mounts (use images)
   - Add restart policies: `restart: unless-stopped`
   - Use secrets for sensitive environment variables
   
2. Create `docker-compose.prod.yml`:
   - Use production-ready Postgres configuration
   - Set appropriate resource limits
   - Configure proper networking

3. Add health check monitoring:
   - Implement `/health` endpoint that checks DB, Redis connectivity
   - Add Prometheus metrics (optional)

4. Security hardening:
   - Change default passwords in `.env`
   - Add CORS configuration for production domain
   - Enable HTTPS (add nginx SSL configuration)
   - Implement rate limiting

5. Create deployment guide in `docs/DEPLOYMENT.md`

**Reference**: `opentt/docker-compose.prod.yml`, `opentt/docs/DEPLOYMENT.md`

# 5. TESTING AND VALIDATION

## Unit Testing Success Criteria

### Backend Tests (pytest)
All backend tests must pass with 100% success rate:

1. **Model Tests** (`tests/test_models.py`):
   - Create and retrieve all model types
   - Verify foreign key relationships work correctly
   - Test cascade deletes (deleting institution removes all related records)
   - Validate model constraints (e.g., start_time < end_time)
   
2. **Service Tests** (`tests/test_services.py`):
   - CRUD operations for all resources
   - Create activity with relationships in single transaction
   - Update operations preserve related data
   - Delete operations handle cascades properly
   
3. **Solver Tests** (`tests/test_solver.py`):
   - **Smoke test with tiny dataset**:
     - 3 teachers, 10 activities, 5 days, 6 periods, 3 rooms
     - No constraints (only hard conflicts)
     - Must find feasible solution in < 30 seconds
   - **Constraint validation**:
     - Teacher not available constraint is respected
     - Room conflicts are prevented
     - Student group conflicts are prevented
   - **Variable creation**:
     - Verify correct number of BoolVars created
     - Verify variable naming convention
   
4. **API Tests** (`tests/test_api.py`):
   - All endpoints return correct status codes
   - Create resource returns 201 with created object
   - Update resource returns 200
   - Delete resource returns 204
   - Get non-existent resource returns 404
   - Validation errors return 422

**Command**: `docker compose exec api pytest tests/ -v --cov=app --cov-report=term`

**Expected**: All tests pass, coverage > 70%

---

## Integration Testing Success Criteria

### Docker Compose Health
All services must start successfully and remain healthy:

```bash
docker compose up -d
docker compose ps  # All services should show "healthy" status
```

**Expected output**:
- db: healthy
- redis: healthy
- api: healthy
- worker: running
- frontend: healthy

### Database Migrations
Migrations must apply cleanly on fresh database:

```bash
docker compose exec api alembic upgrade head
docker compose exec api alembic current  # Should show head revision
```

**Expected**: No errors, all 20+ tables created

### API Endpoint Verification
Use curl or Postman to verify key endpoints:

```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status": "ok"}

# Create institution
curl -X POST http://localhost:8000/api/institutions/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test School", "slug": "test-school", "timezone": "UTC"}'
# Expected: 201 with institution object

# List institutions
curl http://localhost:8000/api/institutions/
# Expected: 200 with array including created institution
```

### Celery Worker Functionality
Verify worker can process tasks:

```bash
docker compose logs worker
# Should show: "[INFO] celery.worker.strategy: Received task: app.solver.tasks.solve_institution_timetable"
```

**Expected**: Worker starts without errors, connects to Redis

---

## End-to-End Testing Success Criteria

### Playwright E2E Test (`frontend/e2e/happy-path.spec.ts`)

**Test scenario**: Complete workflow from institution creation to timetable viewing

**Steps**:
1. Create new institution
2. Add 2 teachers (with different names)
3. Add 2 rooms (with capacity > 0)
4. Add 1 subject
5. Add 4 activities (each with subject, teacher, room assignments)
6. Navigate to Solve page
7. Start solver with 60s time limit
8. Wait for job completion (max 90s)
9. View generated timetable
10. Verify 4 cells are filled in the grid
11. Verify no two activities in same time slot have same teacher

**Command**: `cd frontend && npm run test:e2e`

**Expected**: All assertions pass, test completes in < 2 minutes

---

## Acceptance Criteria Checklist

Run through all acceptance criteria from requirements:

### 1. Docker Compose Startup
```bash
cd opentt
docker compose up --build
```
- ✅ All services start without errors
- ✅ No port conflicts
- ✅ Database initializes correctly
- ✅ Migrations run automatically

### 2. Data Entry via UI
Access http://localhost:3000 and verify:
- ✅ Can create an institution
- ✅ Can add days of week (Monday-Friday)
- ✅ Can add periods (e.g., 6 periods)
- ✅ Can add rooms (with building, capacity)
- ✅ Can add teachers (with email)
- ✅ Can add students (years → groups → subgroups)
- ✅ Can add activities (with subject, teachers, groups)

### 3. Constraint Management
- ✅ Can add teacher_not_available constraint
- ✅ Can add teacher_max_hours_daily constraint
- ✅ Can add students_max_hours_daily constraint
- ✅ Can add activity_preferred_starting_time constraint
- ✅ Can add room_not_available constraint
- ✅ Constraints display correctly in UI
- ✅ Can edit/delete constraints

### 4. Solver Functionality
- ✅ Clicking "Solve" enqueues Celery job
- ✅ Job ID is returned immediately
- ✅ Status shows "pending" → "running" → "completed"
- ✅ Progress updates appear in real-time (solution count, objective, time)
- ✅ Solution completes within time limit or timeout
- ✅ "View Timetable" button appears on completion

### 5. Timetable Display
Navigate to timetable viewer and verify:
- ✅ Grid displays with days as columns, periods as rows
- ✅ Each filled cell shows: subject, teacher, room
- ✅ Cells are colored by subject color
- ✅ Empty cells are blank (not "undefined" or error)
- ✅ No overlapping activities (same teacher/group/room in multiple cells at same time)
- ✅ Tabs work: "By Class", "By Teacher", "By Room"
- ✅ Filtering by teacher/room/group shows correct subset

### 6. Export Functionality
- ✅ Click "Export HTML" downloads HTML file
- ✅ HTML file opens in browser and displays timetable
- ✅ HTML includes all activities with correct times
- ✅ Click "Export CSV" downloads CSV file
- ✅ CSV contains columns: Activity, Subject, Teacher, Group, Day, Period, Room
- ✅ CSV rows match timetable grid

### 7. Backend Tests
```bash
docker compose exec api pytest tests/ -v
```
- ✅ All test files execute
- ✅ Model tests pass
- ✅ Service tests pass
- ✅ Solver smoke test passes (finds solution in < 30s)
- ✅ API tests pass
- ✅ No test errors or warnings

### 8. Documentation
Check `opentt/README.md`:
- ✅ Clear prerequisites listed
- ✅ Step-by-step setup instructions
- ✅ Commands for running locally and with Docker
- ✅ Usage instructions for each major feature
- ✅ API documentation link
- ✅ Architecture explanation

### 9. Playwright E2E Test
```bash
cd frontend && npm run test:e2e
```
- ✅ Test creates institution and resources
- ✅ Test triggers solve and waits for completion
- ✅ Test verifies timetable grid renders
- ✅ Test verifies 4+ filled cells
- ✅ Test verifies no teacher conflicts (no duplicate teacher names in same row+column)
- ✅ All assertions pass

---

## Performance Validation

### Small Dataset Benchmark
**Setup**:
- 3 teachers
- 10 activities (distributed among teachers)
- 5 days × 6 periods = 30 time slots
- 3 rooms
- No soft constraints

**Expected**: Feasible solution found in < 30 seconds

**Command**: Trigger solve via API or UI, measure completion time

### Medium Dataset Benchmark
**Setup**:
- 20 teachers
- 100 activities
- 5 days × 8 periods = 40 time slots
- 10 rooms
- 10 constraints (mix of availability and preferences)

**Expected**: Feasible or best-effort solution in < 5 minutes

**Notes**: Document solve time in README for reference

---

## Failure Scenarios to Test

### 1. Infeasible Constraints
- Create scenario where teacher has 10 activities but only 5 periods available
- **Expected**: Solver returns "failed" status with message "No feasible solution found"
- **UI**: Shows error message, no timetable displayed

### 2. Empty Dataset
- Create institution with no activities
- **Expected**: Solve completes immediately, returns empty solution

### 3. Network Issues
- Stop Redis container during solve
- **Expected**: Job fails gracefully with error message

### 4. Database Constraints
- Try to delete teacher assigned to activities
- **Expected**: Cascade delete removes activities OR returns error preventing deletion (depending on FK constraint config)

---

## Success Definition

The implementation is considered **complete and successful** when:

1. All 9 acceptance criteria pass ✅
2. All backend pytest tests pass ✅
3. E2E Playwright test passes ✅
4. Small dataset solves in < 30 seconds ✅
5. No errors in docker compose logs after 5 minutes of operation ✅
6. README instructions allow new user to run system successfully ✅
7. Timetable grid displays correctly with no visual bugs ✅
8. Export functions produce valid HTML and CSV files ✅

If any criterion fails, debugging and fixes must be applied before considering the project complete.
