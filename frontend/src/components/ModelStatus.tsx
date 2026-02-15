"use client";

import { useEffect, useState } from "react";
import type { ModelInfo } from "@/lib/api";
import { fetchModels } from "@/lib/api";

export default function ModelStatus() {
  const [models, setModels] = useState<ModelInfo[]>([]);

  useEffect(() => {
    fetchModels()
      .then((r) => setModels(r.models))
      .catch(() => {});
  }, []);

  if (models.length === 0) return null;

  return (
    <div className="models-grid">
      {models.map((m) => (
        <div key={m.name} className="model-card">
          <span className={`dot ${m.is_loaded ? "dot-green" : "dot-red"}`} />
          <span>{m.name}</span>
        </div>
      ))}
    </div>
  );
}
