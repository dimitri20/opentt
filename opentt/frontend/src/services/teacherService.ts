import api from '@/lib/api';
import type { Teacher, TeacherCreate, TeacherUpdate, PaginationParams } from '@/types';

export const teacherService = {
  getAll: async (institutionId: number, params?: PaginationParams) => {
    const response = await api.get<Teacher[]>(
      `/api/institutions/${institutionId}/teachers`,
      { params }
    );
    return response.data;
  },

  getById: async (institutionId: number, teacherId: number) => {
    const response = await api.get<Teacher>(
      `/api/institutions/${institutionId}/teachers/${teacherId}`
    );
    return response.data;
  },

  create: async (institutionId: number, data: TeacherCreate) => {
    const response = await api.post<Teacher>(
      `/api/institutions/${institutionId}/teachers`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, teacherId: number, data: TeacherUpdate) => {
    const response = await api.put<Teacher>(
      `/api/institutions/${institutionId}/teachers/${teacherId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, teacherId: number) => {
    await api.delete(`/api/institutions/${institutionId}/teachers/${teacherId}`);
  },
};
