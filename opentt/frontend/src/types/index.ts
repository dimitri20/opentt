// Institution types
export interface Institution {
  id: number;
  name: string;
  slug: string;
  timezone: string;
  description: string | null;
  created_at: string;
  updated_at: string;
}

export interface InstitutionCreate {
  name: string;
  slug: string;
  timezone?: string;
  description?: string | null;
}

export interface InstitutionUpdate {
  name?: string;
  timezone?: string;
  description?: string | null;
}

// Academic Year
export interface AcademicYear {
  id: number;
  institution_id: number;
  name: string;
  start_year: number;
  end_year: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface AcademicYearCreate {
  name: string;
  start_year: number;
  end_year: number;
  is_active?: boolean;
}

// Day of Week
export interface DayOfWeek {
  id: number;
  institution_id: number;
  name: string;
  short_name: string;
  order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface DayOfWeekCreate {
  name: string;
  short_name: string;
  order: number;
  is_active?: boolean;
}

export interface DayOfWeekUpdate {
  name?: string;
  short_name?: string;
  order?: number;
  is_active?: boolean;
}

// Period
export interface Period {
  id: number;
  institution_id: number;
  name: string;
  start_time: string;
  end_time: string;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface PeriodCreate {
  name: string;
  start_time: string;
  end_time: string;
  order: number;
}

export interface PeriodUpdate {
  name?: string;
  start_time?: string;
  end_time?: string;
  order?: number;
}

// Building
export interface Building {
  id: number;
  institution_id: number;
  name: string;
  code: string | null;
  address: string | null;
  created_at: string;
  updated_at: string;
}

export interface BuildingCreate {
  name: string;
  code?: string | null;
  address?: string | null;
}

export interface BuildingUpdate {
  name?: string;
  code?: string | null;
  address?: string | null;
}

// Room
export interface Room {
  id: number;
  building_id: number;
  name: string;
  code: string | null;
  capacity: number;
  room_type: string | null;
  created_at: string;
  updated_at: string;
}

export interface RoomCreate {
  name: string;
  code?: string | null;
  capacity?: number;
  room_type?: string | null;
}

export interface RoomUpdate {
  name?: string;
  code?: string | null;
  capacity?: number;
  room_type?: string | null;
}

export interface BuildingWithRooms extends Building {
  rooms: Room[];
}

// Subject
export interface Subject {
  id: number;
  institution_id: number;
  name: string;
  code: string | null;
  color: string;
  created_at: string;
  updated_at: string;
}

export interface SubjectCreate {
  name: string;
  code?: string | null;
  color?: string;
}

export interface SubjectUpdate {
  name?: string;
  code?: string | null;
  color?: string;
}

// Activity Tag
export interface ActivityTag {
  id: number;
  institution_id: number;
  name: string;
  color: string;
  created_at: string;
  updated_at: string;
}

export interface ActivityTagCreate {
  name: string;
  color?: string;
}

// Teacher
export interface Teacher {
  id: number;
  institution_id: number;
  first_name: string;
  last_name: string;
  email: string | null;
  code: string | null;
  color: string;
  created_at: string;
  updated_at: string;
}

export interface TeacherCreate {
  first_name: string;
  last_name: string;
  email?: string | null;
  code?: string | null;
  color?: string;
}

export interface TeacherUpdate {
  first_name?: string;
  last_name?: string;
  email?: string | null;
  code?: string | null;
  color?: string;
}

// Student hierarchy
export interface StudentYear {
  id: number;
  institution_id: number;
  name: string;
  short_name: string;
  order: number;
  created_at: string;
  updated_at: string;
}

export interface StudentYearCreate {
  name: string;
  short_name: string;
  order: number;
}

export interface StudentGroup {
  id: number;
  year_id: number;
  name: string;
  short_name: string;
  student_count: number;
  created_at: string;
  updated_at: string;
}

export interface StudentGroupCreate {
  name: string;
  short_name: string;
  student_count?: number;
}

export interface StudentSubgroup {
  id: number;
  group_id: number;
  name: string;
  short_name: string;
  student_count: number;
  created_at: string;
  updated_at: string;
}

export interface StudentSubgroupCreate {
  name: string;
  short_name: string;
  student_count?: number;
}

export interface StudentGroupWithSubgroups extends StudentGroup {
  subgroups: StudentSubgroup[];
}

export interface StudentYearWithGroups extends StudentYear {
  groups: StudentGroupWithSubgroups[];
}

// Activity
export interface Activity {
  id: number;
  institution_id: number;
  subject_id: number;
  name: string;
  duration: number;
  split_count: number;
  total_student_count: number;
  requires_room: boolean;
  created_at: string;
  updated_at: string;
}

export interface ActivityCreate {
  subject_id: number;
  name: string;
  duration?: number;
  split_count?: number;
  total_student_count?: number;
  requires_room?: boolean;
  teacher_ids?: number[];
  group_ids?: number[];
  subgroup_ids?: number[];
  preferred_room_ids?: number[];
  tag_ids?: number[];
}

export interface ActivityUpdate {
  subject_id?: number;
  name?: string;
  duration?: number;
  split_count?: number;
  total_student_count?: number;
  requires_room?: boolean;
  teacher_ids?: number[];
  group_ids?: number[];
  subgroup_ids?: number[];
  preferred_room_ids?: number[];
  tag_ids?: number[];
}

export interface ActivityWithRelations extends Activity {
  subject: Subject | null;
  teachers: Teacher[];
  groups: StudentGroup[];
  subgroups: StudentSubgroup[];
  preferred_rooms: Room[];
  tags: ActivityTag[];
}

// Constraints (simplified for now - add more as needed)
export interface TeacherNotAvailable {
  id: number;
  teacher_id: number;
  day_id: number;
  period_id: number;
  is_hard: boolean;
  weight: number;
  created_at: string;
  updated_at: string;
}

export interface TeacherNotAvailableCreate {
  teacher_id: number;
  day_id: number;
  period_id: number;
  is_hard?: boolean;
  weight?: number;
}

export interface RoomNotAvailable {
  id: number;
  room_id: number;
  day_id: number;
  period_id: number;
  is_hard: boolean;
  weight: number;
  created_at: string;
  updated_at: string;
}

export interface RoomNotAvailableCreate {
  room_id: number;
  day_id: number;
  period_id: number;
  is_hard?: boolean;
  weight?: number;
}

// Solve Job
export interface SolveJob {
  id: number;
  institution_id: number;
  status: 'pending' | 'running' | 'completed' | 'failed';
  time_limit_seconds: number;
  solution: Assignment[] | null;
  statistics: Record<string, any> | null;
  error_message: string | null;
  objective_value: number | null;
  solve_time: number | null;
  created_at: string;
  updated_at: string;
}

export interface SolveJobCreate {
  time_limit_seconds?: number;
}

export interface Assignment {
  activity_id: number;
  activity_name: string;
  day_id: number;
  day_name: string;
  period_id: number;
  period_name: string;
  room_id: number | null;
  room_name: string | null;
}

// API Response types
export interface ApiError {
  detail: string | { field: string; message: string }[];
  error?: string;
}

export interface PaginationParams {
  skip?: number;
  limit?: number;
}
