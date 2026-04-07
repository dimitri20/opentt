import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, Loader2, Search } from 'lucide-react';
import { useInstitution } from '@/hooks/useInstitution';
import {
  activityService,
  teacherService,
  subjectService,
  roomService,
  studentYearService,
} from '@/services';
import type { Activity, ActivityCreate } from '@/types';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { useForm, Controller } from 'react-hook-form';

export default function Activities() {
  const { institutionId } = useInstitution();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingActivity, setEditingActivity] = useState<Activity | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [activityToDelete, setActivityToDelete] = useState<Activity | null>(null);

  // Fetch all data
  const { data: activities = [], isLoading } = useQuery({
    queryKey: ['activities', institutionId],
    queryFn: () => activityService.getAll(institutionId),
  });

  const { data: teachers = [] } = useQuery({
    queryKey: ['teachers', institutionId],
    queryFn: () => teacherService.getAll(institutionId),
  });

  const { data: subjects = [] } = useQuery({
    queryKey: ['subjects', institutionId],
    queryFn: () => subjectService.getAll(institutionId),
  });

  const { data: rooms = [] } = useQuery({
    queryKey: ['rooms', institutionId],
    queryFn: () => roomService.getAll(institutionId),
  });

  const { data: years = [] } = useQuery({
    queryKey: ['student-years', institutionId],
    queryFn: () => studentYearService.getAll(institutionId),
  });

  const allGroups = years.flatMap((year) => year.groups || []);

  // Form
  const form = useForm<ActivityCreate & { teacher_id: number; student_group_id: number; room_id?: number }>({
    defaultValues: {
      name: '',
      subject_id: undefined,
      teacher_id: undefined,
      student_group_id: undefined,
      room_id: undefined,
      duration: 1,
      split_count: 1,
      requires_room: true,
    },
  });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (data: ActivityCreate & { teacher_id: number; student_group_id: number; room_id?: number }) => {
      const { teacher_id, student_group_id, room_id, ...activityData } = data;
      
      const payload: ActivityCreate = {
        ...activityData,
        teacher_ids: [teacher_id],
        student_group_ids: [student_group_id],
        ...(room_id && { preferred_room_ids: [room_id] }),
      };
      
      return activityService.create(institutionId, payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['activities', institutionId]);
      setDialogOpen(false);
      form.reset();
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ 
      id, 
      data 
    }: { 
      id: number; 
      data: ActivityCreate & { teacher_id: number; student_group_id: number; room_id?: number };
    }) => {
      const { teacher_id, student_group_id, room_id, ...activityData } = data;
      
      const payload: Partial<ActivityCreate> = {
        ...activityData,
        teacher_ids: [teacher_id],
        student_group_ids: [student_group_id],
        ...(room_id && { preferred_room_ids: [room_id] }),
      };
      
      return activityService.update(institutionId, id, payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['activities', institutionId]);
      setDialogOpen(false);
      setEditingActivity(null);
      form.reset();
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => activityService.delete(institutionId, id),
    onSuccess: () => {
      queryClient.invalidateQueries(['activities', institutionId]);
      setDeleteDialogOpen(false);
      setActivityToDelete(null);
    },
  });

  const handleOpenDialog = (activity?: Activity) => {
    if (activity) {
      setEditingActivity(activity);
      form.reset({
        name: activity.name,
        subject_id: activity.subject_id,
        teacher_id: activity.teachers?.[0]?.id,
        student_group_id: activity.student_groups?.[0]?.id,
        room_id: activity.preferred_rooms?.[0]?.id,
        duration: activity.duration,
        split_count: activity.split_count,
        requires_room: activity.requires_room,
      });
    } else {
      setEditingActivity(null);
      form.reset({
        name: '',
        subject_id: undefined,
        teacher_id: undefined,
        student_group_id: undefined,
        room_id: undefined,
        duration: 1,
        split_count: 1,
        requires_room: true,
      });
    }
    setDialogOpen(true);
  };

  const handleSubmit = form.handleSubmit((data) => {
    if (editingActivity) {
      updateMutation.mutate({ id: editingActivity.id, data });
    } else {
      createMutation.mutate(data);
    }
  });

  const handleDelete = (activity: Activity) => {
    setActivityToDelete(activity);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    if (activityToDelete) {
      deleteMutation.mutate(activityToDelete.id);
    }
  };

  // Filter activities
  const filteredActivities = activities.filter((activity) => {
    const searchLower = searchQuery.toLowerCase();
    return (
      activity.name.toLowerCase().includes(searchLower) ||
      activity.subject?.name.toLowerCase().includes(searchLower) ||
      activity.teachers?.[0]?.first_name.toLowerCase().includes(searchLower) ||
      activity.teachers?.[0]?.last_name.toLowerCase().includes(searchLower)
    );
  });

  // Helper to get subject for display
  const getSubject = (subjectId: number) => 
    subjects.find(s => s.id === subjectId);

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Activities</h1>
        <p className="text-gray-600">
          Create teaching activities by combining teachers, subjects, and student groups
        </p>
      </div>

      <div className="bg-white rounded-lg border">
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between gap-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              placeholder="Search activities..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9"
            />
          </div>
          <Button onClick={() => handleOpenDialog()}>
            <Plus className="w-4 h-4 mr-2" />
            Add Activity
          </Button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
            </div>
          ) : filteredActivities.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              {searchQuery ? (
                <>No activities found matching "{searchQuery}"</>
              ) : (
                <>
                  No activities yet. Click "Add Activity" to create teaching sessions.
                </>
              )}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Activity</TableHead>
                  <TableHead>Subject</TableHead>
                  <TableHead>Teacher</TableHead>
                  <TableHead>Student Group</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredActivities.map((activity) => {
                  const subject = getSubject(activity.subject_id);
                  return (
                    <TableRow key={activity.id}>
                      <TableCell className="font-medium">
                        {activity.name}
                      </TableCell>
                      <TableCell>
                        {subject && (
                          <div className="flex items-center gap-2">
                            <div
                              className="w-4 h-4 rounded"
                              style={{ backgroundColor: subject.color }}
                            />
                            <span>{subject.name}</span>
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        {activity.teachers?.[0] ? (
                          <span>
                            {activity.teachers[0].first_name}{' '}
                            {activity.teachers[0].last_name}
                          </span>
                        ) : (
                          <span className="text-gray-400">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        {activity.student_groups?.[0] ? (
                          <span className="inline-flex items-center px-2 py-1 rounded text-xs bg-blue-50 text-blue-700">
                            {activity.student_groups[0].short_name}
                          </span>
                        ) : (
                          <span className="text-gray-400">-</span>
                        )}
                      </TableCell>
                      <TableCell>
                        <span className="text-sm">
                          {activity.duration} period{activity.duration !== 1 ? 's' : ''}
                        </span>
                      </TableCell>
                      <TableCell className="text-right">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleOpenDialog(activity)}
                        >
                          <Pencil className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(activity)}
                        >
                          <Trash2 className="w-4 h-4 text-red-500" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          )}
        </div>

        {/* Footer */}
        {!isLoading && filteredActivities.length > 0 && (
          <div className="p-4 border-t text-sm text-gray-600">
            Showing {filteredActivities.length} of {activities.length} activit
            {activities.length !== 1 ? 'ies' : 'y'} • Total periods needed:{' '}
            {activities.reduce((sum, act) => sum + act.duration, 0)}
          </div>
        )}
      </div>

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingActivity ? 'Edit Activity' : 'Add Activity'}
            </DialogTitle>
            <DialogDescription>
              {editingActivity
                ? 'Update activity information'
                : 'Create a new teaching activity'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4 max-h-[60vh] overflow-y-auto">
              <div className="grid gap-2">
                <Label htmlFor="name">Activity Name *</Label>
                <Input
                  id="name"
                  placeholder="e.g., Math Lesson, Physics Lab"
                  {...form.register('name', { required: true })}
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="subject">Subject *</Label>
                <Controller
                  name="subject_id"
                  control={form.control}
                  rules={{ required: true }}
                  render={({ field }) => (
                    <Select
                      value={field.value?.toString()}
                      onValueChange={(val) => field.onChange(parseInt(val))}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select a subject" />
                      </SelectTrigger>
                      <SelectContent>
                        {subjects.map((subject) => (
                          <SelectItem key={subject.id} value={subject.id.toString()}>
                            <div className="flex items-center gap-2">
                              <div
                                className="w-3 h-3 rounded"
                                style={{ backgroundColor: subject.color }}
                              />
                              {subject.name}
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="teacher">Teacher *</Label>
                <Controller
                  name="teacher_id"
                  control={form.control}
                  rules={{ required: true }}
                  render={({ field }) => (
                    <Select
                      value={field.value?.toString()}
                      onValueChange={(val) => field.onChange(parseInt(val))}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select a teacher" />
                      </SelectTrigger>
                      <SelectContent>
                        {teachers.map((teacher) => (
                          <SelectItem key={teacher.id} value={teacher.id.toString()}>
                            {teacher.first_name} {teacher.last_name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="student_group">Student Group *</Label>
                <Controller
                  name="student_group_id"
                  control={form.control}
                  rules={{ required: true }}
                  render={({ field }) => (
                    <Select
                      value={field.value?.toString()}
                      onValueChange={(val) => field.onChange(parseInt(val))}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select a student group" />
                      </SelectTrigger>
                      <SelectContent>
                        {allGroups.map((group) => (
                          <SelectItem key={group.id} value={group.id.toString()}>
                            {group.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>

              <div className="grid gap-2">
                <Label htmlFor="room">Preferred Room (Optional)</Label>
                <Controller
                  name="room_id"
                  control={form.control}
                  render={({ field }) => (
                    <Select
                      value={field.value?.toString() || 'none'}
                      onValueChange={(val) => 
                        field.onChange(val === 'none' ? undefined : parseInt(val))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select a room (optional)" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="none">No preference</SelectItem>
                        {rooms.map((room) => (
                          <SelectItem key={room.id} value={room.id.toString()}>
                            {room.name} (Capacity: {room.capacity})
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  )}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="grid gap-2">
                  <Label htmlFor="duration">Duration (periods) *</Label>
                  <Input
                    id="duration"
                    type="number"
                    min="1"
                    {...form.register('duration', {
                      required: true,
                      valueAsNumber: true,
                      min: 1,
                    })}
                  />
                </div>

                <div className="grid gap-2">
                  <Label htmlFor="split_count">Times per Week *</Label>
                  <Input
                    id="split_count"
                    type="number"
                    min="1"
                    {...form.register('split_count', {
                      required: true,
                      valueAsNumber: true,
                      min: 1,
                    })}
                  />
                </div>
              </div>
            </div>
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setDialogOpen(false)}
              >
                Cancel
              </Button>
              <Button
                type="submit"
                disabled={createMutation.isPending || updateMutation.isPending}
              >
                {createMutation.isPending || updateMutation.isPending ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : editingActivity ? (
                  'Update'
                ) : (
                  'Create'
                )}
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Activity</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{activityToDelete?.name}"? This
              action cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setDeleteDialogOpen(false)}
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={confirmDelete}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Deleting...
                </>
              ) : (
                'Delete'
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
