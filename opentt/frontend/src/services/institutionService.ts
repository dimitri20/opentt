import api from '@/lib/api';
import type {
  Institution,
  InstitutionCreate,
  InstitutionUpdate,
  AcademicYear,
  AcademicYearCreate,
  DayOfWeek,
  DayOfWeekCreate,
  DayOfWeekUpdate,
  Period,
  PeriodCreate,
  PeriodUpdate,
  PaginationParams,
} from '@/types';

// Institutions
export const institutionService = {
  getAll: async (params?: PaginationParams) => {
    const response = await api.get<Institution[]>('/api/institutions/', { params });
    return response.data;
  },

  getById: async (id: number) => {
    const response = await api.get<Institution>(`/api/institutions/${id}`);
    return response.data;
  },

  create: async (data: InstitutionCreate) => {
    const response = await api.post<Institution>('/api/institutions/', data);
    return response.data;
  },

  update: async (id: number, data: InstitutionUpdate) => {
    const response = await api.put<Institution>(`/api/institutions/${id}`, data);
    return response.data;
  },

  delete: async (id: number) => {
    await api.delete(`/api/institutions/${id}`);
  },
};

// Academic Years
export const academicYearService = {
  getAll: async (institutionId: number, params?: PaginationParams) => {
    const response = await api.get<AcademicYear[]>(
      `/api/institutions/${institutionId}/academic-years`,
      { params }
    );
    return response.data;
  },

  create: async (institutionId: number, data: AcademicYearCreate) => {
    const response = await api.post<AcademicYear>(
      `/api/institutions/${institutionId}/academic-years`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, yearId: number, data: Partial<AcademicYearCreate>) => {
    const response = await api.put<AcademicYear>(
      `/api/institutions/${institutionId}/academic-years/${yearId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, yearId: number) => {
    await api.delete(`/api/institutions/${institutionId}/academic-years/${yearId}`);
  },
};

// Days of Week
export const dayOfWeekService = {
  getAll: async (institutionId: number) => {
    const response = await api.get<DayOfWeek[]>(`/api/institutions/${institutionId}/days`);
    return response.data;
  },

  create: async (institutionId: number, data: DayOfWeekCreate) => {
    const response = await api.post<DayOfWeek>(
      `/api/institutions/${institutionId}/days`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, dayId: number, data: DayOfWeekUpdate) => {
    const response = await api.put<DayOfWeek>(
      `/api/institutions/${institutionId}/days/${dayId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, dayId: number) => {
    await api.delete(`/api/institutions/${institutionId}/days/${dayId}`);
  },
};

// Periods
export const periodService = {
  getAll: async (institutionId: number) => {
    const response = await api.get<Period[]>(`/api/institutions/${institutionId}/periods`);
    return response.data;
  },

  create: async (institutionId: number, data: PeriodCreate) => {
    const response = await api.post<Period>(
      `/api/institutions/${institutionId}/periods`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, periodId: number, data: PeriodUpdate) => {
    const response = await api.put<Period>(
      `/api/institutions/${institutionId}/periods/${periodId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, periodId: number) => {
    await api.delete(`/api/institutions/${institutionId}/periods/${periodId}`);
  },
};
