import React from "react";
import { Activity, Waves, Sliders, Zap, CheckCircle2, AlertTriangle } from "lucide-react";

export default function AcousticMetrics({ metrics = {} }) {
  if (!metrics || Object.keys(metrics).length === 0) return null;

  const {
    duration_seconds = 0,
    spectral_flatness = 0,
    spectral_rolloff_hz = 0,
    pitch_f0_mean_hz = 0,
    pitch_micro_jitter = 0
  } = metrics;

  // Evaluation criteria for AI vocoders vs authentic human voice
  const isJitterSynthetic = pitch_micro_jitter < 0.015;
  const isFlatnessSynthetic = spectral_flatness > 0.0003;
  const isRolloffLow = spectral_rolloff_hz < 1200;

  const metricCards = [
    {
      title: "Pitch Micro-Jitter (F0)",
      value: `${pitch_micro_jitter.toFixed(4)}`,
      status: isJitterSynthetic ? "Artificial Stability (AI Signature)" : "Organic Vocal Tremor",
      isWarning: isJitterSynthetic,
      desc: "Human voices have natural micro-tremor; AI vocoders exhibit rigid robotic pitch tracking.",
      icon: <Activity size={18} color={isJitterSynthetic ? "#ef4444" : "#10b981"} />
    },
    {
      title: "Spectral Flatness",
      value: `${(spectral_flatness * 1000).toFixed(2)} e-3`,
      status: isFlatnessSynthetic ? "Neural Smoothing (Vocoder)" : "Natural Turbulence",
      isWarning: isFlatnessSynthetic,
      desc: "Neural synthesis (HiFi-GAN) flattens harmonic distribution compared to organic air turbulence.",
      icon: <Waves size={18} color={isFlatnessSynthetic ? "#ef4444" : "#10b981"} />
    },
    {
      title: "Spectral Rolloff",
      value: `${Math.round(spectral_rolloff_hz)} Hz`,
      status: isRolloffLow ? "Damped High-Freqs" : "Full Human Spectrum",
      isWarning: isRolloffLow,
      desc: "Frequency threshold containing 85% of total audio energy.",
      icon: <Sliders size={18} color="#00f2fe" />
    },
    {
      title: "Base Pitch (F0 Mean)",
      value: `${Math.round(pitch_f0_mean_hz)} Hz`,
      status: "Fundamental Frequency",
      isWarning: false,
      desc: "Average fundamental vocal tract pitch tracking.",
      icon: <Zap size={18} color="#8b5cf6" />
    }
  ];

  return (
    <div className="glass-panel" style={{ padding: "24px", marginBottom: "24px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
        <h3 style={{ fontSize: "0.95rem", fontWeight: 700, color: "var(--text-primary)", display: "flex", alignItems: "center", gap: "8px" }}>
          <Sliders size={18} color="#00f2fe" />
          <span>Forensic Acoustic & Vocoder Telemetry (147 Features)</span>
        </h3>
        <span className="badge-safe" style={{ fontSize: "0.7rem" }}>
          Audio Duration: {duration_seconds}s
        </span>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "14px" }}>
        {metricCards.map((card, idx) => (
          <div
            key={idx}
            style={{
              background: "rgba(10, 14, 26, 0.7)",
              border: card.isWarning ? "1px solid rgba(239, 68, 68, 0.3)" : "1px solid var(--border-subtle)",
              borderRadius: "12px",
              padding: "16px",
              display: "flex",
              flexDirection: "column",
              justifyContent: "space-between"
            }}
          >
            <div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
                <span style={{ fontSize: "0.78rem", color: "var(--text-secondary)", fontWeight: 600 }}>
                  {card.title}
                </span>
                {card.icon}
              </div>
              <div className="font-mono" style={{ fontSize: "1.4rem", fontWeight: 700, color: card.isWarning ? "#f87171" : "#f8fafc", marginBottom: "4px" }}>
                {card.value}
              </div>
              <div style={{
                fontSize: "0.72rem",
                fontWeight: 600,
                color: card.isWarning ? "#fbbf24" : "#34d399",
                marginBottom: "8px",
                display: "flex",
                alignItems: "center",
                gap: "4px"
              }}>
                {card.isWarning ? <AlertTriangle size={12} /> : <CheckCircle2 size={12} />}
                {card.status}
              </div>
            </div>
            <p style={{ fontSize: "0.7rem", color: "var(--text-muted)", lineHeight: "1.3" }}>
              {card.desc}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
