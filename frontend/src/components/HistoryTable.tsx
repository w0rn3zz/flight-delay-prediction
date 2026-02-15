"use client";

import { useEffect, useState } from "react";
import type { FlightPredictionResponse } from "@/lib/api";
import { fetchPredictions } from "@/lib/api";

export default function HistoryTable() {
  const [rows, setRows] = useState<FlightPredictionResponse[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPredictions(50)
      .then(setRows)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p style={{ color: "var(--muted)" }}>Loading history…</p>;
  if (rows.length === 0)
    return <p style={{ color: "var(--muted)" }}>No predictions yet.</p>;

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Model</th>
            <th>Result</th>
            <th>Probability</th>
            <th>ID</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.prediction_id}>
              <td>{new Date(r.created_at).toLocaleString()}</td>
              <td>{r.model_used}</td>
              <td>
                <span
                  className={`badge ${r.delayed ? "badge-danger" : "badge-success"}`}
                >
                  {r.delayed ? "Delayed" : "On Time"}
                </span>
              </td>
              <td>{(r.delay_probability * 100).toFixed(1)}%</td>
              <td style={{ fontFamily: "monospace", fontSize: "0.8rem" }}>
                {r.prediction_id.slice(0, 8)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
