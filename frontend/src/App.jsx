import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import AudioUploader from "./components/AudioUploader";
import RiskGauge from "./components/RiskGauge";
import AlertBanner from "./components/AlertBanner";
import AcousticMetrics from "./components/AcousticMetrics";
import LedgerView from "./components/LedgerView";
import HistoryTable from "./components/HistoryTable";
import PitchModal from "./components/PitchModal";
import { 
  analyzeAudio, 
  getLedger, 
  verifyLedger, 
  getHistory, 
  clearHistory as apiClearHistory, 
  checkHealth 
} from "./services/api";

export default function App() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  
  // Blockchain Ledger state
  const [ledgerData, setLedgerData] = useState({ chain: [], total_blocks: 1, is_valid: true });
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationResult, setVerificationResult] = useState(null);

  // History state
  const [historyList, setHistoryList] = useState([]);
  
  // Backend health state
  const [backendStatus, setBackendStatus] = useState("checking");
  const [isPitchOpen, setIsPitchOpen] = useState(false);

  const refreshAll = async () => {
    // Health check
    const health = await checkHealth();
    setBackendStatus(health.status === "online" ? "online" : "offline");

    // Load ledger
    try {
      const ledger = await getLedger();
      setLedgerData(ledger);
    } catch (e) {
      console.error("Ledger fetch error:", e);
    }

    // Load history
    try {
      const hist = await getHistory();
      setHistoryList(hist.history || []);
    } catch (e) {
      console.error("History fetch error:", e);
    }
  };

  // Initial load
  useEffect(() => {
    refreshAll();
  }, []);

  // Run Forensic Voice Clone Scan
  const handleAnalyze = async (fileOrBlob, scenario = "General Audio", customName) => {
    setIsAnalyzing(true);
    setVerificationResult(null);
    try {
      const res = await analyzeAudio(fileOrBlob, "General Audio", customName);
      setAnalysisResult(res);

      // Auto refresh ledger and history
      const [newLedger, newHistory] = await Promise.all([
        getLedger(),
        getHistory()
      ]);
      setLedgerData(newLedger);
      setHistoryList(newHistory.history || []);
    } catch (err) {
      alert("Analysis failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setIsAnalyzing(false);
    }
  };

  // Run Blockchain Chain Audit
  const handleVerifyLedger = async () => {
    setIsVerifying(true);
    try {
      const res = await verifyLedger();
      setVerificationResult(res);
      return res;
    } catch (err) {
      alert("Verification failed: " + err.message);
    } finally {
      setIsVerifying(false);
    }
  };

  // Clear SQLite history
  const handleClearHistory = async () => {
    try {
      await apiClearHistory();
      setHistoryList([]);
      alert("Scan history cleared successfully.");
    } catch (err) {
      alert("Failed to clear history: " + err.message);
    }
  };

  const scrollToLedger = () => {
    const el = document.getElementById("ledger-section");
    if (el) el.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", maxWidth: "1350px", margin: "0 auto" }}>
      
      {/* Navbar Header */}
      <Navbar
        blockchainValid={ledgerData.is_valid}
        totalBlocks={ledgerData.chain?.length || 1}
        onOpenPitch={() => setIsPitchOpen(true)}
        onOpenAudit={scrollToLedger}
        backendStatus={backendStatus}
      />

      {/* Main Content Area */}
      <main style={{ padding: "0 20px 40px 20px", flex: 1 }}>
        
        {/* Top Split Grid: Audio Input & Risk Assessment */}
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(380px, 1fr))",
          gap: "20px",
          marginBottom: "20px",
          alignItems: "stretch"
        }}>
          
          {/* Left Column: Audio Input Matrix */}
          <div>
            <AudioUploader
              onAnalyze={handleAnalyze}
              isAnalyzing={isAnalyzing}
            />
          </div>

          {/* Right Column: Continuous Acoustic Risk Gauge */}
          <div>
            <RiskGauge
              riskScore={analysisResult ? analysisResult.risk_score : 0}
              rawConfidence={analysisResult ? analysisResult.confidence : 0}
              acousticScore={analysisResult?.acoustic_frequency_score}
              threatTier={analysisResult?.threat_tier}
            />
          </div>

        </div>

        {/* Security Alert Banner */}
        {analysisResult && (
          <AlertBanner result={analysisResult} />
        )}

        {/* Forensic Acoustic Frequency Telemetry (147 Features) */}
        {analysisResult?.metrics && (
          <AcousticMetrics metrics={analysisResult.metrics} />
        )}

        {/* Blockchain Ledger Explorer Section */}
        <div id="ledger-section">
          <LedgerView
            chain={ledgerData.chain || []}
            onRefresh={async () => {
              const data = await getLedger();
              setLedgerData(data);
            }}
            onVerify={handleVerifyLedger}
            isVerifying={isVerifying}
            verificationResult={verificationResult}
          />
        </div>

        {/* Persistent Forensic History Table */}
        <HistoryTable
          history={historyList}
          onClear={handleClearHistory}
          onRefresh={async () => {
            const data = await getHistory();
            setHistoryList(data.history || []);
          }}
        />

      </main>

      {/* Technical Pitch & Architecture Modal */}
      <PitchModal
        isOpen={isPitchOpen}
        onClose={() => setIsPitchOpen(false)}
      />

      {/* Footer */}
      <footer style={{
        textAlign: "center",
        padding: "16px 20px",
        borderTop: "1px solid var(--border-subtle)",
        color: "var(--text-muted)",
        fontSize: "0.75rem"
      }}>
        VoiceShield Frequency-Based Acoustic Detection & SHA-256 Blockchain Audit Layer
      </footer>

    </div>
  );
}
