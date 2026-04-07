import api from '@/lib/api';
import type {
  Building,
  BuildingCreate,
  BuildingUpdate,
  BuildingWithRooms,
  Room,
  RoomCreate,
  RoomUpdate,
  PaginationParams,
} from '@/types';

export const buildingService = {
  getAll: async (institutionId: number, params?: PaginationParams) => {
    const response = await api.get<Building[]>(
      `/api/institutions/${institutionId}/buildings`,
      { params }
    );
    return response.data;
  },

  getById: async (institutionId: number, buildingId: number) => {
    const response = await api.get<BuildingWithRooms>(
      `/api/institutions/${institutionId}/buildings/${buildingId}`
    );
    return response.data;
  },

  create: async (institutionId: number, data: BuildingCreate) => {
    const response = await api.post<Building>(
      `/api/institutions/${institutionId}/buildings`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, buildingId: number, data: BuildingUpdate) => {
    const response = await api.put<Building>(
      `/api/institutions/${institutionId}/buildings/${buildingId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, buildingId: number) => {
    await api.delete(`/api/institutions/${institutionId}/buildings/${buildingId}`);
  },
};

export const roomService = {
  getAllByBuilding: async (institutionId: number, buildingId: number) => {
    const response = await api.get<Room[]>(
      `/api/institutions/${institutionId}/buildings/${buildingId}/rooms`
    );
    return response.data;
  },

  getAll: async (institutionId: number, params?: PaginationParams) => {
    const response = await api.get<Room[]>(
      `/api/institutions/${institutionId}/rooms`,
      { params }
    );
    return response.data;
  },

  create: async (institutionId: number, buildingId: number, data: RoomCreate) => {
    const response = await api.post<Room>(
      `/api/institutions/${institutionId}/buildings/${buildingId}/rooms`,
      data
    );
    return response.data;
  },

  update: async (
    institutionId: number,
    buildingId: number,
    roomId: number,
    data: RoomUpdate
  ) => {
    const response = await api.put<Room>(
      `/api/institutions/${institutionId}/buildings/${buildingId}/rooms/${roomId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, buildingId: number, roomId: number) => {
    await api.delete(
      `/api/institutions/${institutionId}/buildings/${buildingId}/rooms/${roomId}`
    );
  },
};
