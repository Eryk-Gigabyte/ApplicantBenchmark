export interface SubmitApplicationsRequest {
	selectedAIs: string[];
}

export interface SubmitApplicationsResponse {
	success: boolean;
	message?: string;
	redirectUrl?: string;
}

/**
 * Submit selected AIs to the backend (no file upload)
 */
export async function submitApplications(
	data: SubmitApplicationsRequest
): Promise<SubmitApplicationsResponse> {
	try {
		const response = await fetch('/api/applications/submit', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ selectedAIs: data.selectedAIs })
		});

		if (!response.ok) {
			throw new Error(`HTTP error! status: ${response.status}`);
		}

		const result = await response.json();
		return result;
	} catch (error) {
		console.error('Error submitting applications:', error);
		return {
			success: false,
			message: error instanceof Error ? error.message : 'Unknown error occurred'
		};
	}
}
