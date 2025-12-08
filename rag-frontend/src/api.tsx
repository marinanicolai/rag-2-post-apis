// src/api.ts
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL as string;

export async function uploadFile(file: File) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/upload/`, {
    method: "POST",
    body: formData,
  });

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`Upload failed (${res.status}): ${text}`);
  }

  return JSON.parse(text) as { message: string; filename: string; chunks: number };
}

export async function askQuestion(q: string) {
  const res = await fetch(`${API_BASE_URL}/ask/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ q }),
  });

  const text = await res.text();
  if (!res.ok) {
    throw new Error(`Ask failed (${res.status}): ${text}`);
  }

  return JSON.parse(text) as { query: string; answer: string };
}
