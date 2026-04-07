import api from '@/lib/api';
import type {
  StudentYear,
  StudentYearCreate,
  StudentYearWithGroups,
  StudentGroup,
  StudentGroupCreate,
  StudentGroupWithSubgroups,
  StudentSubgroup,
  StudentSubgroupCreate,
  PaginationParams,
} from '@/types';

// Student Years
export const studentYearService = {
  getAll: async (institutionId: number, params?: PaginationParams) => {
    const response = await api.get<StudentYearWithGroups[]>(
      `/api/institutions/${institutionId}/student-years`,
      { params }
    );
    return response.data;
  },

  getById: async (institutionId: number, yearId: number) => {
    const response = await api.get<StudentYearWithGroups>(
      `/api/institutions/${institutionId}/student-years/${yearId}`
    );
    return response.data;
  },

  create: async (institutionId: number, data: StudentYearCreate) => {
    const response = await api.post<StudentYear>(
      `/api/institutions/${institutionId}/student-years`,
      data
    );
    return response.data;
  },

  update: async (institutionId: number, yearId: number, data: Partial<StudentYearCreate>) => {
    const response = await api.put<StudentYear>(
      `/api/institutions/${institutionId}/student-years/${yearId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, yearId: number) => {
    await api.delete(`/api/institutions/${institutionId}/student-years/${yearId}`);
  },
};

// Student Groups
export const studentGroupService = {
  getAllByYear: async (institutionId: number, yearId: number) => {
    const response = await api.get<StudentGroupWithSubgroups[]>(
      `/api/institutions/${institutionId}/student-years/${yearId}/groups`
    );
    return response.data;
  },

  create: async (institutionId: number, yearId: number, data: StudentGroupCreate) => {
    const response = await api.post<StudentGroup>(
      `/api/institutions/${institutionId}/student-years/${yearId}/groups`,
      data
    );
    return response.data;
  },

  update: async (
    institutionId: number,
    yearId: number,
    groupId: number,
    data: Partial<StudentGroupCreate>
  ) => {
    const response = await api.put<StudentGroup>(
      `/api/institutions/${institutionId}/student-years/${yearId}/groups/${groupId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, yearId: number, groupId: number) => {
    await api.delete(
      `/api/institutions/${institutionId}/student-years/${yearId}/groups/${groupId}`
    );
  },
};

// Student Subgroups
export const studentSubgroupService = {
  getAllByGroup: async (institutionId: number, groupId: number) => {
    const response = await api.get<StudentSubgroup[]>(
      `/api/institutions/${institutionId}/student-groups/${groupId}/subgroups`
    );
    return response.data;
  },

  create: async (institutionId: number, groupId: number, data: StudentSubgroupCreate) => {
    const response = await api.post<StudentSubgroup>(
      `/api/institutions/${institutionId}/student-groups/${groupId}/subgroups`,
      data
    );
    return response.data;
  },

  update: async (
    institutionId: number,
    groupId: number,
    subgroupId: number,
    data: Partial<StudentSubgroupCreate>
  ) => {
    const response = await api.put<StudentSubgroup>(
      `/api/institutions/${institutionId}/student-groups/${groupId}/subgroups/${subgroupId}`,
      data
    );
    return response.data;
  },

  delete: async (institutionId: number, groupId: number, subgroupId: number) => {
    await api.delete(
      `/api/institutions/${institutionId}/student-groups/${groupId}/subgroups/${subgroupId}`
    );
  },
};
