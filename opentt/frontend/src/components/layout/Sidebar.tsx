import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Settings,
  Users,
  Building2,
  BookOpen,
  GraduationCap,
  CalendarDays,
  ListChecks,
  Play,
  Calendar,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/setup', label: 'Setup', icon: Settings },
  { to: '/teachers', label: 'Teachers', icon: Users },
  { to: '/rooms', label: 'Rooms', icon: Building2 },
  { to: '/subjects', label: 'Subjects', icon: BookOpen },
  { to: '/students', label: 'Students', icon: GraduationCap },
  { to: '/activities', label: 'Activities', icon: CalendarDays },
  { to: '/constraints', label: 'Constraints', icon: ListChecks },
  { to: '/solve', label: 'Solve', icon: Play },
  { to: '/timetable', label: 'Timetable', icon: Calendar },
];

export default function Sidebar() {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-gray-200">
        <h1 className="text-2xl font-bold text-blue-600">OpenTT</h1>
        <p className="text-sm text-gray-500 mt-1">Timetable System</p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors',
                isActive
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-100'
              )
            }
          >
            <Icon className="w-5 h-5" />
            {label}
          </NavLink>
        ))}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-gray-200">
        <div className="text-xs text-gray-500 text-center">
          OpenTT v1.0.0
        </div>
      </div>
    </aside>
  );
}
