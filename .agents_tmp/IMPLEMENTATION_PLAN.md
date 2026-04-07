# OpenTT - Strategic Implementation Plan

## 🎯 Goal: Working Demo in 10-15 Hours

**Strategy**: Build the "Golden Path" - minimum features needed to demonstrate end-to-end timetable generation.

---

## 📋 Phase Breakdown

### ✅ Phase 0: Foundation (COMPLETE)
- Backend API (100%)
- Frontend structure (100%)
- All ready to build on

---

### 🔥 Phase 1: Essential Setup (2-3 hours) - START HERE
**Goal**: Configure institution basics

#### 1.1 Setup Page - Days & Periods (1.5-2h)
**Why first**: Required for any timetable, establishes CRUD patterns

**Features**:
- Institution selector/creator (use first institution by default for demo)
- Days of week management (Mon-Fri)
  - Add day dialog
  - Edit day inline
  - Delete with confirmation
  - Drag to reorder
- Periods management (e.g., 8:00-9:00, 9:00-10:00)
  - Add period dialog
  - Time pickers
  - Edit/delete
  - Auto-order by start time

**Components to build**:
- `src/pages/Setup.tsx` (main page)
- `src/components/setup/DaysSection.tsx`
- `src/components/setup/PeriodsSection.tsx`
- `src/components/setup/AddDayDialog.tsx`
- `src/components/setup/AddPeriodDialog.tsx`
- `src/hooks/useInstitution.ts` (shared hook)

**Pattern established**: React Query mutations, form handling, dialogs

---

### 🔥 Phase 2: Simple CRUD - Teachers (1-1.5h)
**Goal**: Establish reusable CRUD pattern

**Features**:
- List teachers in a table
- Add teacher button → dialog
- Edit button → same dialog
- Delete button → confirmation
- Search/filter

**Components**:
- `src/pages/Teachers.tsx`
- `src/components/teachers/TeacherDialog.tsx`
- `src/components/teachers/TeacherTable.tsx`
- `src/components/shared/DataTable.tsx` (reusable)
- `src/components/shared/ConfirmDialog.tsx` (reusable)

**Pattern established**: Table CRUD, reusable components

---

### 🔥 Phase 3: Quick Resource Setup (2-3h)
**Goal**: Get enough data to create activities

#### 3.1 Subjects Page (0.5h)
- Copy Teachers pattern
- Add color picker

#### 3.2 Rooms Page (1h)
- Simple version: Just rooms list (skip buildings hierarchy for MVP)
- Name, capacity, type

#### 3.3 Students Page - Simplified (1h)
- Single-level for MVP (just Groups, skip Year/Subgroup hierarchy)
- Name, student count
- Can enhance later

**Total resources**: Teachers, Subjects, Rooms, Student Groups

---

### 🔥 Phase 4: Activities - Minimal (2h)
**Goal**: Create schedulable activities

**Features** (simplified for MVP):
- List activities
- Add activity:
  - Name
  - Subject (dropdown)
  - Teacher (dropdown, single for MVP)
  - Student group (dropdown, single for MVP)
  - Duration (default: 1)
  - Requires room? (checkbox)
- Edit/delete

**Skip for MVP**: 
- Multiple teachers
- Multiple groups
- Preferred rooms
- Tags
- Advanced options

**Components**:
- `src/pages/Activities.tsx`
- `src/components/activities/ActivityDialog.tsx`
- `src/components/activities/ActivityTable.tsx`

---

### 🔥 Phase 5: Solve Page (1.5h)
**Goal**: Generate timetable!

**Features**:
- "Solve Timetable" button
- Time limit slider (30s - 5min)
- Start solve → show progress
- Poll job status every 2s
- Show status: Pending → Running → Completed/Failed
- On success: "View Timetable" button

**Components**:
- `src/pages/Solve.tsx`
- `src/components/solve/SolveConfig.tsx`
- `src/components/solve/SolveProgress.tsx`

---

### 🔥 Phase 6: Timetable Viewer (2-3h)
**Goal**: Display the result!

**Features** (MVP):
- Grid layout: Days × Periods
- Show all activities on grid
- Each cell shows: Subject, Teacher, Room, Group
- Color code by subject
- Simple, no filters for MVP

**Components**:
- `src/pages/Timetable.tsx`
- `src/components/timetable/TimetableGrid.tsx`
- `src/components/timetable/ActivityCell.tsx`

---

### 🔥 Phase 7: Dashboard (0.5h)
**Goal**: Nice landing page

**Features**:
- Stats cards (counts)
- "Quick Solve" button
- "View Last Timetable" button

**Components**:
- `src/pages/Dashboard.tsx`
- `src/components/dashboard/StatCard.tsx`

---

## 🎯 MVP Complete = ~10-12 hours

**You can now**:
1. Setup institution (days, periods)
2. Add teachers, subjects, rooms, groups
3. Create activities
4. Click "Solve"
5. View generated timetable!

---

## 📈 Phase 8: Enhancements (5-10h)
**After MVP works**:

1. **Better Students** (1h)
   - Add 3-level hierarchy
   - Tree view

2. **Better Activities** (2h)
   - Multiple teachers
   - Multiple groups
   - Preferred rooms

3. **Constraints** (2-3h)
   - Teacher not available
   - Max hours per day
   - UI for selecting time slots

4. **Better Timetable** (2h)
   - View selector (by teacher, by room, by group)
   - Filters
   - Print view

5. **Export** (2h)
   - CSV export
   - PDF generation

---

## 🏗️ Implementation Order (Recommended)

```
Day 1 (4-5h):
  ✅ Setup page
  ✅ Teachers page
  ✅ Dashboard skeleton

Day 2 (3-4h):
  ✅ Subjects page
  ✅ Rooms page (simple)
  ✅ Students page (simple)

Day 3 (3-4h):
  ✅ Activities page (MVP)
  ✅ Solve page

Day 4 (2-3h):
  ✅ Timetable viewer (MVP)
  ✅ Polish & test end-to-end

Total: 12-16 hours to working demo
```

---

## 🎨 UI/UX Principles

1. **Simple First**: Get it working, then make it pretty
2. **Reuse Components**: Build generic components (DataTable, Dialog, etc.)
3. **Consistent Patterns**: Same flow for all CRUD operations
4. **Instant Feedback**: Loading states, success messages
5. **Mobile Later**: Desktop-first for MVP

---

## 🔧 Technical Patterns

### React Query Pattern:
```typescript
// List
const { data: teachers, isLoading } = useQuery({
  queryKey: ['teachers', institutionId],
  queryFn: () => teacherService.getAll(institutionId),
});

// Create
const createMutation = useMutation({
  mutationFn: (data) => teacherService.create(institutionId, data),
  onSuccess: () => queryClient.invalidateQueries(['teachers']),
});
```

### Form Pattern:
```typescript
// Use react-hook-form
const form = useForm<TeacherCreate>({
  defaultValues: { ... }
});

const onSubmit = (data) => {
  createMutation.mutate(data);
};
```

### Component Pattern:
```
Page (Teachers.tsx)
  ├─ Header with Add button
  ├─ DataTable component
  └─ Dialog component
```

---

## 🚀 Let's Start!

**Next immediate steps**:
1. Install form dependencies: `react-hook-form`, `@hookform/resolvers`, `zod`
2. Build Setup page (Days & Periods)
3. Build Teachers page
4. Continue down the list...

**Success Criteria for MVP**:
- [ ] Can setup institution
- [ ] Can add 2 teachers, 2 subjects, 2 rooms, 1 group
- [ ] Can create 4 activities
- [ ] Can click "Solve" and get a timetable
- [ ] Can view the timetable in a grid

**When this works, you have a demo-able product!** 🎉

---

## 💡 After MVP

Once working:
- Add constraints
- Better UI/UX
- Export features
- Testing
- Documentation
- Deploy

---

**Ready to start building?** Let's go! 🚀
