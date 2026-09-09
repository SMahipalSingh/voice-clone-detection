import React from "react";
import { X, ShieldAlert, Link2, Award, Zap } from "lucide-react";

export default function PitchModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  return (
    <div style={{
      position: "fixed",
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: "rgba(3, 7, 18, 0.85)",
      backdropFilter: "blur(12px)",
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      zIndex: 1000,
      padding: "20px"
    }}>
      <div className="glass-panel" style={{
        maxWidth: "780px",
        width: "100%",
        maxHeight: "90vh",
        overflowY: "auto",
        padding: "32px",
        background: "rgba(13, 18, 31, 0.95)",
        border: "1.5px solid rgba(0, 242, 254, 0.3)",
        boxShadow: "0 25px 60px rgba(0,0,0,0.8), 0 0 30px rgba(0,242,254,0.15)",
        position: "relative"
      }}>
        {/* Close Button */}
        <button
          onClick={onClose}
          style={{
            position: "absolute",
            top: "20px",
            right: "20px",
            background: "rgba(255,255,255,0.06)",
            border: "1px solid var(--border-subtle)",
            borderRadius: "50%",
            width: "36px",
            height: "36px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            color: "var(--text-secondary)",
            cursor: "pointer"
          }}
        >
          <X size={18} />
        </button>

        {/* Header */}
        <div style={{ marginBottom: "24px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "8px" }}>
            <span className="badge-blockchain">
              <Award size={13} /> TECHNICAL PITCH & RATIONALE
            </span>
            <span className="badge-safe">
              ASVSPOOF 2021 PA + NEURAL VOCODER
            </span>
          </div>
          <h2 style={{ fontSize: "1.5rem", fontWeight: 800, color: "var(--text-primary)" }}>
            VoiceShield: Generalized AI Voice Clone Detection & Blockchain Registry
          </h2>
          <p style={{ fontSize: "0.85rem", color: "var(--text-secondary)", marginTop: "4px" }}>
            Comprehensive architectural breakdown and judge Q&A guide.
          </p>
        </div>

        {/* Section 1: The Problem */}
        <div style={{ marginBottom: "20px", background: "rgba(10, 14, 26, 0.6)", padding: "18px", borderRadius: "12px", border: "1px solid var(--border-subtle)" }}>
          <h4 style={{ fontSize: "0.95rem", fontWeight: 700, color: "#00f2fe", display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
            <ShieldAlert size={18} /> 1. The Core Problem & The "Safe" Detection Trap
          </h4>
          <p style={{ fontSize: "0.82rem", color: "var(--text-secondary)", lineHeight: "1.5", marginBottom: "8px" }}>
            Standard spoof classifiers trained solely on simple MFCC averages or replay benchmarks (like ASVspoof PA alone) frequently classify modern neural clones (ElevenLabs, Tortoise, RVC) as <strong>"SAFE"</strong>. This occurs because neural vocoders generate clean audio without room reverberation.
          </p>
          <p style={{ fontSize: "0.82rem", color: "#34d399", fontWeight: 600 }}>
            ✓ How VoiceShield Solves This: We extract 147 forensic acoustic features—including pitch micro-prosody jitter, spectral flatness, high-frequency vocoder Nyquist damping, and spectral contrast derivatives.
          </p>
        </div>

        {/* Section 2: Why Blockchain? */}
        <div style={{ marginBottom: "20px", background: "rgba(10, 14, 26, 0.6)", padding: "18px", borderRadius: "12px", border: "1px solid var(--border-subtle)" }}>
          <h4 style={{ fontSize: "0.95rem", fontWeight: 700, color: "#a78bfa", display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
            <Link2 size={18} /> 2. Why Blockchain Here? (Consortium Fraud Audit Layer)
          </h4>
          <ul style={{ fontSize: "0.82rem", color: "var(--text-secondary)", lineHeight: "1.5", paddingLeft: "20px" }}>
            <li style={{ marginBottom: "6px" }}>
              <strong>Tamper-Evident Chain:</strong> When an executive or banking customer authorizes a transaction via voice, the voice fingerprint (SHA-256) and risk score are committed to an immutable cryptographic block.
            </li>
            <li style={{ marginBottom: "6px" }}>
              <strong>Zero Repudiation:</strong> Attackers or malicious insiders cannot alter historical fraud audit logs to erase detection traces.
            </li>
            <li>
              <strong>Inter-Bank Consortium Verification:</strong> Multiple institutions can cryptographically audit voice fraud attempts without sharing sensitive PII audio files.
            </li>
          </ul>
        </div>

        {/* Section 3: Dataset Nuance (ASVspoof 2021 PA) */}
        <div style={{ marginBottom: "24px", background: "rgba(10, 14, 26, 0.6)", padding: "18px", borderRadius: "12px", border: "1px solid var(--border-subtle)" }}>
          <h4 style={{ fontSize: "0.95rem", fontWeight: 700, color: "#fbbf24", display: "flex", alignItems: "center", gap: "8px", marginBottom: "8px" }}>
            <Zap size={18} /> 3. Pitch Strategy: ASVspoof 2021 PA Nuance
          </h4>
          <p style={{ fontSize: "0.82rem", color: "var(--text-secondary)", lineHeight: "1.5" }}>
            <em>"Our model is trained and validated on ASVspoof 2021 PA (replay-attack detection); the same spectral-artifact detection approach extends to synthetic voice cloning, and we additionally tested it against neural TTS-generated samples to demonstrate generalized robustness."</em>
          </p>
        </div>

        <button
          onClick={onClose}
          className="btn-primary"
          style={{ width: "100%", justifyContent: "center", padding: "12px" }}
        >
          Close & Return to Dashboard
        </button>

      </div>
    </div>
  );
}
