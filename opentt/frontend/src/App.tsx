import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from '@/components/layout/Layout';
import Dashboard from '@/pages/Dashboard';
import Setup from '@/pages/Setup';
import Teachers from '@/pages/Teachers';
import Rooms from '@/pages/Rooms';
import Subjects from '@/pages/Subjects';
import Students from '@/pages/Students';
import Activities from '@/pages/Activities';
import Constraints from '@/pages/Constraints';
import Solve from '@/pages/Solve';
import Timetable from '@/pages/Timetable';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="setup" element={<Setup />} />
          <Route path="teachers" element={<Teachers />} />
          <Route path="rooms" element={<Rooms />} />
          <Route path="subjects" element={<Subjects />} />
          <Route path="students" element={<Students />} />
          <Route path="activities" element={<Activities />} />
          <Route path="constraints" element={<Constraints />} />
          <Route path="solve" element={<Solve />} />
          <Route path="timetable" element={<Timetable />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
