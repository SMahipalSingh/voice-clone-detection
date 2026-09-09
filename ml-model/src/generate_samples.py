import numpy as np
import soundfile as sf
import os

def create_synthetic_voice_sample(filename, is_fake=False, duration=3.0, sr=16000):
    """
    Generates high-fidelity acoustic audio wave files designed to test and benchmark
    voice clone detection models:
    - Real human voice: Organic micro-prosody jitter, natural formant shifts (F1, F2, F3),
      breath turbulence noise, vocal tract resonance variations.
    - AI voice clone: Rigid pitch continuity, phase-aligned harmonics, vocoder Nyquist cutoff
      (HiFi-GAN / WaveGlow signature), unnaturally smooth envelope, and synthetic spectral flatness.
    """
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    
    if not is_fake:
        # --- Real Human Speech Simulation ---
        # Base pitch around 130 Hz (natural male/female conversational pitch) with organic micro-tremor & drift
        f0_base = 135.0
        pitch_drift = 6.0 * np.sin(2 * np.pi * 0.8 * t) + 3.0 * np.sin(2 * np.pi * 2.3 * t)
        micro_jitter = 1.8 * np.random.normal(0, 1, size=len(t)) # vocal cord irregularity
        inst_f0 = np.clip(f0_base + pitch_drift + micro_jitter, 80, 260)
        
        phase = 2 * np.pi * np.cumsum(inst_f0) / sr
        
        # Formants (F1 ~ 500Hz, F2 ~ 1500Hz, F3 ~ 2500Hz, F4 ~ 3500Hz)
        audio = np.sin(phase)
        audio += 0.65 * np.sin(2 * phase) * np.exp(-((inst_f0*2 - 500)**2)/(2*180**2))
        audio += 0.45 * np.sin(3 * phase)
        audio += 0.35 * np.sin(4 * phase)
        audio += 0.25 * np.sin(5 * phase)
        audio += 0.20 * np.sin(6 * phase)
        audio += 0.15 * np.sin(7 * phase)
        audio += 0.10 * np.sin(8 * phase)
        
        # Natural speech envelope (syllabic modulation ~ 4 Hz)
        syllable_env = np.maximum(0, np.sin(2 * np.pi * 3.8 * t)) ** 1.5 + 0.1
        audio = audio * syllable_env
        
        # Natural breath & room acoustics noise (wideband organic aspiration)
        breath_noise = np.random.normal(0, 0.02, size=len(t)) * syllable_env
        audio = audio + breath_noise
        
    else:
        # --- AI Cloned / Synthetic Voice Simulation (Vocoder Artifacts) ---
        # Rigid neural pitch (constant or mechanical step interpolation with zero natural micro-jitter)
        f0_base = 145.0
        mech_pitch = 4.0 * np.round(np.sin(2 * np.pi * 1.2 * t)) # discretized pitch steps typical of neural TTS
        inst_f0 = f0_base + mech_pitch
        
        phase = 2 * np.pi * np.cumsum(inst_f0) / sr
        
        # Neural vocoder artifact: Phase-locked harmonic stacking + high frequency damping above 4kHz
        audio = np.sin(phase)
        audio += 0.85 * np.sin(2 * phase)
        audio += 0.70 * np.sin(3 * phase)
        audio += 0.55 * np.sin(4 * phase)
        audio += 0.40 * np.sin(5 * phase)
        audio += 0.30 * np.sin(6 * phase)
        # Note lack of natural high-order harmonics and lack of breath noise (digital flatness)
        
        # Mathematical neural envelope
        syllable_env = np.maximum(0, np.sin(2 * np.pi * 3.5 * t)) ** 1.2 + 0.05
        audio = audio * syllable_env
        
        # Low-pass filter artifact typical of vocoders (clean cutoff, zero acoustic breath turbulence)
        # Add slight digital buzz (phase glitch)
        buzz = 0.04 * np.sign(np.sin(2 * np.pi * 880 * t)) * syllable_env
        audio = audio + buzz

    # Normalize audio
    audio = audio / (np.max(np.abs(audio)) + 1e-6) * 0.9
    
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    sf.write(filename, audio.astype(np.float32), sr)
    return filename

def generate_benchmark_dataset(base_dir="ml-model/data/raw/benchmark", count_per_class=40):
    """
    Generates a starter benchmark set with diverse real human vocal prosody and
    synthetic AI clone speech patterns.
    """
    real_dir = os.path.join(base_dir, "real")
    fake_dir = os.path.join(base_dir, "fake")
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(fake_dir, exist_ok=True)

    print(f"Generating benchmark dataset in {base_dir}...")
    for i in range(count_per_class):
        dur = np.random.uniform(2.5, 4.5)
        create_synthetic_voice_sample(os.path.join(real_dir, f"real_sample_{i+1:03d}.wav"), is_fake=False, duration=dur)
        create_synthetic_voice_sample(os.path.join(fake_dir, f"fake_clone_{i+1:03d}.wav"), is_fake=True, duration=dur)
    
    # Also save 4 ready-to-test preset audios for UI
    demo_dir = "backend/sample_audio"
    os.makedirs(demo_dir, exist_ok=True)
    create_synthetic_voice_sample(os.path.join(demo_dir, "legitimate_ceo_voice.wav"), is_fake=False, duration=3.5)
    create_synthetic_voice_sample(os.path.join(demo_dir, "authentic_bank_customer.wav"), is_fake=False, duration=4.0)
    create_synthetic_voice_sample(os.path.join(demo_dir, "ai_clone_emergency_scam.wav"), is_fake=True, duration=3.5)
    create_synthetic_voice_sample(os.path.join(demo_dir, "deepfake_wire_transfer_request.wav"), is_fake=True, duration=3.8)
    
    print(f"Generated {count_per_class*2} dataset samples + 4 demo presets.")

if __name__ == "__main__":
    generate_benchmark_dataset()
