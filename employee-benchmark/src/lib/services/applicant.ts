import { apiRequest } from '$lib/api/client';
import { BASE_URL } from '$lib/config';

export const ApplicantService = {
    async getOverview() {
        return apiRequest(`${BASE_URL}/applicants`);
    },
    async triggerBenchmark(data: any) {
        return apiRequest(`${BASE_URL}/benchmark`, 'POST', data);
    }
};