import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Calendar, Loader2, AlertCircle, Users, MapPin, User } from 'lucide-react';
import { useInstitution } from '@/hooks/useInstitution';
import { solveService, dayOfWeekService, periodService, subjectService } from '@/services';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';

export default function Timetable() {
  const { institutionId } = useInstitution();

  // Fetch configuration
  const { data: days = [] } = useQuery({
    queryKey: ['days', institutionId],
    queryFn: () => dayOfWeekService.getAll(institutionId),
  });

  const { data: periods = [] } = useQuery({
    queryKey: ['periods', institutionId],
    queryFn: () => periodService.getAll(institutionId),
  });

  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects', institutionId],
    queryFn: () => subjectService.getAll(institutionId),
  });

  // Fetch latest timetable
  const { data: jobs = [], isLoading } = useQuery({
    queryKey: ['solve-jobs', institutionId],
    queryFn: () => solveService.getJobs(institutionId),
  });

  const latestJob = jobs[0];
  const timetable = latestJob?.result;

  // Sort days and periods
  const sortedDays = [...days].sort((a, b) => a.order - b.order).filter(d => d.is_active);
  const sortedPeriods = [...periods].sort((a, b) => a.order - b.order);

  // Build assignment lookup: [day_id][period_id] = [assignments]
  const assignmentMap: Record<number, Record<number, any[]>> = {};
  
  if (timetable?.assignments) {
    timetable.assignments.forEach((assignment: any) => {
      const dayId = assignment.day_of_week_id;
      const periodId = assignment.period_id;
      
      if (!assignmentMap[dayId]) {
        assignmentMap[dayId] = {};
      }
      if (!assignmentMap[dayId][periodId]) {
        assignmentMap[dayId][periodId] = [];
      }
      assignmentMap[dayId][periodId].push(assignment);
    });
  }

  // Get subject by ID
  const getSubject = (subjectId: number) => subjects.find(s => s.id === subjectId);

  // Render cell content
  const renderCell = (dayId: number, periodId: number) => {
    const assignments = assignmentMap[dayId]?.[periodId] || [];
    
    if (assignments.length === 0) {
      return (
        <div className="h-full flex items-center justify-center text-gray-300">
          <span className="text-xs">—</span>
        </div>
      );
    }

    return (
      <div className="space-y-1">
        {assignments.map((assignment: any, idx: number) => {
          const subject = getSubject(assignment.activity.subject_id);
          const activity = assignment.activity;
          
          return (
            <Card
              key={idx}
              className="border-l-4 hover:shadow-md transition-shadow"
              style={{
                borderLeftColor: subject?.color || '#6B7280',
                backgroundColor: subject ? `${subject.color}10` : '#F3F4F6',
              }}
            >
              <CardContent className="p-2 space-y-1">
                <div
                  className="font-semibold text-sm truncate"
                  style={{ color: subject?.color || '#374151' }}
                >
                  {subject?.name || 'Unknown Subject'}
                </div>
                
                <div className="flex items-center gap-1 text-xs text-gray-600">
                  <User className="w-3 h-3" />
                  <span className="truncate">
                    {activity.teachers?.[0]
                      ? `${activity.teachers[0].first_name} ${activity.teachers[0].last_name}`
                      : 'No teacher'}
                  </span>
                </div>

                {assignment.room && (
                  <div className="flex items-center gap-1 text-xs text-gray-600">
                    <MapPin className="w-3 h-3" />
                    <span className="truncate">{assignment.room.name}</span>
                  </div>
                )}

                <div className="flex items-center gap-1 text-xs text-gray-600">
                  <Users className="w-3 h-3" />
                  <span className="truncate">
                    {activity.student_groups?.[0]?.short_name || 'No group'}
                  </span>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    );
  };

  if (isLoading) {
    return (
      <div className="p-6 flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <Loader2 className="w-8 h-8 animate-spin text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600">Loading timetable...</p>
        </div>
      </div>
    );
  }

  if (!latestJob) {
    return (
      <div className="p-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">Timetable</h1>
          <p className="text-gray-600">View your generated timetable</p>
        </div>
        
        <Card className="border-amber-200 bg-amber-50">
          <CardContent className="p-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-amber-900 mb-1">No Timetable Generated</h3>
                <p className="text-sm text-amber-700 mb-4">
                  You haven't generated a timetable yet. Go to the Solve page to create one.
                </p>
                <Button
                  onClick={() => (window.location.href = '/solve')}
                  className="bg-amber-600 hover:bg-amber-700"
                >
                  <Calendar className="w-4 h-4 mr-2" />
                  Generate Timetable
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (latestJob.status !== 'completed' || !timetable) {
    return (
      <div className="p-6">
        <div className="mb-6">
          <h1 className="text-3xl font-bold mb-2">Timetable</h1>
          <p className="text-gray-600">View your generated timetable</p>
        </div>
        
        <Card className="border-blue-200 bg-blue-50">
          <CardContent className="p-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-blue-900 mb-1">
                  {latestJob.status === 'running' || latestJob.status === 'pending'
                    ? 'Timetable Generation in Progress'
                    : 'Timetable Generation Failed'}
                </h3>
                <p className="text-sm text-blue-700 mb-4">
                  {latestJob.status === 'running' || latestJob.status === 'pending'
                    ? 'Your timetable is currently being generated. Please wait...'
                    : 'The timetable generation failed. Please try again.'}
                </p>
                <Button
                  onClick={() => (window.location.href = '/solve')}
                  className="bg-blue-600 hover:bg-blue-700"
                >
                  Go to Solve Page
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Timetable</h1>
        <p className="text-gray-600">
          Generated timetable with {timetable.assignments?.length || 0} activities scheduled
        </p>
      </div>

      {sortedDays.length === 0 || sortedPeriods.length === 0 ? (
        <Card className="border-amber-200 bg-amber-50">
          <CardContent className="p-6">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600 mt-0.5" />
              <div>
                <h3 className="font-medium text-amber-900 mb-1">Configuration Missing</h3>
                <p className="text-sm text-amber-700">
                  Please configure days and periods in the Setup page before viewing the timetable.
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : (
        <div className="bg-white rounded-lg border overflow-x-auto">
          {/* Stats bar */}
          <div className="p-4 border-b bg-gray-50">
            <div className="flex items-center gap-6 text-sm">
              <div>
                <span className="text-gray-500">Status:</span>
                <span className="ml-2 font-medium text-green-600">Completed</span>
              </div>
              <div>
                <span className="text-gray-500">Solve Time:</span>
                <span className="ml-2 font-medium">
                  {timetable.solve_time ? `${timetable.solve_time.toFixed(2)}s` : 'N/A'}
                </span>
              </div>
              <div>
                <span className="text-gray-500">Activities:</span>
                <span className="ml-2 font-medium">{timetable.assignments?.length || 0}</span>
              </div>
              <div>
                <span className="text-gray-500">Conflicts:</span>
                <span className="ml-2 font-medium">
                  {timetable.conflicts !== undefined ? timetable.conflicts : 'N/A'}
                </span>
              </div>
            </div>
          </div>

          {/* Timetable Grid */}
          <div className="p-4">
            <div className="grid gap-2" style={{ 
              gridTemplateColumns: `120px repeat(${sortedDays.length}, minmax(200px, 1fr))` 
            }}>
              {/* Header Row */}
              <div className="font-medium text-gray-500 text-sm flex items-center justify-center sticky left-0 bg-white z-10">
                Time / Day
              </div>
              {sortedDays.map((day) => (
                <div
                  key={day.id}
                  className="font-semibold text-center py-2 px-3 bg-gray-50 rounded-lg"
                >
                  <div className="text-sm">{day.name}</div>
                  <div className="text-xs text-gray-500">{day.short_name}</div>
                </div>
              ))}

              {/* Period Rows */}
              {sortedPeriods.map((period) => (
                <div key={period.id} className="contents">
                  {/* Period Label */}
                  <div className="sticky left-0 bg-white z-10 border-r">
                    <div className="py-2 px-3 text-sm">
                      <div className="font-medium text-gray-700">{period.name}</div>
                      <div className="text-xs text-gray-500">
                        {period.start_time} - {period.end_time}
                      </div>
                    </div>
                  </div>

                  {/* Day Cells */}
                  {sortedDays.map((day) => (
                    <div
                      key={`${day.id}-${period.id}`}
                      className="border rounded-lg p-2 min-h-[100px] bg-gray-50/30"
                    >
                      {renderCell(day.id, period.id)}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>

          {/* Legend */}
          <div className="p-4 border-t bg-gray-50">
            <h4 className="text-sm font-medium text-gray-700 mb-2">Legend</h4>
            <div className="flex flex-wrap gap-4 text-xs text-gray-600">
              <div className="flex items-center gap-1">
                <User className="w-3 h-3" />
                <span>Teacher</span>
              </div>
              <div className="flex items-center gap-1">
                <MapPin className="w-3 h-3" />
                <span>Room</span>
              </div>
              <div className="flex items-center gap-1">
                <Users className="w-3 h-3" />
                <span>Student Group</span>
              </div>
              <div className="ml-4 flex items-center gap-2">
                <div className="flex items-center gap-1">
                  <div className="w-3 h-3 rounded border-l-4" style={{ borderLeftColor: '#10B981', backgroundColor: '#10B98110' }} />
                  <span>Color = Subject</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
