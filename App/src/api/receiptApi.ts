const API_URL = "http://localhost:8000"

export async function createReceipt(data: any) {

    const response = await fetch(
        `${API_URL}/receipt`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        }
    );

    if (!response.ok) {
        throw new Error("Failed to creat receipt");
    }

    return response.json();
}