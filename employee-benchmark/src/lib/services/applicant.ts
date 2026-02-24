import { apiRequest } from '$lib/api/client';
import { BASE_URL } from '$lib/config';
import type { Applicant } from '$lib/types/index';

export const ApplicantService = {
    async getOverview(): Promise<Applicant[]> {
        return await apiRequest<Applicant[]>(`${BASE_URL}/applicants`);
    },
    async getById(id: string): Promise<Applicant> {
        return await apiRequest<Applicant>(`${BASE_URL}/applicants/${id}`);
    },
    async triggerBenchmark(data: any) {
        return apiRequest(`${BASE_URL}/benchmark`, 'POST', data);
    }
};