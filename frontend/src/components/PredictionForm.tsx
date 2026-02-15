"use client";

import { useState } from "react";
import type { FlightPredictionRequest, FlightPredictionResponse } from "@/lib/api";
import { createPrediction } from "@/lib/api";

const CARRIERS = ["AA", "UA", "DL", "WN", "US", "NW", "CO", "MQ", "OH", "OO", "XE", "TZ", "EV", "FL", "YV", "9E", "AQ", "HA", "B6", "F9"];

const MODELS = [
  { value: "catboost_default", label: "CatBoost Default" },
  { value: "catboost_optimized", label: "CatBoost Optimized" },
  { value: "lightgbm_default", label: "LightGBM Default" },
  { value: "lightgbm_optimized", label: "LightGBM Optimized" },
];

const initial: FlightPredictionRequest = {
  month: 6,
  day_of_month: 15,
  day_of_week: 3,
  dep_time: 1430,
  carrier: "AA",
  origin: "LAX",
  dest: "JFK",
  distance: 2475,
};

export default function PredictionForm() {
  const [form, setForm] = useState(initial);
  const [model, setModel] = useState(MODELS[0].value);
  const [result, setResult] = useState<FlightPredictionResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const set = (key: keyof FlightPredictionRequest, value: string | number) =>
    setForm((prev) => ({ ...prev, [key]: value }));

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const res = await createPrediction(form, model);
      setResult(res);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="form-grid">
          <div className="field">
            <label>Month (1-12)</label>
            <input
              type="number"
              min={1}
              max={12}
              value={form.month}
              onChange={(e) => set("month", +e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Day of Month</label>
            <input
              type="number"
              min={1}
              max={31}
              value={form.day_of_month}
              onChange={(e) => set("day_of_month", +e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Day of Week</label>
            <input
              type="number"
              min={1}
              max={7}
              value={form.day_of_week}
              onChange={(e) => set("day_of_week", +e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Dep Time (HHMM)</label>
            <input
              type="number"
              min={0}
              max={2359}
              value={form.dep_time}
              onChange={(e) => set("dep_time", +e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Carrier</label>
            <select
              value={form.carrier}
              onChange={(e) => set("carrier", e.target.value)}
            >
              {CARRIERS.map((c) => (
                <option key={c}>{c}</option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>Origin</label>
            <input
              type="text"
              maxLength={4}
              value={form.origin}
              onChange={(e) => set("origin", e.target.value.toUpperCase())}
              required
            />
          </div>
          <div className="field">
            <label>Destination</label>
            <input
              type="text"
              maxLength={4}
              value={form.dest}
              onChange={(e) => set("dest", e.target.value.toUpperCase())}
              required
            />
          </div>
          <div className="field">
            <label>Distance (mi)</label>
            <input
              type="number"
              min={0}
              value={form.distance}
              onChange={(e) => set("distance", +e.target.value)}
              required
            />
          </div>
          <div className="field">
            <label>Model</label>
            <select value={model} onChange={(e) => setModel(e.target.value)}>
              {MODELS.map((m) => (
                <option key={m.value} value={m.value}>
                  {m.label}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="btn-row">
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Predicting…" : "Predict Delay"}
          </button>
        </div>
      </form>

      {error && <p className="error-msg">{error}</p>}

      {result && (
        <div style={{ marginTop: "1.25rem" }}>
          <div className={`result ${result.delayed ? "delayed" : "on-time"}`}>
            {result.delayed ? "⚠ Likely Delayed" : "✓ On Time"}
          </div>
          <div className="result-details">
            <span>
              Delay probability:{" "}
              <strong>{(result.delay_probability * 100).toFixed(1)}%</strong>
            </span>
            <span>Model: {result.model_used}</span>
            <span>ID: {result.prediction_id.slice(0, 8)}…</span>
          </div>
        </div>
      )}
    </>
  );
}
