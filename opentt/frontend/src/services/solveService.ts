import api from '@/lib/api';
import type { SolveJob, SolveJobCreate } from '@/types';

export const solveService = {
  startSolve: async (institutionId: number, data: SolveJobCreate) => {
    const response = await api.post<SolveJob>(
      `/api/institutions/${institutionId}/solve`,
      data
    );
    return response.data;
  },

  getJobById: async (institutionId: number, jobId: number) => {
    const response = await api.get<SolveJob>(
      `/api/institutions/${institutionId}/solve-jobs/${jobId}`
    );
    return response.data;
  },

  getAllJobs: async (institutionId: number, limit: number = 20) => {
    const response = await api.get<SolveJob[]>(
      `/api/institutions/${institutionId}/solve-jobs`,
      { params: { limit } }
    );
    return response.data;
  },

  getLatestCompleted: async (institutionId: number) => {
    const response = await api.get<SolveJob>(
      `/api/institutions/${institutionId}/solve-jobs/latest/completed`
    );
    return response.data;
  },
};
