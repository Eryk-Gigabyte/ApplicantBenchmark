// Einmalige Konfiguration des Fetch-Verhaltens
export async function apiRequest<T>(url: string, method = 'GET', body?: any): Promise<T> {
    const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: body ? JSON.stringify(body) : undefined
    });
    if (!response.ok) throw new Error(`API Error: ${response.status}`);
    return response.json();
}