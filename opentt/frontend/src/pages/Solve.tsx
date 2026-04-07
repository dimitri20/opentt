import { useState, useEffect } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { Play, Loader2, CheckCircle, XCircle, Clock, ArrowRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useInstitution } from '@/hooks/useInstitution';
import { solveService } from '@/services';
import type { SolveJob } from '@/types';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';

export default function Solve() {
  const { institutionId } = useInstitution();
  const navigate = useNavigate();
  const [timeLimitSeconds, setTimeLimitSeconds] = useState(60);
  const [currentJob, setCurrentJob] = useState<SolveJob | null>(null);
  const [polling, setPolling] = useState(false);

  // Get latest job
  const { data: jobs = [] } = useQuery({
    queryKey: ['solve-jobs', institutionId],
    queryFn: () => solveService.getJobs(institutionId),
    refetchInterval: polling ? 2000 : false, // Poll every 2s when solving
  });

  const latestJob = jobs[0];

  // Update currentJob when we get new data
  useEffect(() => {
    if (latestJob) {
      setCurrentJob(latestJob);
      
      // Stop polling if job is complete or failed
      if (latestJob.status === 'completed' || latestJob.status === 'failed') {
        setPolling(false);
      }
    }
  }, [latestJob]);

  // Start solve mutation
  const solveMutation = useMutation({
    mutationFn: () =>
      solveService.startSolve(institutionId, { time_limit_seconds: timeLimitSeconds }),
    onSuccess: (job) => {
      setCurrentJob(job);
      setPolling(true); // Start polling
    },
  });

  const handleSolve = () => {
    solveMutation.mutate();
  };

  const handleViewTimetable = () => {
    navigate('/timetable');
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
      case 'running':
        return <Loader2 className="w-5 h-5 animate-spin text-blue-500" />;
      case 'completed':
        return <CheckCircle className="w-5 h-5 text-green-500" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-500" />;
      default:
        return <Clock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-50 text-yellow-700 border-yellow-200';
      case 'running':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'completed':
        return 'bg-green-50 text-green-700 border-green-200';
      case 'failed':
        return 'bg-red-50 text-red-700 border-red-200';
      default:
        return 'bg-gray-50 text-gray-700 border-gray-200';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'pending':
        return 'Queued';
      case 'running':
        return 'Solving...';
      case 'completed':
        return 'Completed';
      case 'failed':
        return 'Failed';
      default:
        return 'Unknown';
    }
  };

  const isSolving = currentJob?.status === 'pending' || currentJob?.status === 'running';
  const isCompleted = currentJob?.status === 'completed';
  const isFailed = currentJob?.status === 'failed';

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Solve Timetable</h1>
        <p className="text-gray-600">
          Generate an optimized timetable using the OR-Tools CP-SAT solver
        </p>
      </div>

      <div className="grid gap-6">
        {/* Configuration Card */}
        <Card>
          <CardHeader>
            <CardTitle>Solver Configuration</CardTitle>
            <CardDescription>
              Configure the solver parameters before generating the timetable
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid gap-2">
              <Label htmlFor="timeLimit">Time Limit (seconds)</Label>
              <Input
                id="timeLimit"
                type="number"
                min="10"
                max="300"
                value={timeLimitSeconds}
                onChange={(e) => setTimeLimitSeconds(parseInt(e.target.value))}
                disabled={isSolving}
              />
              <p className="text-sm text-gray-500">
                Maximum time the solver will run. Recommended: 60-120 seconds.
              </p>
            </div>

            <div className="pt-4">
              <Button
                size="lg"
                onClick={handleSolve}
                disabled={isSolving || solveMutation.isPending}
                className="w-full"
              >
                {isSolving || solveMutation.isPending ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Solving Timetable...
                  </>
                ) : (
                  <>
                    <Play className="w-5 h-5 mr-2" />
                    Solve Timetable
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Status Card */}
        {currentJob && (
          <Card>
            <CardHeader>
              <CardTitle>Solve Status</CardTitle>
              <CardDescription>
                Current timetable generation progress
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Status Badge */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {getStatusIcon(currentJob.status)}
                  <div>
                    <div className="font-medium">
                      {getStatusText(currentJob.status)}
                    </div>
                    <div className="text-sm text-gray-500">
                      Job ID: {currentJob.id}
                    </div>
                  </div>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium border ${getStatusColor(
                    currentJob.status
                  )}`}
                >
                  {getStatusText(currentJob.status)}
                </span>
              </div>

              {/* Progress Info */}
              {isSolving && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-blue-700 mb-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span className="font-medium">
                      Optimizing your timetable...
                    </span>
                  </div>
                  <p className="text-sm text-blue-600">
                    This may take up to {timeLimitSeconds} seconds. The solver is
                    finding the best schedule while respecting all constraints.
                  </p>
                </div>
              )}

              {/* Success Message */}
              {isCompleted && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-green-700 mb-2">
                    <CheckCircle className="w-4 h-4" />
                    <span className="font-medium">Timetable Generated!</span>
                  </div>
                  <p className="text-sm text-green-600 mb-4">
                    Your optimized timetable has been successfully generated.
                  </p>
                  <Button
                    onClick={handleViewTimetable}
                    className="w-full bg-green-600 hover:bg-green-700"
                  >
                    View Timetable
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </div>
              )}

              {/* Error Message */}
              {isFailed && currentJob.error_message && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex items-center gap-2 text-red-700 mb-2">
                    <XCircle className="w-4 h-4" />
                    <span className="font-medium">Solve Failed</span>
                  </div>
                  <p className="text-sm text-red-600">{currentJob.error_message}</p>
                  <p className="text-sm text-red-500 mt-2">
                    Try adjusting your activities or increasing the time limit.
                  </p>
                </div>
              )}

              {/* Job Details */}
              {currentJob.result && (
                <div className="border rounded-lg p-4 space-y-2">
                  <h4 className="font-medium text-sm text-gray-700">Solver Results</h4>
                  <div className="grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <span className="text-gray-500">Status:</span>
                      <span className="ml-2 font-medium">
                        {currentJob.result.status || 'N/A'}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Solve Time:</span>
                      <span className="ml-2 font-medium">
                        {currentJob.result.solve_time
                          ? `${currentJob.result.solve_time.toFixed(2)}s`
                          : 'N/A'}
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-500">Assignments:</span>
                      <span className="ml-2 font-medium">
                        {currentJob.result.assignments?.length || 0}
                      </span>
                    </div>
                    {currentJob.result.conflicts !== undefined && (
                      <div>
                        <span className="text-gray-500">Conflicts:</span>
                        <span className="ml-2 font-medium">
                          {currentJob.result.conflicts}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Timestamps */}
              <div className="text-xs text-gray-500 space-y-1">
                <div>
                  Created: {new Date(currentJob.created_at).toLocaleString()}
                </div>
                {currentJob.started_at && (
                  <div>
                    Started: {new Date(currentJob.started_at).toLocaleString()}
                  </div>
                )}
                {currentJob.completed_at && (
                  <div>
                    Completed: {new Date(currentJob.completed_at).toLocaleString()}
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Help Card */}
        {!currentJob && (
          <Card>
            <CardHeader>
              <CardTitle>How It Works</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3 text-sm text-gray-600">
                <p>
                  The timetable solver uses Google's OR-Tools CP-SAT solver to generate
                  an optimized schedule that satisfies all your constraints:
                </p>
                <ul className="list-disc list-inside space-y-1 ml-2">
                  <li>No teacher/room/student conflicts</li>
                  <li>Respects teacher and student availability</li>
                  <li>Honors room capacity limits</li>
                  <li>Distributes activities evenly across the week</li>
                  <li>Optimizes for preferred time slots</li>
                </ul>
                <p className="pt-2">
                  Click "Solve Timetable" to generate your optimized schedule!
                </p>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
