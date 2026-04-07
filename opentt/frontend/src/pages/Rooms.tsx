import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Pencil, Trash2, Loader2, Search } from 'lucide-react';
import { useInstitution } from '@/hooks/useInstitution';
import { roomService, buildingService } from '@/services';
import type { Room, RoomCreate, Building } from '@/types';
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

export default function Rooms() {
  const { institutionId } = useInstitution();
  const queryClient = useQueryClient();
  const [searchQuery, setSearchQuery] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);
  const [editingRoom, setEditingRoom] = useState<Room | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [roomToDelete, setRoomToDelete] = useState<Room | null>(null);

  // Fetch buildings (we need at least one building to create rooms)
  const { data: buildings = [] } = useQuery({
    queryKey: ['buildings', institutionId],
    queryFn: () => buildingService.getAll(institutionId),
  });

  // Fetch all rooms
  const { data: rooms = [], isLoading } = useQuery({
    queryKey: ['rooms', institutionId],
    queryFn: () => roomService.getAll(institutionId),
  });

  // Form
  const form = useForm<RoomCreate & { building_id: number }>({
    defaultValues: {
      name: '',
      code: '',
      capacity: 30,
      room_type: '',
      building_id: buildings[0]?.id || 1, // Default to first building
    },
  });

  // Auto-create default building if none exist
  const createDefaultBuilding = useMutation({
    mutationFn: () =>
      buildingService.create(institutionId, {
        name: 'Main Building',
        code: 'MAIN',
      }),
    onSuccess: () => {
      queryClient.invalidateQueries(['buildings', institutionId]);
    },
  });

  // Create mutation
  const createMutation = useMutation({
    mutationFn: (data: RoomCreate & { building_id: number }) => {
      const { building_id, ...roomData } = data;
      return roomService.create(institutionId, building_id, roomData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['rooms', institutionId]);
      setDialogOpen(false);
      form.reset();
    },
  });

  // Update mutation
  const updateMutation = useMutation({
    mutationFn: ({
      id,
      building_id,
      data,
    }: {
      id: number;
      building_id: number;
      data: Partial<RoomCreate>;
    }) => roomService.update(institutionId, building_id, id, data),
    onSuccess: () => {
      queryClient.invalidateQueries(['rooms', institutionId]);
      setDialogOpen(false);
      setEditingRoom(null);
      form.reset();
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: ({ id, building_id }: { id: number; building_id: number }) =>
      roomService.delete(institutionId, building_id, id),
    onSuccess: () => {
      queryClient.invalidateQueries(['rooms', institutionId]);
      setDeleteDialogOpen(false);
      setRoomToDelete(null);
    },
  });

  const handleOpenDialog = (room?: Room) => {
    // Ensure we have a building
    if (buildings.length === 0) {
      createDefaultBuilding.mutate();
      return;
    }

    if (room) {
      setEditingRoom(room);
      form.reset({
        name: room.name,
        code: room.code || '',
        capacity: room.capacity,
        room_type: room.room_type || '',
        building_id: room.building_id,
      });
    } else {
      setEditingRoom(null);
      form.reset({
        name: '',
        code: '',
        capacity: 30,
        room_type: '',
        building_id: buildings[0]?.id || 1,
      });
    }
    setDialogOpen(true);
  };

  const handleSubmit = form.handleSubmit((data) => {
    if (editingRoom) {
      updateMutation.mutate({
        id: editingRoom.id,
        building_id: data.building_id,
        data,
      });
    } else {
      createMutation.mutate(data);
    }
  });

  const handleDelete = (room: Room) => {
    setRoomToDelete(room);
    setDeleteDialogOpen(true);
  };

  const confirmDelete = () => {
    if (roomToDelete) {
      deleteMutation.mutate({
        id: roomToDelete.id,
        building_id: roomToDelete.building_id,
      });
    }
  };

  // Filter rooms
  const filteredRooms = rooms.filter((room) => {
    const searchLower = searchQuery.toLowerCase();
    return (
      room.name.toLowerCase().includes(searchLower) ||
      room.code?.toLowerCase().includes(searchLower) ||
      room.room_type?.toLowerCase().includes(searchLower)
    );
  });

  return (
    <div className="p-6 max-w-7xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold mb-2">Rooms</h1>
        <p className="text-gray-600">
          Manage classrooms and teaching spaces
        </p>
      </div>

      <div className="bg-white rounded-lg border">
        {/* Header */}
        <div className="p-4 border-b flex items-center justify-between gap-4">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <Input
              placeholder="Search rooms..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-9"
            />
          </div>
          <Button onClick={() => handleOpenDialog()}>
            <Plus className="w-4 h-4 mr-2" />
            Add Room
          </Button>
        </div>

        {/* Table */}
        <div className="overflow-x-auto">
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
            </div>
          ) : filteredRooms.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              {searchQuery ? (
                <>No rooms found matching "{searchQuery}"</>
              ) : (
                <>No rooms yet. Click "Add Room" to get started.</>
              )}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Code</TableHead>
                  <TableHead>Capacity</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead className="text-right">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {filteredRooms.map((room) => (
                  <TableRow key={room.id}>
                    <TableCell className="font-medium">{room.name}</TableCell>
                    <TableCell>
                      <span className="inline-flex items-center px-2 py-1 rounded text-xs font-mono bg-gray-100">
                        {room.code || '-'}
                      </span>
                    </TableCell>
                    <TableCell>
                      <span className="inline-flex items-center gap-1">
                        <span className="font-semibold">{room.capacity}</span>
                        <span className="text-xs text-gray-500">seats</span>
                      </span>
                    </TableCell>
                    <TableCell>
                      {room.room_type ? (
                        <span className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-blue-50 text-blue-700">
                          {room.room_type}
                        </span>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleOpenDialog(room)}
                      >
                        <Pencil className="w-4 h-4" />
                      </Button>
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => handleDelete(room)}
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
        {!isLoading && filteredRooms.length > 0 && (
          <div className="p-4 border-t text-sm text-gray-600">
            Showing {filteredRooms.length} of {rooms.length} room
            {rooms.length !== 1 ? 's' : ''} • Total capacity:{' '}
            {rooms.reduce((sum, room) => sum + room.capacity, 0)} seats
          </div>
        )}
      </div>

      {/* Add/Edit Dialog */}
      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{editingRoom ? 'Edit Room' : 'Add Room'}</DialogTitle>
            <DialogDescription>
              {editingRoom
                ? 'Update room information'
                : 'Add a new room to your institution'}
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleSubmit}>
            <div className="grid gap-4 py-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Name *</Label>
                <Input
                  id="name"
                  placeholder="Room 101"
                  {...form.register('name', { required: true })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="code">Code</Label>
                <Input
                  id="code"
                  placeholder="R101"
                  {...form.register('code')}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="capacity">Capacity *</Label>
                <Input
                  id="capacity"
                  type="number"
                  placeholder="30"
                  {...form.register('capacity', {
                    required: true,
                    valueAsNumber: true,
                  })}
                />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="room_type">Type</Label>
                <Input
                  id="room_type"
                  placeholder="Classroom, Lab, Auditorium"
                  {...form.register('room_type')}
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
                ) : editingRoom ? (
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
            <DialogTitle>Delete Room</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{roomToDelete?.name}"? This
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
