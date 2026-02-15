"use client";

import { useState } from "react";
import PredictionForm from "@/components/PredictionForm";
import HistoryTable from "@/components/HistoryTable";
import ModelStatus from "@/components/ModelStatus";

type Tab = "predict" | "history" | "models";

export default function Home() {
  const [tab, setTab] = useState<Tab>("predict");

  return (
    <main>
      <h1>✈ Flight Delay Prediction</h1>
      <p className="subtitle">
        Predict whether a flight will be delayed using ML models
      </p>

      <div className="tabs">
        <button
          className={`tab ${tab === "predict" ? "active" : ""}`}
          onClick={() => setTab("predict")}
        >
          Predict
        </button>
        <button
          className={`tab ${tab === "history" ? "active" : ""}`}
          onClick={() => setTab("history")}
        >
          History
        </button>
        <button
          className={`tab ${tab === "models" ? "active" : ""}`}
          onClick={() => setTab("models")}
        >
          Models
        </button>
      </div>

      {tab === "predict" && (
        <div className="card">
          <h2>New Prediction</h2>
          <PredictionForm />
        </div>
      )}

      {tab === "history" && (
        <div className="card">
          <h2>Prediction History</h2>
          <HistoryTable />
        </div>
      )}

      {tab === "models" && (
        <div className="card">
          <h2>Model Status</h2>
          <ModelStatus />
        </div>
      )}
    </main>
  );
}
