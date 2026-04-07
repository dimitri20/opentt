import api from '@/lib/api';
import type { Subject, SubjectCreate, SubjectUpdate, PaginationParams } from '@/types';

export const subjectService = {
  getAll: async (institutionId: number, params?: PaginationParams) => {
    const response = await api.get<Subject[]>(
      `/api/institutions/${institutionId}/subjects`,
      { params }
    );
    return response.data;
  },

  getById: async (institutionId: number, subjectId: number) => {
    const response = await api.get<Subject>(
      `/api/institutions/${institutionId}/subjects/${subjectId}`
    );
    return response.data;
  },

  create: async (institutionId: number, data: SubjectCreate) => {
    const response = await api.post<Subject>(
      `/api/institutions/${institutionId}/subjects`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, subjectId: number, data: SubjectUpdate) => {
    const response = await api.put<Subject>(
      `/api/institutions/${institutionId}/subjects/${subjectId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, subjectId: number) => {
    await api.delete(`/api/institutions/${institutionId}/subjects/${subjectId}`);
  },
};
