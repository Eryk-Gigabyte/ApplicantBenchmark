export interface SubmitApplicationsRequest {
	selectedAIs: string[];
	file: File;
}

export interface SubmitApplicationsResponse {
	success: boolean;
	message?: string;
	redirectUrl?: string;
}

/**
 * Submit selected AIs and uploaded file to the backend
 */
export async function submitApplications(
	data: SubmitApplicationsRequest
): Promise<SubmitApplicationsResponse> {
	const formData = new FormData();
	
	// Add selected AIs as array
	data.selectedAIs.forEach((ai) => {
		formData.append('selectedAIs[]', ai);
	});
	
	// Add uploaded file
	formData.append('file', data.file);

	try {
		const response = await fetch('/api/applications/submit', {
			method: 'POST',
			body: formData
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
