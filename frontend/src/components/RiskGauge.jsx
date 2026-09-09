import React from "react";
import { ShieldCheck, AlertOctagon, AlertTriangle } from "lucide-react";

export default function RiskGauge({ riskScore = 0, rawConfidence = 0, acousticScore = 0, threatTier }) {
  // SVG gauge circle parameters
  const size = 200;
  const strokeWidth = 14;
  const center = size / 2;
  const radius = center - strokeWidth - 4;
  const circumference = 2 * Math.PI * radius;
  
  // Arc angle: 260 degrees
  const arcLength = circumference * 0.72;
  const strokeDashoffset = arcLength - (arcLength * Math.min(100, Math.max(0, riskScore))) / 100;

  // Determine color theme based on continuous score
  let strokeColor = "#10b981"; // Safe
  let glowColor = "rgba(16, 185, 129, 0.4)";
  let icon = <ShieldCheck size={32} color="#10b981" />;

  if (riskScore >= 70) {
    strokeColor = "#ef4444"; // Clone
    glowColor = "rgba(239, 68, 68, 0.5)";
    icon = <AlertOctagon size={32} color="#ef4444" />;
  } else if (riskScore >= 45) {
    strokeColor = "#f59e0b"; // Warning
    glowColor = "rgba(245, 158, 11, 0.4)";
    icon = <AlertTriangle size={32} color="#f59e0b" />;
  }

  return (
    <div className="glass-panel" style={{
      padding: "20px",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      position: "relative",
      overflow: "hidden"
    }}>
      {/* Background radial glow */}
      <div style={{
        position: "absolute",
        top: "40%",
        left: "50%",
        transform: "translate(-50%, -50%)",
        width: "150px",
        height: "150px",
        borderRadius: "50%",
        background: glowColor,
        filter: "blur(45px)",
        pointerEvents: "none",
        opacity: 0.35,
        transition: "all 0.5s ease"
      }} />

      <h3 style={{ fontSize: "0.82rem", color: "var(--text-secondary)", fontWeight: 600, letterSpacing: "0.06em", textTransform: "uppercase", marginBottom: "8px" }}>
        Acoustic Threat Analysis
      </h3>

      {/* Radial SVG Gauge */}
      <div style={{ position: "relative", width: size, height: size * 0.82, display: "flex", alignItems: "center", justifyContent: "center" }}>
        <svg width={size} height={size} style={{ transform: "rotate(140deg)" }}>
          {/* Background Track */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke="rgba(255, 255, 255, 0.07)"
            strokeWidth={strokeWidth}
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeLinecap="round"
          />
          {/* Animated Glowing Progress Bar */}
          <circle
            cx={center}
            cy={center}
            r={radius}
            fill="none"
            stroke={strokeColor}
            strokeWidth={strokeWidth}
            strokeDasharray={`${arcLength} ${circumference}`}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            style={{
              transition: "stroke-dashoffset 0.8s cubic-bezier(0.16, 1, 0.3, 1), stroke 0.4s ease",
              filter: `drop-shadow(0 0 8px ${strokeColor})`
            }}
          />
        </svg>

        {/* Center Score Display */}
        <div style={{
          position: "absolute",
          top: "48%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center"
        }}>
          <div style={{ marginBottom: "2px" }}>
            {icon}
          </div>
          <div style={{
            fontSize: "2.4rem",
            fontWeight: 800,
            lineHeight: 1,
            color: strokeColor,
            textShadow: `0 0 15px ${glowColor}`,
            fontFamily: "var(--font-mono)"
          }}>
            {riskScore}
            <span style={{ fontSize: "1.1rem", fontWeight: 500, color: "var(--text-muted)" }}>%</span>
          </div>
          <span style={{ fontSize: "0.68rem", color: "var(--text-secondary)", textTransform: "uppercase", letterSpacing: "0.08em", marginTop: "2px" }}>
            Synthetic Risk Index
          </span>
        </div>
      </div>

      {/* Threat Tier Status Badge */}
      <div style={{
        marginTop: "4px",
        padding: "6px 16px",
        borderRadius: "20px",
        background: riskScore >= 70 ? "rgba(239, 68, 68, 0.15)" : riskScore >= 45 ? "rgba(245, 158, 11, 0.15)" : "rgba(16, 185, 129, 0.15)",
        border: `1px solid ${strokeColor}`,
        color: strokeColor,
        fontWeight: 700,
        fontSize: "0.8rem",
        boxShadow: `0 0 10px ${glowColor}`,
        textAlign: "center"
      }}>
        {threatTier || (riskScore >= 70 ? "HIGH RISK — AI VOICE CLONE" : riskScore >= 45 ? "SUSPICIOUS ACOUSTICS" : "AUTHENTIC HUMAN VOICE — SAFE")}
      </div>

      {/* Continuous Acoustic Frequency vs Neural Model Telemetry */}
      <div style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gap: "10px",
        width: "100%",
        marginTop: "16px",
        paddingTop: "14px",
        borderTop: "1px solid var(--border-subtle)",
        fontSize: "0.75rem"
      }}>
        <div style={{ textAlign: "center", background: "rgba(10, 14, 26, 0.7)", padding: "8px", borderRadius: "8px" }}>
          <span style={{ color: "var(--text-muted)", display: "block", fontSize: "0.7rem" }}>Acoustic Frequency Anomaly</span>
          <span className="font-mono" style={{ fontWeight: 600, color: "#00f2fe", fontSize: "0.9rem" }}>
            {((acousticScore || (rawConfidence * 0.9)) * 100).toFixed(1)}%
          </span>
        </div>
        <div style={{ textAlign: "center", background: "rgba(10, 14, 26, 0.7)", padding: "8px", borderRadius: "8px" }}>
          <span style={{ color: "var(--text-muted)", display: "block", fontSize: "0.7rem" }}>Neural Vocoder Probability</span>
          <span className="font-mono" style={{ fontWeight: 600, color: strokeColor, fontSize: "0.9rem" }}>
            {(rawConfidence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

    </div>
  );
}
