import React, { useState, useRef } from "react";
import { Upload, Mic, MicOff, Play, Pause, FileAudio, CheckCircle2, ShieldAlert, AlertCircle } from "lucide-react";

export default function AudioUploader({ onAnalyze, isAnalyzing }) {
  const [activeTab, setActiveTab] = useState("upload"); // "upload" or "mic"
  const [selectedFile, setSelectedFile] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  
  // Microphone recording states
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [recordingError, setRecordingError] = useState(null);

  const audioRef = useRef(null);
  const timerRef = useRef(null);
  const canvasRef = useRef(null);
  const animFrameRef = useRef(null);
  
  // Audio recorder refs
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const mediaStreamRef = useRef(null);
  const audioContextRef = useRef(null);

  // Handle file drop & select
  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setRecordedBlob(null);
      setIsPlaying(false);
      setRecordingError(null);
      if (audioUrl) URL.revokeObjectURL(audioUrl);
      setAudioUrl(URL.createObjectURL(file));
    }
  };

  // Toggle playback
  const togglePlay = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
      setIsPlaying(false);
    } else {
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  // --- Start Recording with Native High-Fidelity MediaRecorder ---
  const startRecording = async () => {
    try {
      setRecordingError(null);
      setRecordingDuration(0);
      setRecordedBlob(null);
      setSelectedFile(null);
      setIsPlaying(false);
      audioChunksRef.current = [];

      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: { 
          channelCount: 1, 
          echoCancellation: true, 
          noiseSuppression: true, 
          autoGainControl: true 
        } 
      });
      mediaStreamRef.current = stream;

      // Audio visualizer setup
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const audioCtx = new AudioCtx();
      audioContextRef.current = audioCtx;
      const source = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      drawLiveVisualizer(analyser);

      // Determine supported high-quality audio codec
      let mimeType = 'audio/webm;codecs=opus';
      if (!MediaRecorder.isTypeSupported(mimeType)) {
        mimeType = MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : (MediaRecorder.isTypeSupported('audio/mp4') ? 'audio/mp4' : '');
      }

      const mediaRecorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (e) => {
        if (e.data && e.data.size > 0) {
          audioChunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = async () => {
        try {
          const rawBlob = new Blob(audioChunksRef.current, { type: mediaRecorder.mimeType || 'audio/webm' });
          
          // Convert to uncompressed standard 16-bit PCM WAV for perfect acoustic fidelity
          const arrayBuffer = await rawBlob.arrayBuffer();
          const decodeCtx = new (window.AudioContext || window.webkitAudioContext)();
          const audioBuffer = await decodeCtx.decodeAudioData(arrayBuffer);
          const wavBlob = audioBufferToWav(audioBuffer);
          try { await decodeCtx.close(); } catch {}

          setRecordedBlob(wavBlob);
          if (audioUrl) URL.revokeObjectURL(audioUrl);
          setAudioUrl(URL.createObjectURL(wavBlob));
        } catch (convErr) {
          console.warn("WAV conversion fallback:", convErr);
          const fallbackBlob = new Blob(audioChunksRef.current, { type: mediaRecorder.mimeType || 'audio/webm' });
          setRecordedBlob(fallbackBlob);
          if (audioUrl) URL.revokeObjectURL(audioUrl);
          setAudioUrl(URL.createObjectURL(fallbackBlob));
        }
      };

      mediaRecorder.start(100);
      setIsRecording(true);

      timerRef.current = setInterval(() => {
        setRecordingDuration((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      setRecordingError("Microphone access failed: " + err.message);
    }
  };

  // Convert AudioBuffer to 16-bit mono PCM WAV Blob
  const audioBufferToWav = (buffer) => {
    const numOfChan = 1;
    const sampleRate = buffer.sampleRate;
    
    // Mix to mono
    let channelData;
    if (buffer.numberOfChannels > 1) {
      const ch0 = buffer.getChannelData(0);
      const ch1 = buffer.getChannelData(1);
      channelData = new Float32Array(ch0.length);
      for (let i = 0; i < ch0.length; i++) {
        channelData[i] = (ch0[i] + ch1[i]) / 2;
      }
    } else {
      channelData = buffer.getChannelData(0);
    }

    const length = channelData.length * 2 + 44;
    const out = new DataView(new ArrayBuffer(length));

    const writeString = (view, offset, string) => {
      for (let i = 0; i < string.length; i++) {
        view.setUint8(offset + i, string.charCodeAt(i));
      }
    };

    /* RIFF identifier */
    writeString(out, 0, 'RIFF');
    /* file length */
    out.setUint32(4, 36 + channelData.length * 2, true);
    /* RIFF type */
    writeString(out, 8, 'WAVE');
    /* format chunk identifier */
    writeString(out, 12, 'fmt ');
    /* format chunk length */
    out.setUint32(16, 16, true);
    /* sample format (1 = PCM) */
    out.setUint16(20, 1, true);
    /* channel count */
    out.setUint16(22, numOfChan, true);
    /* sample rate */
    out.setUint32(24, sampleRate, true);
    /* byte rate */
    out.setUint32(28, sampleRate * 2, true);
    /* block align */
    out.setUint16(32, 2, true);
    /* bits per sample */
    out.setUint16(34, 16, true);
    /* data chunk identifier */
    writeString(out, 36, 'data');
    /* data chunk length */
    out.setUint32(40, channelData.length * 2, true);

    // Write 16-bit PCM samples with clamping
    let offset = 44;
    for (let i = 0; i < channelData.length; i++, offset += 2) {
      const s = Math.max(-1, Math.min(1, channelData[i]));
      out.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }

    return new Blob([out], { type: 'audio/wav' });
  };

  // --- Stop Recording ---
  const stopRecording = () => {
    if (!isRecording) return;

    if (timerRef.current) clearInterval(timerRef.current);
    if (animFrameRef.current) cancelAnimationFrame(animFrameRef.current);

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }

    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
    }

    if (audioContextRef.current) {
      audioContextRef.current.close().catch(() => {});
    }

    setIsRecording(false);
  };

  const drawLiveVisualizer = (analyser) => {
    if (!canvasRef.current || !analyser) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const render = () => {
      animFrameRef.current = requestAnimationFrame(render);
      analyser.getByteFrequencyData(dataArray);

      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const barWidth = (canvas.width / bufferLength) * 2.4;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height * 0.95;
        const gradient = ctx.createLinearGradient(0, canvas.height, 0, 0);
        gradient.addColorStop(0, "#00f2fe");
        gradient.addColorStop(0.5, "#4facfe");
        gradient.addColorStop(1, "#8b5cf6");

        ctx.fillStyle = gradient;
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight);
        x += barWidth + 2;
      }
    };
    render();
  };

  // Submit for Forensic Analysis
  const handleAnalyzeClick = () => {
    if (activeTab === "upload" && selectedFile) {
      onAnalyze(selectedFile, "General Audio", selectedFile.name);
    } else if (activeTab === "mic" && recordedBlob) {
      const isWav = recordedBlob.type.includes('wav');
      const filename = isWav ? `Live_Voice_Capture_${Date.now()}.wav` : `Live_Voice_Capture_${Date.now()}.webm`;
      onAnalyze(recordedBlob, "General Audio", filename);
    }
  };

  const isReadyToAnalyze = 
    (activeTab === "upload" && selectedFile) ||
    (activeTab === "mic" && recordedBlob && !isRecording);

  return (
    <div className="glass-panel" style={{ padding: "20px" }}>
      
      {/* Tab Navigation: Upload & Microphone */}
      <div style={{
        display: "flex",
        background: "rgba(10, 14, 26, 0.8)",
        borderRadius: "12px",
        padding: "4px",
        marginBottom: "16px",
        border: "1px solid var(--border-subtle)"
      }}>
        <button
          onClick={() => {
            setActiveTab("upload");
            setIsPlaying(false);
          }}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "8px",
            border: "none",
            background: activeTab === "upload" ? "linear-gradient(135deg, rgba(0,242,254,0.15) 0%, rgba(79,172,254,0.2) 100%)" : "transparent",
            color: activeTab === "upload" ? "#00f2fe" : "var(--text-secondary)",
            fontWeight: 600,
            fontSize: "0.85rem",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
            transition: "all 0.2s"
          }}
        >
          <Upload size={16} />
          <span>Upload Audio File</span>
        </button>

        <button
          onClick={() => {
            setActiveTab("mic");
            setIsPlaying(false);
          }}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "8px",
            border: "none",
            background: activeTab === "mic" ? "linear-gradient(135deg, rgba(0,242,254,0.15) 0%, rgba(79,172,254,0.2) 100%)" : "transparent",
            color: activeTab === "mic" ? "#00f2fe" : "var(--text-secondary)",
            fontWeight: 600,
            fontSize: "0.85rem",
            cursor: "pointer",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: "8px",
            transition: "all 0.2s"
          }}
        >
          <Mic size={16} />
          <span>Live Microphone</span>
        </button>
      </div>

      {/* --- TAB 1: UPLOAD AUDIO FILE --- */}
      {activeTab === "upload" && (
        <div style={{ marginBottom: "16px" }}>
          <label style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            padding: "32px 16px",
            border: "2px dashed var(--border-subtle)",
            borderRadius: "12px",
            background: "rgba(13, 18, 31, 0.4)",
            cursor: "pointer",
            transition: "all 0.2s ease"
          }}>
            <input
              type="file"
              accept=".wav,.mp3,.flac,.ogg,.m4a,.webm"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
            <div style={{
              width: "48px",
              height: "48px",
              borderRadius: "50%",
              background: "rgba(0, 242, 254, 0.1)",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              marginBottom: "10px"
            }}>
              <FileAudio size={24} color="#00f2fe" />
            </div>
            <p style={{ fontWeight: 600, fontSize: "0.92rem", marginBottom: "4px" }}>
              {selectedFile ? selectedFile.name : "Click to select or drag audio file here"}
            </p>
            <p style={{ fontSize: "0.74rem", color: "var(--text-muted)" }}>
              Supports WAV, FLAC, MP3, OGG, M4A, WEBM
            </p>
          </label>
        </div>
      )}

      {/* --- TAB 2: LIVE MICROPHONE CAPTURE --- */}
      {activeTab === "mic" && (
        <div style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "22px 16px",
          background: "rgba(13, 18, 31, 0.5)",
          borderRadius: "12px",
          border: "1px solid var(--border-subtle)",
          marginBottom: "16px"
        }}>
          {/* Live Waveform Frequency Canvas */}
          <canvas
            ref={canvasRef}
            width={320}
            height={56}
            style={{
              width: "100%",
              maxWidth: "360px",
              height: "56px",
              borderRadius: "8px",
              background: "rgba(7, 9, 14, 0.8)",
              marginBottom: "14px"
            }}
          />

          <div style={{ display: "flex", alignItems: "center", gap: "14px", marginBottom: "8px" }}>
            {!isRecording ? (
              <button
                onClick={startRecording}
                className="btn-danger"
                style={{ padding: "11px 22px", fontSize: "0.9rem" }}
              >
                <Mic size={18} />
                <span>Start Voice Recording</span>
              </button>
            ) : (
              <button
                onClick={stopRecording}
                className="btn-primary"
                style={{
                  padding: "11px 22px",
                  fontSize: "0.9rem",
                  background: "linear-gradient(135deg, #ef4444 0%, #dc2626 100%)",
                  boxShadow: "0 0 20px rgba(239, 68, 68, 0.6)"
                }}
              >
                <MicOff size={18} />
                <span>Stop Recording ({recordingDuration}s)</span>
              </button>
            )}
          </div>

          {recordingError && (
            <div style={{ color: "#f87171", fontSize: "0.78rem", display: "flex", alignItems: "center", gap: "6px", marginTop: "6px" }}>
              <AlertCircle size={14} /> {recordingError}
            </div>
          )}

          {recordedBlob && !isRecording && (
            <div style={{ display: "flex", alignItems: "center", gap: "6px", color: "#34d399", fontSize: "0.78rem", marginTop: "4px" }}>
              <CheckCircle2 size={14} /> Voice audio captured ({recordingDuration}s). Ready to scan!
            </div>
          )}
        </div>
      )}

      {/* Audio Playback Preview */}
      {audioUrl && (
        <div style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: "10px 14px",
          background: "rgba(10, 14, 26, 0.9)",
          borderRadius: "8px",
          border: "1px solid var(--border-subtle)",
          marginBottom: "14px"
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
            <button
              onClick={togglePlay}
              style={{
                width: "34px",
                height: "34px",
                borderRadius: "50%",
                background: "#00f2fe",
                border: "none",
                color: "#030712",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                cursor: "pointer"
              }}
            >
              {isPlaying ? <Pause size={16} /> : <Play size={16} style={{ marginLeft: "2px" }} />}
            </button>
            <div>
              <span style={{ fontSize: "0.82rem", fontWeight: 600 }}>
                {selectedFile ? selectedFile.name : `Live Voice Capture (${recordingDuration}s)`}
              </span>
              <p style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>
                Audio Loaded for Frequency & Acoustic Telemetry Analysis
              </p>
            </div>
          </div>

          <audio
            ref={audioRef}
            src={audioUrl}
            onEnded={() => setIsPlaying(false)}
            style={{ display: "none" }}
          />
        </div>
      )}

      {/* Primary Action Button */}
      <button
        onClick={handleAnalyzeClick}
        disabled={!isReadyToAnalyze || isAnalyzing}
        className="btn-primary"
        style={{
          width: "100%",
          padding: "13px",
          fontSize: "0.95rem",
          justifyContent: "center",
          opacity: !isReadyToAnalyze || isAnalyzing ? 0.5 : 1,
          cursor: !isReadyToAnalyze || isAnalyzing ? "not-allowed" : "pointer"
        }}
      >
        {isAnalyzing ? (
          <>
            <div style={{
              width: "16px",
              height: "16px",
              border: "2px solid #030712",
              borderTopColor: "transparent",
              borderRadius: "50%",
              animation: "spin-slow 1s linear infinite"
            }} />
            <span>Analyzing Acoustic Frequencies & Minting Block...</span>
          </>
        ) : (
          <>
            <ShieldAlert size={18} />
            <span>
              {activeTab === "mic" 
                ? (recordedBlob ? "Scan Recorded Microphone Audio" : "Record Audio to Scan")
                : (selectedFile ? "Scan Uploaded Audio File" : "Select Audio File to Scan")}
            </span>
          </>
        )}
      </button>

    </div>
  );
}
