import api from '@/lib/api';
import type {
  Activity,
  ActivityCreate,
  ActivityUpdate,
  ActivityWithRelations,
  PaginationParams,
} from '@/types';

export const activityService = {
  getAll: async (institutionId: number, params?: PaginationParams) => {
    const response = await api.get<ActivityWithRelations[]>(
      `/api/institutions/${institutionId}/activities`,
      { params }
    );
    return response.data;
  },

  getById: async (institutionId: number, activityId: number) => {
    const response = await api.get<ActivityWithRelations>(
      `/api/institutions/${institutionId}/activities/${activityId}`
    );
    return response.data;
  },

  create: async (institutionId: number, data: ActivityCreate) => {
    const response = await api.post<ActivityWithRelations>(
      `/api/institutions/${institutionId}/activities`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, activityId: number, data: ActivityUpdate) => {
    const response = await api.put<ActivityWithRelations>(
      `/api/institutions/${institutionId}/activities/${activityId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, activityId: number) => {
    await api.delete(`/api/institutions/${institutionId}/activities/${activityId}`);
  },
};
