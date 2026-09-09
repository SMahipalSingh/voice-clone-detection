import React, { useState } from "react";
import { AlertOctagon, CheckCircle2, AlertTriangle, Link2, Copy, Check } from "lucide-react";

export default function AlertBanner({ result }) {
  const [copied, setCopied] = useState(false);

  if (!result) return null;

  const { risk_score, threat_tier, recommendation, forensic_summary, blockchain, filename } = result;
  const isDanger = risk_score >= 70;
  const isWarning = risk_score >= 45 && risk_score < 70;

  const handleCopyHash = () => {
    if (blockchain?.block_hash) {
      navigator.clipboard.writeText(blockchain.block_hash);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  let bannerBg = "rgba(16, 185, 129, 0.1)";
  let borderColor = "rgba(16, 185, 129, 0.4)";
  let textColor = "#34d399";
  let icon = <CheckCircle2 size={24} color="#34d399" />;

  if (isDanger) {
    bannerBg = "rgba(239, 68, 68, 0.12)";
    borderColor = "rgba(239, 68, 68, 0.45)";
    textColor = "#f87171";
    icon = <AlertOctagon size={24} color="#f87171" />;
  } else if (isWarning) {
    bannerBg = "rgba(245, 158, 11, 0.12)";
    borderColor = "rgba(245, 158, 11, 0.45)";
    textColor = "#fbbf24";
    icon = <AlertTriangle size={24} color="#fbbf24" />;
  }

  return (
    <div className="glass-panel" style={{
      padding: "20px 24px",
      background: bannerBg,
      border: `1.5px solid ${borderColor}`,
      marginBottom: "24px",
      position: "relative",
      overflow: "hidden"
    }}>
      <div style={{ display: "flex", alignItems: "flex-start", gap: "16px", flexWrap: "wrap" }}>
        
        <div style={{ marginTop: "2px" }}>
          {icon}
        </div>

        <div style={{ flex: 1, minWidth: "260px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap", marginBottom: "4px" }}>
            <h4 style={{ fontSize: "1.05rem", fontWeight: 700, color: textColor }}>
              {threat_tier}
            </h4>
            <span style={{ fontSize: "0.75rem", color: "var(--text-muted)", background: "rgba(0,0,0,0.3)", padding: "2px 8px", borderRadius: "4px" }}>
              Target: {filename}
            </span>
          </div>

          <p style={{ fontSize: "0.85rem", color: "var(--text-primary)", fontWeight: 500, marginBottom: "8px", lineHeight: "1.4" }}>
            {forensic_summary}
          </p>

          <div style={{
            background: "rgba(0, 0, 0, 0.35)",
            padding: "10px 14px",
            borderRadius: "8px",
            borderLeft: `3px solid ${textColor}`,
            fontSize: "0.82rem",
            color: "var(--text-primary)",
            marginBottom: "10px"
          }}>
            <strong style={{ color: textColor }}>Recommended Security Action: </strong>
            {recommendation}
          </div>

          {/* Blockchain Attestation Reference */}
          {blockchain && (
            <div style={{ display: "flex", alignItems: "center", gap: "8px", fontSize: "0.75rem", color: "var(--text-secondary)", flexWrap: "wrap" }}>
              <span className="badge-blockchain" style={{ padding: "2px 8px", fontSize: "0.68rem" }}>
                <Link2 size={11} /> Block #{blockchain.block_index}
              </span>
              <span className="font-mono" style={{ color: "#a78bfa" }}>
                Hash: {blockchain.block_hash ? `${blockchain.block_hash.slice(0, 16)}...${blockchain.block_hash.slice(-8)}` : "Pending"}
              </span>
              <button
                onClick={handleCopyHash}
                style={{
                  background: "transparent",
                  border: "none",
                  color: "var(--text-muted)",
                  cursor: "pointer",
                  display: "inline-flex",
                  alignItems: "center",
                  gap: "4px",
                  padding: "2px 6px"
                }}
                title="Copy Full SHA-256 Hash"
              >
                {copied ? <Check size={12} color="#34d399" /> : <Copy size={12} />}
                <span>{copied ? "Copied" : "Copy"}</span>
              </button>
            </div>
          )}

        </div>
      </div>
    </div>
  );
}
