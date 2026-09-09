import React, { useState } from "react";
import { Link2, ShieldCheck, AlertOctagon, CheckCircle2, Copy, Check, Search, RefreshCw, Layers, Lock } from "lucide-react";
import confetti from "canvas-confetti";

export default function LedgerView({ 
  chain = [], 
  onRefresh, 
  onVerify, 
  isVerifying, 
  verificationResult 
}) {
  const [searchTerm, setSearchTerm] = useState("");
  const [copiedHash, setCopiedHash] = useState(null);

  const handleCopy = (text, id) => {
    navigator.clipboard.writeText(text);
    setCopiedHash(id);
    setTimeout(() => setCopiedHash(null), 2000);
  };

  const handleRunAudit = async () => {
    if (onVerify) {
      const res = await onVerify();
      if (res?.valid) {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.7 }
        });
      }
    }
  };

  const filteredChain = chain.filter((b) => {
    const term = searchTerm.toLowerCase();
    return (
      b.hash?.toLowerCase().includes(term) ||
      b.filename?.toLowerCase().includes(term) ||
      b.scenario?.toLowerCase().includes(term) ||
      b.verdict?.toLowerCase().includes(term) ||
      String(b.index).includes(term)
    );
  });

  return (
    <div className="glass-panel" style={{ padding: "24px", marginBottom: "24px" }}>
      
      {/* Header with Blockchain Audit Controls */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: "16px", marginBottom: "20px" }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <h3 style={{ fontSize: "1.1rem", fontWeight: 700, display: "flex", alignItems: "center", gap: "8px" }}>
              <Layers size={20} color="#8b5cf6" />
              <span>Immutable Blockchain Audit Ledger</span>
            </h3>
            <span className="badge-blockchain">
              <Lock size={12} /> SHA-256 Chained
            </span>
          </div>
          <p style={{ fontSize: "0.78rem", color: "var(--text-secondary)", marginTop: "4px" }}>
            Decentralized tamper-evident registry storing audio hashes, risk scores, and forensic verdicts.
          </p>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: "10px", flexWrap: "wrap" }}>
          {/* Audit Verification Button */}
          <button
            onClick={handleRunAudit}
            disabled={isVerifying}
            className="btn-primary"
            style={{
              background: "linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%)",
              boxShadow: "0 4px 14px rgba(139, 92, 246, 0.4)",
              fontSize: "0.85rem",
              padding: "9px 16px"
            }}
          >
            <ShieldCheck size={16} />
            <span>{isVerifying ? "Verifying SHA-256 Signatures..." : "Run Cryptographic Audit"}</span>
          </button>

          <button
            onClick={onRefresh}
            className="btn-secondary"
            style={{ fontSize: "0.85rem", padding: "9px 14px" }}
            title="Refresh Ledger"
          >
            <RefreshCw size={15} />
          </button>
        </div>
      </div>

      {/* Verification Status Banner (if audited) */}
      {verificationResult && (
        <div style={{
          padding: "12px 18px",
          borderRadius: "10px",
          background: verificationResult.valid ? "rgba(16, 185, 129, 0.12)" : "rgba(239, 68, 68, 0.15)",
          border: `1px solid ${verificationResult.valid ? "rgba(16, 185, 129, 0.4)" : "rgba(239, 68, 68, 0.4)"}`,
          marginBottom: "18px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          flexWrap: "wrap",
          gap: "10px"
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            {verificationResult.valid ? (
              <CheckCircle2 size={20} color="#34d399" />
            ) : (
              <AlertOctagon size={20} color="#f87171" />
            )}
            <div>
              <span style={{ fontWeight: 700, fontSize: "0.88rem", color: verificationResult.valid ? "#34d399" : "#f87171" }}>
                {verificationResult.valid ? "Cryptographic Chain Integrity 100% Intact" : "Ledger Tampering Detected!"}
              </span>
              <p style={{ fontSize: "0.74rem", color: "var(--text-secondary)" }}>
                {verificationResult.valid
                  ? `All ${verificationResult.total_blocks} blocks verified via SHA-256 hash recursion. Zero data alterations detected.`
                  : verificationResult.reason}
              </p>
            </div>
          </div>
          <span className="font-mono" style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>
            Root: {verificationResult.latest_block_hash?.slice(0, 16)}...
          </span>
        </div>
      )}

      {/* Search Input */}
      <div style={{ position: "relative", marginBottom: "16px" }}>
        <Search size={16} color="var(--text-muted)" style={{ position: "absolute", left: "14px", top: "50%", transform: "translateY(-50%)" }} />
        <input
          type="text"
          placeholder="Filter blocks by Hash, Audio Filename, Scenario, or Verdict..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: "100%",
            background: "rgba(10, 14, 26, 0.7)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "10px",
            padding: "10px 14px 10px 40px",
            color: "var(--text-primary)",
            fontSize: "0.85rem",
            outline: "none"
          }}
        />
      </div>

      {/* Visual Block Cards Chain */}
      <div style={{
        display: "flex",
        flexDirection: "column",
        gap: "14px",
        maxHeight: "460px",
        overflowY: "auto",
        paddingRight: "6px"
      }}>
        {filteredChain.map((block) => {
          const isGenesis = block.index === 0;
          const isDanger = block.risk_score >= 70;
          const isWarning = block.risk_score >= 45 && block.risk_score < 70;

          return (
            <div
              key={block.index}
              style={{
                background: isGenesis 
                  ? "linear-gradient(135deg, rgba(139,92,246,0.12) 0%, rgba(13,18,31,0.8) 100%)" 
                  : "rgba(13, 18, 31, 0.6)",
                border: isGenesis 
                  ? "1.5px solid rgba(139, 92, 246, 0.4)" 
                  : "1px solid var(--border-subtle)",
                borderRadius: "12px",
                padding: "16px",
                transition: "all 0.2s ease"
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: "10px", marginBottom: "10px" }}>
                <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
                  <div style={{
                    width: "32px",
                    height: "32px",
                    borderRadius: "8px",
                    background: isGenesis ? "rgba(139, 92, 246, 0.25)" : "rgba(0, 242, 254, 0.15)",
                    border: `1px solid ${isGenesis ? "#8b5cf6" : "#00f2fe"}`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontWeight: 700,
                    fontSize: "0.85rem",
                    color: isGenesis ? "#c084fc" : "#00f2fe"
                  }}>
                    #{block.index}
                  </div>
                  <div>
                    <span style={{ fontWeight: 600, fontSize: "0.9rem", color: "var(--text-primary)" }}>
                      {isGenesis ? "Genesis Block (Consortium Root)" : block.filename}
                    </span>
                    <p style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>
                      Timestamp: {new Date(block.timestamp).toLocaleString()} | Scenario: {block.scenario}
                    </p>
                  </div>
                </div>

                {/* Verdict Badge */}
                {!isGenesis && (
                  <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                    <span className={isDanger ? "badge-danger" : isWarning ? "badge-warning" : "badge-safe"}>
                      Risk: {block.risk_score}% ({block.verdict.toUpperCase()})
                    </span>
                  </div>
                )}
              </div>

              {/* Hash Cryptographic Proof */}
              <div style={{
                background: "rgba(7, 9, 14, 0.8)",
                padding: "10px 14px",
                borderRadius: "8px",
                fontSize: "0.74rem",
                display: "grid",
                gridTemplateColumns: "auto 1fr auto",
                gap: "10px",
                alignItems: "center"
              }}>
                <span style={{ color: "var(--text-muted)", fontWeight: 600 }}>BLOCK HASH:</span>
                <span className="font-mono" style={{ color: "#a78bfa", wordBreak: "break-all" }}>
                  {block.hash}
                </span>
                <button
                  onClick={() => handleCopy(block.hash, `hash-${block.index}`)}
                  style={{ background: "transparent", border: "none", color: "var(--text-secondary)", cursor: "pointer" }}
                  title="Copy SHA-256 Hash"
                >
                  {copiedHash === `hash-${block.index}` ? <Check size={14} color="#34d399" /> : <Copy size={14} />}
                </button>
              </div>

              {/* Parent Hash Pointer */}
              <div style={{ display: "flex", alignItems: "center", gap: "8px", marginTop: "8px", fontSize: "0.7rem", color: "var(--text-muted)" }}>
                <Link2 size={12} color="#8b5cf6" />
                <span>Prev Hash:</span>
                <span className="font-mono" style={{ color: "var(--text-secondary)" }}>
                  {block.prev_hash.slice(0, 24)}...{block.prev_hash.slice(-8)}
                </span>
                <span style={{ marginLeft: "auto", color: "#34d399", fontWeight: 600 }}>
                  [ {block.signature_status} ]
                </span>
              </div>

            </div>
          );
        })}
      </div>

    </div>
  );
}
