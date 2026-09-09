import numpy as np
import librosa  # type: ignore # pyrefly: ignore [missing-import]
import soundfile as sf  # type: ignore # pyrefly: ignore [missing-import]
import os

# Configure bundled ffmpeg for pydub fallback decoding
try:
    import pydub  # type: ignore
    import imageio_ffmpeg  # type: ignore
    pydub.AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()
    pydub.utils.get_prober_name = lambda: imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    pass

def extract_features(audio_path_or_bytes, sr=16000, n_mfcc=20):
    """
    Extracts comprehensive forensic audio features specifically designed to detect:
    1. Modern Neural AI Voice Clones (ElevenLabs, RVC, VALL-E, HiFi-GAN vocoder smoothing)
    2. Replay & Physical Access spoofing attacks (ASVspoof 2021 PA)
    3. Classic Concatenative/Parametric TTS artifacts
    
    Returns:
        feature_vector: 1D numpy array for ML model input
        metrics: dict of interpretable forensic indicators
    """
    try:
        if isinstance(audio_path_or_bytes, str):
            try:
                y, orig_sr = librosa.load(audio_path_or_bytes, sr=sr)
            except Exception:
                try:
                    y, orig_sr = sf.read(audio_path_or_bytes)
                    if orig_sr != sr:
                        y = librosa.resample(y, orig_sr=orig_sr, target_sr=sr)
                except Exception:
                    # Fallback for compressed/exotic containers using pydub
                    from pydub import AudioSegment  # type: ignore # pyrefly: ignore [missing-import]
                    seg = AudioSegment.from_file(audio_path_or_bytes)
                    seg = seg.set_frame_rate(sr).set_channels(1)
                    samples = np.array(seg.get_array_of_samples(), dtype=np.float32)
                    max_val = float(2 ** (seg.sample_width * 8 - 1))
                    y = samples / (max_val + 1e-6)
                    orig_sr = sr
        else:
            y, orig_sr = sf.read(audio_path_or_bytes)
            if orig_sr != sr:
                y = librosa.resample(y, orig_sr=orig_sr, target_sr=sr)
    except Exception as e:
        raise ValueError(f"Unable to decode audio file: {e}")

    # Ensure mono
    if y.ndim > 1:
        y = np.mean(y, axis=1)

    # Trim silence
    if len(y) > sr * 0.2:
        y_trimmed, _ = librosa.effects.trim(y, top_db=30)
        if len(y_trimmed) >= sr * 0.3:
            y = y_trimmed

    # Amplitude Peak Normalization (Standardize dynamic range across all devices & gain levels)
    max_amp = np.max(np.abs(y))
    if max_amp > 1e-4:
        y = (y / max_amp) * 0.90

    # Pad if very short
    min_len = int(sr * 0.5)
    if len(y) < min_len:
        y = np.pad(y, (0, min_len - len(y)), mode='constant')

    duration = len(y) / sr

    # --- 1. MFCCs + First & Second Derivatives (Delta & Delta-Delta) ---
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=1024, hop_length=256)
    mfcc_delta = librosa.feature.delta(mfcc)
    mfcc_delta2 = librosa.feature.delta(mfcc, order=2)

    mfcc_mean = np.mean(mfcc, axis=1)
    mfcc_std = np.std(mfcc, axis=1)
    delta_mean = np.mean(mfcc_delta, axis=1)
    delta_std = np.std(mfcc_delta, axis=1)
    delta2_mean = np.mean(mfcc_delta2, axis=1)
    delta2_std = np.std(mfcc_delta2, axis=1)

    # --- 2. Spectral Flatness & Contrast (Neural Vocoder Smoothing Detection) ---
    # Neural vocoders (HiFi-GAN/WaveGlow) create unnatural spectral smoothness/flatness patterns
    flatness = librosa.feature.spectral_flatness(y=y, n_fft=1024, hop_length=256)
    flatness_mean = float(np.mean(flatness))
    flatness_std = float(np.std(flatness))

    contrast = librosa.feature.spectral_contrast(y=y, sr=sr, n_fft=1024, hop_length=256)
    contrast_mean = np.mean(contrast, axis=1)
    contrast_std = np.std(contrast, axis=1)

    # --- 3. Spectral Centroid & High-Frequency Rolloff ---
    # AI vocoders frequently exhibit artificial high-frequency damping above 8kHz-12kHz
    rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
    rolloff_mean = float(np.mean(rolloff))
    rolloff_std = float(np.std(rolloff))

    centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    centroid_mean = float(np.mean(centroid))
    centroid_std = float(np.std(centroid))

    # --- 4. Zero Crossing Rate & Energy Variance ---
    zcr = librosa.feature.zero_crossing_rate(y)
    zcr_mean = float(np.mean(zcr))
    zcr_std = float(np.std(zcr))

    rms = librosa.feature.rms(y=y)
    rms_mean = float(np.mean(rms))
    rms_std = float(np.std(rms))

    # --- 5. Robust YIN Fundamental Frequency (F0) Tracking & Voiced Micro-Prosody Jitter ---
    try:
        f0 = librosa.yin(y, fmin=65, fmax=500, sr=sr, frame_length=1024, hop_length=256)
        frame_rms = librosa.feature.rms(y=y, frame_length=1024, hop_length=256)[0]
        min_rms = np.mean(frame_rms) * 0.25
        voiced_mask = (frame_rms >= min_rms) & (f0 >= 65) & (f0 <= 500)
        voiced_f0 = f0[voiced_mask]
        
        if len(voiced_f0) > 4:
            f0_mean = float(np.median(voiced_f0))
            f0_std = float(np.std(voiced_f0))
            diffs = np.abs(np.diff(voiced_f0))
            smooth_diffs = diffs[diffs < 45.0]
            if len(smooth_diffs) > 2:
                jitter = float(np.mean(smooth_diffs) / (f0_mean + 1e-6))
            else:
                jitter = 0.018
        else:
            f0_mean, f0_std, jitter = 145.0, 8.0, 0.018
    except Exception:
        f0_mean, f0_std, jitter = 145.0, 8.0, 0.018

    # Assemble comprehensive 1D feature vector
    feature_vector = np.concatenate([
        mfcc_mean,       # 20
        mfcc_std,        # 20
        delta_mean,      # 20
        delta_std,       # 20
        delta2_mean,     # 20
        delta2_std,      # 20
        [flatness_mean, flatness_std], # 2
        contrast_mean,   # 7
        contrast_std,    # 7
        [rolloff_mean, rolloff_std],   # 2
        [centroid_mean, centroid_std], # 2
        [zcr_mean, zcr_std],           # 2
        [rms_mean, rms_std],           # 2
        [f0_mean, f0_std, jitter]      # 3
    ])

    # Human-interpretable metrics
    metrics = {
        "duration_seconds": round(duration, 2),
        "spectral_flatness": round(flatness_mean, 5),
        "spectral_rolloff_hz": round(rolloff_mean, 1),
        "spectral_centroid_hz": round(centroid_mean, 1),
        "pitch_f0_mean_hz": round(f0_mean, 1),
        "pitch_micro_jitter": round(jitter, 4),
        "zero_crossing_rate": round(zcr_mean, 4),
        "energy_rms": round(rms_mean, 4)
    }

    return feature_vector, metrics
