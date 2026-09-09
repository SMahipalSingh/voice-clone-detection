import React from "react";
import { Shield, Link2, BookOpen, Activity } from "lucide-react";

export default function Navbar({ 
  blockchainValid, 
  totalBlocks, 
  onOpenPitch,
  onOpenAudit,
  backendStatus 
}) {
  return (
    <header className="glass-panel" style={{ margin: "16px 20px", padding: "14px 20px" }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: "16px" }}>
        
        {/* Brand Logo & Title */}
        <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
          <div style={{
            width: "40px",
            height: "40px",
            borderRadius: "10px",
            background: "linear-gradient(135deg, rgba(0, 242, 254, 0.2) 0%, rgba(139, 92, 246, 0.3) 100%)",
            border: "1px solid rgba(0, 242, 254, 0.4)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 0 15px rgba(0, 242, 254, 0.25)"
          }}>
            <Shield size={22} color="#00f2fe" />
          </div>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
              <h1 style={{ fontSize: "1.2rem", fontWeight: 700, letterSpacing: "-0.02em" }}>
                VOICE<span className="gradient-text">SHIELD</span>
              </h1>
              <span className="badge-blockchain" style={{ fontSize: "0.68rem" }}>
                <Link2 size={11} /> SHA-256 LEDGER
              </span>
            </div>
            <p style={{ fontSize: "0.74rem", color: "var(--text-secondary)" }}>
              Forensic Voice Clone & Deepfake Frequency Analysis Engine
            </p>
          </div>
        </div>

        {/* Right Status Badges & Quick Action */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
          
          {/* Blockchain Node Status Pill */}
          <div 
            onClick={onOpenAudit}
            className={blockchainValid ? "badge-safe" : "badge-danger"} 
            style={{ cursor: "pointer", padding: "6px 12px", fontSize: "0.75rem" }}
            title="Click to view Cryptographic Blockchain Audit"
          >
            <Activity size={13} className="animate-pulse-ring" />
            <span>Ledger: {blockchainValid ? "VERIFIED" : "INTEGRITY ALERT"} ({totalBlocks} Blocks)</span>
          </div>

          {/* Backend Status */}
          <div style={{
            display: "flex",
            alignItems: "center",
            gap: "6px",
            fontSize: "0.75rem",
            color: backendStatus === "online" ? "#34d399" : "#f87171",
            background: "rgba(255,255,255,0.03)",
            padding: "6px 10px",
            borderRadius: "8px",
            border: "1px solid var(--border-subtle)"
          }}>
            <span style={{
              width: "7px",
              height: "7px",
              borderRadius: "50%",
              background: backendStatus === "online" ? "#10b981" : "#ef4444",
              boxShadow: backendStatus === "online" ? "0 0 8px #10b981" : "0 0 8px #ef4444"
            }} />
            <span>{backendStatus === "online" ? "ML Engine Online" : "Connecting..."}</span>
          </div>

          {/* Pitch & Guide Button */}
          <button 
            onClick={onOpenPitch}
            className="btn-secondary" 
            style={{ padding: "6px 12px", fontSize: "0.78rem" }}
          >
            <BookOpen size={13} color="#00f2fe" />
            <span>Architecture Guide</span>
          </button>

        </div>
      </div>
    </header>
  );
}
