import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, Loader2 } from 'lucide-react';
import { useInstitution } from '@/hooks/useInstitution';
import { dayOfWeekService, periodService } from '@/services';
import type { DayOfWeek, Period, DayOfWeekCreate, PeriodCreate } from '@/types';
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
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { useForm } from 'react-hook-form';

export default function Setup() {
  const { institutionId } = useInstitution();
  const queryClient = useQueryClient();

  // Fetch days
  const { data: days = [], isLoading: daysLoading } = useQuery({
    queryKey: ['days', institutionId],
    queryFn: () => dayOfWeekService.getAll(institutionId),
  });

  // Fetch periods
  const { data: periods = [], isLoading: periodsLoading } = useQuery({
    queryKey: ['periods', institutionId],
    queryFn: () => periodService.getAll(institutionId),
  });

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Institution Setup</h1>
        <p className="text-gray-600">
          Configure days of the week and time periods for your timetable
        </p>
      </div>

      <div className="grid gap-8">
        {/* Days Section */}
        <DaysSection
          days={days}
          isLoading={daysLoading}
          institutionId={institutionId}
          queryClient={queryClient}
        />

        {/* Periods Section */}
        <PeriodsSection
          periods={periods}
          isLoading={periodsLoading}
          institutionId={institutionId}
          queryClient={queryClient}
        />
      </div>
    </div>
  );
}

// Days Section Component
function DaysSection({
  days,
  isLoading,
  institutionId,
  queryClient,
}: {
  days: DayOfWeek[];
  isLoading: boolean;
  institutionId: number;
  queryClient: any;
}) {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingDay, setEditingDay] = useState<DayOfWeek | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [dayToDelete, setDayToDelete] = useState<DayOfWeek | null>(null);

  const form = useForm<DayOfWeekCreate>({
    defaultValues: {
      name: '',
      short_name: '',
      order: days.length,
      is_active: true,
    },
  });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (data: DayOfWeekCreate) =>
      dayOfWeekService.create(institutionId, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['days', institutionId]);
      setDialogOpen(false);
      form.reset();
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<DayOfWeekCreate> }) =>
      dayOfWeekService.update(institutionId, id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['days', institutionId]);
      setDialogOpen(false);
      setEditingDay(null);
      form.reset();
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => dayOfWeekService.delete(institutionId, id),
    onSuccess: () => {
      queryClient.invalidateQueries(['days', institutionId]);
      setDeleteDialogOpen(false);
      setDayToDelete(null);
    },
  });

  const handleOpenDialog = (day?: DayOfWeek) => {
    if (day) {
      setEditingDay(day);
      form.reset({
        name: day.name,
        short_name: day.short_name,
        order: day.order,
        is_active: day.is_active,
      });
    } else {
      setEditingDay(null);
      form.reset({
        name: '',
        short_name: '',
        order: days.length,
        is_active: true,
      });
    }
    setDialogOpen(true);
  };

  const handleSubmit = form.handleSubmit((data) => {
    if (editingDay) {
      updateMutation.mutate({ id: editingDay.id, data });
    } else {
      createMutation.mutate(data);
    }
  });

  const handleDelete = (day: DayOfWeek) => {
    setDayToDelete(day);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    if (dayToDelete) {
      deleteMutation.mutate(dayToDelete.id);
    }
  };

  return (
    <div className="bg-white rounded-lg border p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-xl font-semibold">Days of Week</h2>
          <p className="text-sm text-gray-500">Define which days are active</p>
        </div>
        <Button onClick={() => handleOpenDialog()}>
          <Plus className="w-4 h-4 mr-2" />
          Add Day
        </Button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
        </div>
      ) : days.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No days configured. Click "Add Day" to get started.
        </div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Order</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Short Name</TableHead>
              <TableHead>Status</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {days
              .sort((a, b) => a.order - b.order)
              .map((day) => (
                <TableRow key={day.id}>
                  <TableCell>{day.order + 1}</TableCell>
                  <TableCell className="font-medium">{day.name}</TableCell>
                  <TableCell>{day.short_name}</TableCell>
                  <TableCell>
                    <span
                      className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        day.is_active
                          ? 'bg-green-100 text-green-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}
                    >
                      {day.is_active ? 'Active' : 'Inactive'}
                    </span>
                  </TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleOpenDialog(day)}
                    >
                      <Pencil className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(day)}
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      )}

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingDay ? 'Edit Day' : 'Add Day'}</DialogTitle>
            <DialogDescription>
              {editingDay
                ? 'Update day information'
                : 'Add a new day to your schedule'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Name</Label>
                <Input
                  id="name"
                  placeholder="e.g., Monday"
                  {...form.register('name', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="short_name">Short Name</Label>
                <Input
                  id="short_name"
                  placeholder="e.g., Mon"
                  {...form.register('short_name', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="order">Order</Label>
                <Input
                  id="order"
                  type="number"
                  {...form.register('order', { valueAsNumber: true })}
                />
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
                ) : editingDay ? (
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
            <DialogTitle>Delete Day</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{dayToDelete?.name}"? This action
              cannot be undone.
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

// Periods Section Component
function PeriodsSection({
  periods,
  isLoading,
  institutionId,
  queryClient,
}: {
  periods: Period[];
  isLoading: boolean;
  institutionId: number;
  queryClient: any;
}) {
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingPeriod, setEditingPeriod] = useState<Period | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [periodToDelete, setPeriodToDelete] = useState<Period | null>(null);

  const form = useForm<PeriodCreate>({
    defaultValues: {
      name: '',
      start_time: '',
      end_time: '',
      order: periods.length,
    },
  });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (data: PeriodCreate) =>
      periodService.create(institutionId, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['periods', institutionId]);
      setDialogOpen(false);
      form.reset();
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<PeriodCreate> }) =>
      periodService.update(institutionId, id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['periods', institutionId]);
      setDialogOpen(false);
      setEditingPeriod(null);
      form.reset();
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: (id: number) => periodService.delete(institutionId, id),
    onSuccess: () => {
      queryClient.invalidateQueries(['periods', institutionId]);
      setDeleteDialogOpen(false);
      setPeriodToDelete(null);
    },
  });

  const handleOpenDialog = (period?: Period) => {
    if (period) {
      setEditingPeriod(period);
      form.reset({
        name: period.name,
        start_time: period.start_time,
        end_time: period.end_time,
        order: period.order,
      });
    } else {
      setEditingPeriod(null);
      form.reset({
        name: '',
        start_time: '',
        end_time: '',
        order: periods.length,
      });
    }
    setDialogOpen(true);
  };

  const handleSubmit = form.handleSubmit((data) => {
    if (editingPeriod) {
      updateMutation.mutate({ id: editingPeriod.id, data });
    } else {
      createMutation.mutate(data);
    }
  });

  const handleDelete = (period: Period) => {
    setPeriodToDelete(period);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    if (periodToDelete) {
      deleteMutation.mutate(periodToDelete.id);
    }
  };

  return (
    <div className="bg-white rounded-lg border p-6">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-xl font-semibold">Time Periods</h2>
          <p className="text-sm text-gray-500">
            Define time slots for your timetable
          </p>
        </div>
        <Button onClick={() => handleOpenDialog()}>
          <Plus className="w-4 h-4 mr-2" />
          Add Period
        </Button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <Loader2 className="w-6 h-6 animate-spin text-gray-400" />
        </div>
      ) : periods.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No periods configured. Click "Add Period" to get started.
        </div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Order</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Start Time</TableHead>
              <TableHead>End Time</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {periods
              .sort((a, b) => a.order - b.order)
              .map((period) => (
                <TableRow key={period.id}>
                  <TableCell>{period.order + 1}</TableCell>
                  <TableCell className="font-medium">{period.name}</TableCell>
                  <TableCell>{period.start_time}</TableCell>
                  <TableCell>{period.end_time}</TableCell>
                  <TableCell className="text-right">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleOpenDialog(period)}
                    >
                      <Pencil className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDelete(period)}
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
          </TableBody>
        </Table>
      )}

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editingPeriod ? 'Edit Period' : 'Add Period'}
            </DialogTitle>
            <DialogDescription>
              {editingPeriod
                ? 'Update period information'
                : 'Add a new time period to your schedule'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="period_name">Name</Label>
                <Input
                  id="period_name"
                  placeholder="e.g., Period 1"
                  {...form.register('name', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="start_time">Start Time</Label>
                <Input
                  id="start_time"
                  type="time"
                  {...form.register('start_time', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="end_time">End Time</Label>
                <Input
                  id="end_time"
                  type="time"
                  {...form.register('end_time', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="period_order">Order</Label>
                <Input
                  id="period_order"
                  type="number"
                  {...form.register('order', { valueAsNumber: true })}
                />
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
                ) : editingPeriod ? (
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
            <DialogTitle>Delete Period</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{periodToDelete?.name}"? This
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
