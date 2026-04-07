import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, Loader2, Search, Users } from 'lucide-react';
import { useInstitution } from '@/hooks/useInstitution';
import { studentYearService, studentGroupService } from '@/services';
import type { StudentYear, StudentGroup, StudentGroupCreate } from '@/types';
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

export default function Students() {
  const { institutionId } = useInstitution();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingGroup, setEditingGroup] = useState<StudentGroup | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [groupToDelete, setGroupToDelete] = useState<StudentGroup | null>(null);

  // Fetch years (we need at least one year to create groups)
  const { data: years = [] } = useQuery({
    queryKey: ['student-years', institutionId],
    queryFn: () => studentYearService.getAll(institutionId),
  });

  // Get all groups from all years
  const allGroups = years.flatMap((year) => year.groups || []);

  // Auto-create default year if none exist
  const createDefaultYear = useMutation({
    mutationFn: () =>
      studentYearService.create(institutionId, {
        name: 'Academic Year 2024',
        short_name: '2024',
        order: 0,
      }),
    onSuccess: () => {
      queryClient.invalidateQueries(['student-years', institutionId]);
    },
  });

  // Form
  const form = useForm<StudentGroupCreate & { year_id: number }>({
    defaultValues: {
      name: '',
      short_name: '',
      student_count: 30,
      year_id: years[0]?.id || 1,
    },
  });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (data: StudentGroupCreate & { year_id: number }) => {
      const { year_id, ...groupData } = data;
      return studentGroupService.create(institutionId, year_id, groupData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['student-years', institutionId]);
      setDialogOpen(false);
      form.reset();
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({
      id,
      year_id,
      data,
    }: {
      id: number;
      year_id: number;
      data: Partial<StudentGroupCreate>;
    }) => studentGroupService.update(institutionId, year_id, id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['student-years', institutionId]);
      setDialogOpen(false);
      setEditingGroup(null);
      form.reset();
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: ({ id, year_id }: { id: number; year_id: number }) =>
      studentGroupService.delete(institutionId, year_id, id),
    onSuccess: () => {
      queryClient.invalidateQueries(['student-years', institutionId]);
      setDeleteDialogOpen(false);
      setGroupToDelete(null);
    },
  });

  const handleOpenDialog = (group?: StudentGroup) => {
    // Ensure we have a year
    if (years.length === 0) {
      createDefaultYear.mutate();
      return;
    }

    if (group) {
      setEditingGroup(group);
      form.reset({
        name: group.name,
        short_name: group.short_name,
        student_count: group.student_count,
        year_id: group.year_id,
      });
    } else {
      setEditingGroup(null);
      form.reset({
        name: '',
        short_name: '',
        student_count: 30,
        year_id: years[0]?.id || 1,
      });
    }
    setDialogOpen(true);
  };

  const handleSubmit = form.handleSubmit((data) => {
    if (editingGroup) {
      updateMutation.mutate({
        id: editingGroup.id,
        year_id: data.year_id,
        data,
      });
    } else {
      createMutation.mutate(data);
    }
  });

  const handleDelete = (group: StudentGroup) => {
    setGroupToDelete(group);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    if (groupToDelete) {
      deleteMutation.mutate({
        id: groupToDelete.id,
        year_id: groupToDelete.year_id,
      });
    }
  };

  // Filter groups
  const filteredGroups = allGroups.filter((group) => {
    const searchLower = searchQuery.toLowerCase();
    return (
      group.name.toLowerCase().includes(searchLower) ||
      group.short_name.toLowerCase().includes(searchLower)
    );
  });

  const isLoading = false; // We're using years query which handles loading

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Student Groups</h1>
        <p className="text-gray-600">
          Manage student groups and classes
        </p>
      </div>

      <div className="bg-white rounded-lg border">
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between gap-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              placeholder="Search groups..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9"
            />
          </div>
          <Button onClick={() => handleOpenDialog()}>
            <Plus className="w-4 h-4 mr-2" />
            Add Group
          </Button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
            </div>
          ) : filteredGroups.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              {searchQuery ? (
                <>No groups found matching "{searchQuery}"</>
              ) : (
                <>No student groups yet. Click "Add Group" to get started.</>
              )}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Short Name</TableHead>
                  <TableHead>Student Count</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredGroups.map((group) => (
                  <TableRow key={group.id}>
                    <TableCell className="font-medium">{group.name}</TableCell>
                    <TableCell>
                      <span className="inline-flex items-center px-2 py-1 rounded text-xs font-mono bg-gray-100">
                        {group.short_name}
                      </span>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-2">
                        <Users className="w-4 h-4 text-gray-400" />
                        <span className="font-semibold">{group.student_count}</span>
                        <span className="text-xs text-gray-500">students</span>
                      </div>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleOpenDialog(group)}
                      >
                        <Pencil className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(group)}
                      >
                        <Trash2 className="w-4 h-4 text-red-500" />
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </div>

        {/* Footer */}
        {!isLoading && filteredGroups.length > 0 && (
          <div className="p-4 border-t text-sm text-gray-600">
            Showing {filteredGroups.length} of {allGroups.length} group
            {allGroups.length !== 1 ? 's' : ''} • Total students:{' '}
            {allGroups.reduce((sum, group) => sum + group.student_count, 0)}
          </div>
        )}
      </div>

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editingGroup ? 'Edit Student Group' : 'Add Student Group'}
            </DialogTitle>
            <DialogDescription>
              {editingGroup
                ? 'Update student group information'
                : 'Add a new student group or class'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Name *</Label>
                <Input
                  id="name"
                  placeholder="Grade 10A"
                  {...form.register('name', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="short_name">Short Name *</Label>
                <Input
                  id="short_name"
                  placeholder="10A"
                  {...form.register('short_name', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="student_count">Student Count *</Label>
                <Input
                  id="student_count"
                  type="number"
                  placeholder="30"
                  {...form.register('student_count', {
                    required: true,
                    valueAsNumber: true,
                  })}
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
                ) : editingGroup ? (
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
            <DialogTitle>Delete Student Group</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{groupToDelete?.name}"? This
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
