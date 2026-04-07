# OpenTT - Next Steps Plan

## Current Status: Backend Complete (75%), Frontend Skeleton (25%)

---

## 🎯 Phase 1: Frontend Foundation (3-5 hours)
**Priority: CRITICAL** | **Dependencies: None**

### 1.1 API Client Setup (1-2 hours)
**Goal**: Create type-safe API client for backend communication

**Tasks**:
- [ ] Install dependencies:
  ```bash
  npm install axios @tanstack/react-query react-router-dom
  npm install -D @types/node
  ```
- [ ] Create `src/lib/api.ts` - Axios instance with base URL
- [ ] Create `src/lib/queryClient.ts` - React Query setup
- [ ] Create API service functions in `src/services/`:
  - `institutionService.ts`
  - `teacherService.ts`
  - `roomService.ts`
  - `subjectService.ts`
  - `studentService.ts`
  - `activityService.ts`
  - `constraintService.ts`
  - `solveService.ts`
- [ ] Add TypeScript interfaces matching backend schemas in `src/types/`

**Files to create**:
- `src/lib/api.ts`
- `src/lib/queryClient.ts`
- `src/types/index.ts` (all type definitions)
- `src/services/*.ts` (8 service files)

**Reference**: Backend schemas in `backend/app/schemas/`

---

### 1.2 Routing Setup (1 hour)
**Goal**: Configure React Router with all pages

**Tasks**:
- [ ] Install React Router: `npm install react-router-dom`
- [ ] Create route structure in `src/App.tsx`
- [ ] Create page components (empty shells):
  - `src/pages/Dashboard.tsx`
  - `src/pages/Setup.tsx`
  - `src/pages/Teachers.tsx`
  - `src/pages/Rooms.tsx`
  - `src/pages/Subjects.tsx`
  - `src/pages/Students.tsx`
  - `src/pages/Activities.tsx`
  - `src/pages/Constraints.tsx`
  - `src/pages/Solve.tsx`
  - `src/pages/Timetable.tsx`
- [ ] Create layout component: `src/components/Layout.tsx`
- [ ] Create navigation sidebar: `src/components/Sidebar.tsx`

**Route Structure**:
```
/ → Dashboard
/setup → Setup (Days & Periods)
/teachers → Teachers CRUD
/rooms → Rooms CRUD
/subjects → Subjects CRUD
/students → Students (Hierarchical)
/activities → Activities Management
/constraints → Constraints Configuration
/solve → Solve Timetable
/timetable → View Timetable
```

---

### 1.3 Shared Components (1-2 hours)
**Goal**: Create reusable UI components

**Tasks**:
- [ ] Create `src/components/DataTable.tsx` - Generic table with sorting/filtering
- [ ] Create `src/components/LoadingSpinner.tsx`
- [ ] Create `src/components/ErrorAlert.tsx`
- [ ] Create `src/components/ConfirmDialog.tsx`
- [ ] Create `src/components/PageHeader.tsx`
- [ ] Create form components:
  - `src/components/forms/FormField.tsx`
  - `src/components/forms/FormSelect.tsx`
  - `src/components/forms/FormInput.tsx`

**Additional shadcn/ui components to install**:
```bash
npx shadcn-ui@latest add alert
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add sheet
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add checkbox
npx shadcn-ui@latest add calendar
```

---

## 🎯 Phase 2: Core CRUD Pages (8-10 hours)
**Priority: HIGH** | **Dependencies: Phase 1**

### 2.1 Setup Page (1.5 hours)
**Goal**: Configure days of week and periods

**Features**:
- Institution selection/creation
- Days of week management (add, edit, delete, reorder)
- Periods management (add, edit, delete with time validation)
- Visual timeline preview

**Files**:
- `src/pages/Setup.tsx`
- `src/components/setup/DaysList.tsx`
- `src/components/setup/PeriodsList.tsx`
- `src/components/setup/AddDayDialog.tsx`
- `src/components/setup/AddPeriodDialog.tsx`

---

### 2.2 Teachers Page (1.5 hours)
**Goal**: Full CRUD for teachers

**Features**:
- List all teachers with search/filter
- Add new teacher (form: first name, last name, email, code, color)
- Edit teacher (inline or modal)
- Delete teacher (with confirmation)
- Color picker for teacher color

**Files**:
- `src/pages/Teachers.tsx`
- `src/components/teachers/TeacherForm.tsx`
- `src/components/teachers/TeacherCard.tsx` (optional grid view)

**API Integration**:
- GET `/api/institutions/{id}/teachers`
- POST `/api/institutions/{id}/teachers`
- PUT `/api/institutions/{id}/teachers/{teacher_id}`
- DELETE `/api/institutions/{id}/teachers/{teacher_id}`

---

### 2.3 Rooms Page (2 hours)
**Goal**: Manage buildings and rooms hierarchically

**Features**:
- Left panel: Buildings list
- Right panel: Rooms in selected building
- Add/edit/delete buildings
- Add/edit/delete rooms (with capacity)
- Room type selection
- Building floor plan view (optional)

**Files**:
- `src/pages/Rooms.tsx`
- `src/components/rooms/BuildingsList.tsx`
- `src/components/rooms/RoomsList.tsx`
- `src/components/rooms/BuildingForm.tsx`
- `src/components/rooms/RoomForm.tsx`

**Layout**: Split view (buildings | rooms)

---

### 2.4 Subjects Page (1 hour)
**Goal**: Manage subjects and tags

**Features**:
- Subjects list with color coding
- Add/edit/delete subjects
- Activity tags management
- Color picker for visual distinction

**Files**:
- `src/pages/Subjects.tsx`
- `src/components/subjects/SubjectForm.tsx`

---

### 2.5 Students Page (2-3 hours)
**Goal**: Manage 3-level student hierarchy (Years → Groups → Subgroups)

**Features**:
- Expandable tree view:
  - Year (e.g., "Grade 10")
    - Group (e.g., "10A")
      - Subgroup (e.g., "10A Lab Group 1")
- Add/edit/delete at each level
- Student count tracking
- Drag-to-reorder (optional)

**Files**:
- `src/pages/Students.tsx`
- `src/components/students/StudentTree.tsx`
- `src/components/students/YearNode.tsx`
- `src/components/students/GroupNode.tsx`
- `src/components/students/SubgroupNode.tsx`
- `src/components/students/AddYearDialog.tsx`
- `src/components/students/AddGroupDialog.tsx`
- `src/components/students/AddSubgroupDialog.tsx`

**Complexity**: High - nested state management

---

## 🎯 Phase 3: Activities & Constraints (6-8 hours)
**Priority: HIGH** | **Dependencies: Phase 2 (need teachers, rooms, students, subjects)**

### 3.1 Activities Page (3-4 hours)
**Goal**: Create and manage activities with all relationships

**Features**:
- Activities list with filters (by subject, teacher, group)
- Add activity wizard:
  - Step 1: Basic info (name, subject, duration, split count)
  - Step 2: Assign teachers (multi-select)
  - Step 3: Assign student groups/subgroups (tree selector)
  - Step 4: Preferred rooms (multi-select with priority)
  - Step 5: Tags (optional)
- Edit activity (all relationships)
- Delete activity
- Duplicate activity
- Activity card showing all relationships

**Files**:
- `src/pages/Activities.tsx`
- `src/components/activities/ActivityList.tsx`
- `src/components/activities/ActivityCard.tsx`
- `src/components/activities/ActivityWizard.tsx`
- `src/components/activities/TeacherSelector.tsx`
- `src/components/activities/StudentSelector.tsx`
- `src/components/activities/RoomSelector.tsx`

**Complexity**: Very High - complex relationships

---

### 3.2 Constraints Page (3-4 hours)
**Goal**: Configure all constraint types

**Features**:
- Tabbed interface for constraint categories:
  - **Teacher Constraints**
  - **Student Constraints**
  - **Activity Constraints**
  - **Room Constraints**
- For each tab, list existing constraints
- Add/edit/delete constraints
- Weight sliders for soft constraints
- Visual constraint builder (e.g., time slot selector for "not available")

**Files**:
- `src/pages/Constraints.tsx`
- `src/components/constraints/ConstraintTabs.tsx`
- `src/components/constraints/TeacherConstraints.tsx`
- `src/components/constraints/StudentConstraints.tsx`
- `src/components/constraints/ActivityConstraints.tsx`
- `src/components/constraints/RoomConstraints.tsx`
- `src/components/constraints/TimeSlotPicker.tsx` (grid selector)
- `src/components/constraints/ConstraintForm.tsx` (generic)

**UI Pattern**: Calendar-style grid for time slot selection

---

## 🎯 Phase 4: Solve & Timetable Viewer (6-8 hours)
**Priority: CRITICAL** | **Dependencies: All data entry complete**

### 4.1 Solve Page (2-3 hours)
**Goal**: Initiate timetable generation and track progress

**Features**:
- Pre-solve validation:
  - Check if all activities have teachers
  - Check if rooms are sufficient
  - Warn about potential conflicts
- Solve configuration:
  - Time limit slider (10s - 1 hour)
  - Advanced settings (optional)
- Start solve button
- Real-time progress tracking:
  - Status (pending → running → completed/failed)
  - Time elapsed
  - Solutions found (if available)
  - Current objective value
- View results button → redirect to Timetable page
- Solve history (past jobs with status)

**Files**:
- `src/pages/Solve.tsx`
- `src/components/solve/SolveConfig.tsx`
- `src/components/solve/SolveProgress.tsx`
- `src/components/solve/SolveHistory.tsx`
- `src/components/solve/ValidationResults.tsx`

**API Integration**:
- POST `/api/institutions/{id}/solve`
- GET `/api/institutions/{id}/solve-jobs/{job_id}` (polling every 2s)
- GET `/api/institutions/{id}/solve-jobs`

---

### 4.2 Timetable Viewer (4-5 hours)
**Goal**: Display generated timetable in multiple views

**Features**:
- View selector:
  - **By Teacher**: Each teacher's weekly schedule
  - **By Room**: Each room's weekly schedule
  - **By Class**: Each student group's schedule
  - **Master Grid**: All activities on one grid
- Weekly grid layout:
  - Columns: Days (Monday - Friday)
  - Rows: Periods (Period 1 - Period 8)
  - Cells: Activity cards with:
    - Subject name
    - Teacher name(s)
    - Room name
    - Student group(s)
    - Color coding by subject
- Filters:
  - Select specific teacher/room/class
  - Filter by day
- Export buttons:
  - Print view
  - Export to CSV (future)
  - Export to PDF (future)

**Files**:
- `src/pages/Timetable.tsx`
- `src/components/timetable/ViewSelector.tsx`
- `src/components/timetable/TimetableGrid.tsx`
- `src/components/timetable/ActivityCell.tsx`
- `src/components/timetable/FilterPanel.tsx`
- `src/components/timetable/ExportButtons.tsx`

**Data Structure**:
```typescript
type Assignment = {
  activity_id: number;
  activity_name: string;
  day_id: number;
  day_name: string;
  period_id: number;
  period_name: string;
  room_id: number;
  room_name: string;
};
```

**Complexity**: High - complex grid layout and filtering

---

### 4.3 Dashboard (1 hour)
**Goal**: Overview page with statistics and quick actions

**Features**:
- Statistics cards:
  - Total teachers, rooms, subjects
  - Total activities
  - Constraints count
  - Last solve status
- Quick actions:
  - "Quick Solve" button
  - "View Last Timetable"
  - "Add Activity"
- Recent activity feed
- System status (backend health)

**Files**:
- `src/pages/Dashboard.tsx`
- `src/components/dashboard/StatCard.tsx`
- `src/components/dashboard/QuickActions.tsx`

---

## 🎯 Phase 5: Export Functionality (3-4 hours)
**Priority: MEDIUM** | **Dependencies: Timetable viewer**

### 5.1 Backend Export Endpoints (1.5-2 hours)
**Goal**: Generate downloadable files

**Tasks**:
- [ ] Create `backend/app/api/routes/export.py`
- [ ] Implement CSV export:
  - `GET /api/institutions/{id}/export/csv?view=teacher&filter=all`
  - Returns CSV file
- [ ] Implement PDF export (optional):
  - Install `reportlab` or `weasyprint`
  - Generate PDF from HTML template
  - `GET /api/institutions/{id}/export/pdf?view=teacher&filter=all`
- [ ] Implement Excel export (optional):
  - Install `openpyxl`
  - Generate .xlsx file
  - `GET /api/institutions/{id}/export/excel?view=teacher&filter=all`

**Files**:
- `backend/app/api/routes/export.py`
- `backend/app/services/export_service.py`
- `backend/app/templates/timetable.html` (for PDF)

---

### 5.2 Frontend Export Integration (1-2 hours)
**Goal**: Download buttons in timetable viewer

**Tasks**:
- [ ] Add export buttons to timetable viewer
- [ ] Implement download logic (trigger browser download)
- [ ] Add loading states during export
- [ ] Add export format selector (CSV/PDF/Excel)

**Files**:
- Update `src/components/timetable/ExportButtons.tsx`
- Add `src/services/exportService.ts`

---

## 🎯 Phase 6: Testing & Quality (6-8 hours)
**Priority: MEDIUM** | **Dependencies: All features complete**

### 6.1 Backend Unit Tests (3-4 hours)
**Goal**: Test core business logic

**Tasks**:
- [ ] Install test dependencies (already in requirements.txt)
- [ ] Create test database setup
- [ ] Write tests for services:
  - `tests/test_institution_service.py`
  - `tests/test_activity_service.py`
  - `tests/test_constraint_service.py`
- [ ] Write tests for solver:
  - `tests/test_data_loader.py`
  - `tests/test_timetable_solver.py`
- [ ] Write API endpoint tests:
  - `tests/test_api_teachers.py`
  - `tests/test_api_activities.py`
  - `tests/test_api_solve.py`
- [ ] Run coverage report: `pytest --cov=app tests/`

**Target**: 70%+ code coverage

---

### 6.2 Frontend E2E Tests (3-4 hours)
**Goal**: Test user workflows

**Tasks**:
- [ ] Install Playwright: `npm install -D @playwright/test`
- [ ] Create test scenarios:
  - `tests/e2e/setup.spec.ts` - Setup days & periods
  - `tests/e2e/teachers.spec.ts` - CRUD teachers
  - `tests/e2e/activities.spec.ts` - Create activity
  - `tests/e2e/solve.spec.ts` - Full solve workflow
- [ ] Configure CI/CD (GitHub Actions)

**Files**:
- `playwright.config.ts`
- `tests/e2e/*.spec.ts`

---

## 🎯 Phase 7: Polish & Documentation (4-6 hours)
**Priority: LOW** | **Dependencies: All features complete**

### 7.1 UI/UX Improvements (2-3 hours)
**Tasks**:
- [ ] Add loading skeletons
- [ ] Improve error messages
- [ ] Add empty states (e.g., "No teachers yet")
- [ ] Add tooltips for complex features
- [ ] Responsive design fixes
- [ ] Dark mode support (optional)
- [ ] Keyboard shortcuts (optional)

---

### 7.2 Documentation (2-3 hours)
**Tasks**:
- [ ] API documentation improvements
- [ ] User guide (how to use the system)
- [ ] Developer guide (how to extend)
- [ ] Deployment guide (production setup)
- [ ] Video walkthrough (optional)
- [ ] Screenshots for README

**Files**:
- `docs/USER_GUIDE.md`
- `docs/DEVELOPER_GUIDE.md`
- `docs/DEPLOYMENT.md`
- Update `README.md` with screenshots

---

## 🎯 Phase 8: Deployment Preparation (2-3 hours)
**Priority: LOW** | **Dependencies: Testing complete**

### 8.1 Production Configuration (1-2 hours)
**Tasks**:
- [ ] Create production Dockerfile (multi-stage build)
- [ ] Create production docker-compose.yml
- [ ] Add Nginx reverse proxy
- [ ] Add SSL/TLS configuration
- [ ] Environment variable validation
- [ ] Database backup scripts
- [ ] Monitoring setup (optional)

**Files**:
- `docker-compose.prod.yml`
- `nginx/nginx.conf`
- `scripts/backup.sh`

---

### 8.2 CI/CD Pipeline (1 hour)
**Tasks**:
- [ ] Create GitHub Actions workflow:
  - Run tests on PR
  - Build Docker images
  - Deploy to staging (optional)
- [ ] Add deployment script

**Files**:
- `.github/workflows/ci.yml`
- `.github/workflows/deploy.yml`

---

## 📊 Total Time Estimate

| Phase | Time Estimate | Priority |
|-------|---------------|----------|
| Phase 1: Frontend Foundation | 3-5 hours | CRITICAL |
| Phase 2: Core CRUD Pages | 8-10 hours | HIGH |
| Phase 3: Activities & Constraints | 6-8 hours | HIGH |
| Phase 4: Solve & Timetable | 6-8 hours | CRITICAL |
| Phase 5: Export | 3-4 hours | MEDIUM |
| Phase 6: Testing | 6-8 hours | MEDIUM |
| Phase 7: Polish & Docs | 4-6 hours | LOW |
| Phase 8: Deployment | 2-3 hours | LOW |
| **TOTAL** | **38-52 hours** | |

---

## 🎯 Recommended Execution Order

### Week 1: Core Functionality (16-20 hours)
1. **Days 1-2**: Phase 1 (Frontend Foundation)
2. **Days 3-4**: Phase 2 (CRUD Pages)
3. **Days 5**: Phase 3.1 (Activities Page)

### Week 2: Advanced Features (14-18 hours)
4. **Days 6**: Phase 3.2 (Constraints Page)
5. **Days 7-8**: Phase 4 (Solve & Timetable Viewer)
6. **Days 9**: Phase 5 (Export)

### Week 3: Quality & Launch (8-14 hours)
7. **Days 10-11**: Phase 6 (Testing)
8. **Day 12**: Phase 7 (Polish & Docs)
9. **Day 13**: Phase 8 (Deployment)

**Total: 2-3 weeks of focused development**

---

## 🚀 Quick Wins (If Time is Limited)

### MVP Features (15-20 hours):
1. ✅ Setup page (days & periods)
2. ✅ Teachers CRUD
3. ✅ Rooms CRUD (simplified)
4. ✅ Subjects CRUD
5. ✅ Students CRUD (basic, no tree view)
6. ✅ Activities page (simplified)
7. ✅ Basic constraints (teacher not available only)
8. ✅ Solve page (basic)
9. ✅ Timetable viewer (one view only)

This gets you a **working demo** in 15-20 hours!

---

## 📚 Learning Resources

### For Frontend Development:
- React Query: https://tanstack.com/query/latest
- React Router: https://reactrouter.com/
- shadcn/ui: https://ui.shadcn.com/
- Tailwind CSS: https://tailwindcss.com/

### For Testing:
- Pytest: https://docs.pytest.org/
- Playwright: https://playwright.dev/

---

## 🎯 Success Criteria

### ✅ MVP Complete When:
- [ ] Can create institution and setup
- [ ] Can add teachers, rooms, subjects, students
- [ ] Can create activities with relationships
- [ ] Can add basic constraints
- [ ] Can solve and get a timetable
- [ ] Can view timetable in at least one format

### ✅ Full Product Complete When:
- [ ] All CRUD operations work
- [ ] All constraint types supported
- [ ] Multiple timetable views
- [ ] Export functionality
- [ ] 70%+ test coverage
- [ ] Documentation complete
- [ ] Production deployment ready

---

## 💡 Tips for Success

1. **Start with API client** - Everything depends on this
2. **Use React Query** - Makes data fetching much easier
3. **Reuse components** - Build generic form components early
4. **Test as you go** - Don't wait until the end
5. **Deploy early** - Get feedback on real environment
6. **Focus on UX** - Simple, intuitive UI > fancy features
7. **Ask for help** - If stuck on solver or complex features

---

## 🔥 Next Immediate Steps (Start Here!)

1. **Right now**: Install frontend dependencies
   ```bash
   cd /workspace/project/opentt/frontend
   npm install axios @tanstack/react-query react-router-dom
   ```

2. **Next**: Create API client structure
   ```bash
   mkdir -p src/lib src/services src/types
   touch src/lib/api.ts
   touch src/lib/queryClient.ts
   ```

3. **Then**: Start with Setup page (easiest to test)

Ready to continue? 🚀
