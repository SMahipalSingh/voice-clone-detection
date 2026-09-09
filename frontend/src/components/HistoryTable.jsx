import React, { useState } from "react";
import { History, Trash2, Copy, Check, FileAudio, RefreshCw } from "lucide-react";

export default function HistoryTable({ history = [], onClear, onRefresh }) {
  const [copiedId, setCopiedId] = useState(null);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleClearClick = async () => {
    if (window.confirm("Are you sure you want to permanently clear all forensic scan records from the database?")) {
      setIsDeleting(true);
      try {
        await onClear();
      } catch (err) {
        alert("Failed to delete history: " + err.message);
      } finally {
        setIsDeleting(false);
      }
    }
  };

  return (
    <div className="glass-panel" style={{ padding: "20px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px", flexWrap: "wrap", gap: "10px" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
          <History size={18} color="#00f2fe" />
          <h3 style={{ fontSize: "1rem", fontWeight: 700 }}>
            Forensic Scan Audit History
          </h3>
          <span style={{ fontSize: "0.72rem", color: "var(--text-muted)", background: "rgba(255,255,255,0.06)", padding: "2px 8px", borderRadius: "10px" }}>
            {history.length} Scans Logged
          </span>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <button
            onClick={onRefresh}
            className="btn-secondary"
            style={{ fontSize: "0.76rem", padding: "6px 12px" }}
            title="Refresh Scan History"
          >
            <RefreshCw size={13} />
            <span>Refresh</span>
          </button>

          {history.length > 0 && (
            <button
              onClick={handleClearClick}
              disabled={isDeleting}
              className="btn-secondary"
              style={{
                fontSize: "0.76rem",
                padding: "6px 12px",
                color: "#f87171",
                borderColor: "rgba(239, 68, 68, 0.4)",
                background: "rgba(239, 68, 68, 0.1)"
              }}
            >
              <Trash2 size={13} />
              <span>{isDeleting ? "Deleting..." : "Clear History"}</span>
            </button>
          )}
        </div>
      </div>

      {history.length === 0 ? (
        <div style={{ textAlign: "center", padding: "32px", color: "var(--text-muted)", fontSize: "0.82rem" }}>
          No scans recorded yet. Upload an audio sample or record with the live microphone to log forensic records.
        </div>
      ) : (
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontSize: "0.78rem", textAlign: "left" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid var(--border-subtle)", color: "var(--text-secondary)" }}>
                <th style={{ padding: "10px 12px", fontWeight: 600 }}>Audio File</th>
                <th style={{ padding: "10px 12px", fontWeight: 600 }}>Acoustic Risk</th>
                <th style={{ padding: "10px 12px", fontWeight: 600 }}>Threat Classification</th>
                <th style={{ padding: "10px 12px", fontWeight: 600 }}>Blockchain Block Hash</th>
                <th style={{ padding: "10px 12px", fontWeight: 600 }}>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              {history.map((row) => {
                const isDanger = row.risk_score >= 70;
                const isWarning = row.risk_score >= 45 && row.risk_score < 70;

                return (
                  <tr key={row.id} style={{ borderBottom: "1px solid rgba(255,255,255,0.03)", transition: "background 0.2s" }}>
                    <td style={{ padding: "10px 12px", fontWeight: 600, color: "var(--text-primary)" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                        <FileAudio size={14} color="#00f2fe" />
                        <span style={{ maxWidth: "220px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
                          {row.filename}
                        </span>
                      </div>
                    </td>
                    <td style={{ padding: "10px 12px" }}>
                      <span className={isDanger ? "badge-danger" : isWarning ? "badge-warning" : "badge-safe"} style={{ fontSize: "0.72rem" }}>
                        {row.risk_score}%
                      </span>
                    </td>
                    <td style={{ padding: "10px 12px", color: isDanger ? "#f87171" : isWarning ? "#fbbf24" : "#34d399", fontWeight: 600 }}>
                      {row.threat_tier || (isDanger ? "HIGH RISK — AI CLONE" : isWarning ? "SUSPICIOUS ACOUSTICS" : "AUTHENTIC HUMAN VOICE")}
                    </td>
                    <td style={{ padding: "10px 12px" }}>
                      <div style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                        <span className="font-mono" style={{ color: "#a78bfa", fontSize: "0.72rem" }}>
                          {row.block_hash ? `${row.block_hash.slice(0, 10)}...${row.block_hash.slice(-6)}` : "—"}
                        </span>
                        {row.block_hash && (
                          <button
                            onClick={() => handleCopy(row.block_hash, row.id)}
                            style={{ background: "transparent", border: "none", color: "var(--text-muted)", cursor: "pointer" }}
                            title="Copy Hash"
                          >
                            {copiedId === row.id ? <Check size={12} color="#34d399" /> : <Copy size={12} />}
                          </button>
                        )}
                      </div>
                    </td>
                    <td style={{ padding: "10px 12px", color: "var(--text-muted)", fontSize: "0.72rem" }}>
                      {new Date(row.timestamp).toLocaleTimeString()}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

    </div>
  );
}
