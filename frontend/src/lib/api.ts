const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface FlightPredictionRequest {
  month: number;
  day_of_month: number;
  day_of_week: number;
  dep_time: number;
  carrier: string;
  origin: string;
  dest: string;
  distance: number;
}

export interface FlightPredictionResponse {
  prediction_id: string;
  delayed: boolean;
  delay_probability: number;
  no_delay_probability: number;
  model_used: string;
  created_at: string;
}

export interface ModelInfo {
  name: string;
  is_loaded: boolean;
}

export interface StatusResponse {
  status: string;
  models: ModelInfo[];
}

export async function createPrediction(
  data: FlightPredictionRequest,
  modelName: string
): Promise<FlightPredictionResponse> {
  const res = await fetch(
    `${API_BASE}/api/v1/predictions/?model_name=${modelName}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }
  );
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error ?? err.detail ?? res.statusText);
  }
  return res.json();
}

export async function fetchPredictions(
  limit = 50,
  offset = 0
): Promise<FlightPredictionResponse[]> {
  const res = await fetch(
    `${API_BASE}/api/v1/predictions/?limit=${limit}&offset=${offset}`,
    { cache: "no-store" }
  );
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
}

export async function fetchModels(): Promise<StatusResponse> {
  const res = await fetch(`${API_BASE}/api/v1/models`, { cache: "no-store" });
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
}

export async function healthCheck(): Promise<{ status: string }> {
  const res = await fetch(`${API_BASE}/health`, { cache: "no-store" });
  if (!res.ok) throw new Error(res.statusText);
  return res.json();
}
