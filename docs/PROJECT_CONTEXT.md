# VoiceShield: Project Context & Architectural Documentation

## Executive Overview
**VoiceShield** is an enterprise-grade AI voice clone & deepfake audio detection platform with a cryptographic SHA-256 blockchain audit ledger. It is engineered to solve voice authorization fraud (e.g. CEO voice scams, unauthorized wire transfers, emergency extortion scams) by combining multi-spectral acoustic feature extraction with an immutable proof-of-detection chain.

---

## 1. Machine Learning & Spectral Forensic Architecture

### Why Basic Models Fail (The "Always Safe" Detection Trap)
Many naive spoof detection systems fail against modern voice cloning (e.g., ElevenLabs, Tortoise, RVC) and mistakenly flag fake voices as "Safe". This happens for two primary reasons:
1. **Benchmark Domain Mismatch**: ASVspoof 2021 PA (Physical Access) is composed of *replay attacks* (human speech played through physical speakers), not neural vocoder synthesis. Replay attacks contain room reverberation, while neural vocoders generate pristine, clean digital waveforms.
2. **Loss of Temporal Dynamics**: Simple MFCC mean/std vectors discard the fine micro-prosody and harmonic phase alignments that characterize neural speech synthesis.

### Our Multi-Feature Solution (147 Acoustic Features):
- **MFCC + Delta + Delta-Delta (120 dims)**: Captures velocity and acceleration of vocal tract frequency shifts.
- **Spectral Flatness & Contrast (16 dims)**: Neural vocoders (HiFi-GAN, WaveGlow) exhibit unnatural mathematical smoothness and harmonic flattening.
- **High-Frequency Rolloff & Centroid (4 dims)**: Identifies Nyquist damping and high-frequency cutoff artifacts.
- **Pitch Micro-Jitter (F0 Tracking) (3 dims)**: Real human vocal cords have involuntary organic micro-tremors; neural clones have rigid step-interpolated pitch contours.
- **Zero-Crossing & RMS Energy Variance (4 dims)**: Captures acoustic breath dynamics vs digital noise floor.

---

## 2. Cryptographic Blockchain Audit Ledger

### Why Blockchain is Essential in Voice Fraud Prevention:
1. **Immutable Audit Trail**: When a voice transaction occurs, the raw audio's SHA-256 fingerprint, model confidence, risk score, and timestamp are sealed in a cryptographically chained block.
2. **Zero Tampering & Anti-Repudiation**: Rogue insiders or attackers cannot modify database records after the fact to conceal unauthorized transfers.
3. **Consortium Verification**: Multiple banking and security institutions can verify fraud attempts across a shared cryptographic ledger without exchanging sensitive PII audio files.

---

## 3. ASVspoof 2021 PA Dataset Notes for Pitch & Presentation

- **PA means Physical Access (Replay Attacks)**.
- In your pitch, emphasize:
  > *"Our detection engine is trained and benchmarked against standard ASVspoof 2021 PA evaluation baselines for replay defense, and augmented with high-dimensional vocoder spectral extraction (spectral flatness, pitch micro-jitter, and Nyquist rolloff) to achieve generalized detection of modern neural TTS/voice conversion clones."*
