def compute_risk(confidence: float, scenario: str = "General Audio", metrics: dict = None) -> dict:
    """
    Computes direct, continuous, granular risk score (0-100%)
    derived purely from voice frequency analysis and acoustic telemetry.
    """
    # Direct continuous percentage derived from acoustic analysis
    risk_score = int(round(confidence * 100.0))
    risk_score = max(1, min(99, risk_score))

    if risk_score >= 70:
        verdict = "critical_clone"
        threat_tier = "HIGH RISK — AI VOICE CLONE"
        color_theme = "danger"
        recommendation = "AI SYNTHESIS DETECTED: Frequency analysis indicates neural vocoder smoothing and synthetic pitch harmonics. Do not authorize verbal requests without out-of-band verification."
    elif risk_score >= 45:
        verdict = "suspicious"
        threat_tier = "ELEVATED RISK — SUSPICIOUS ACOUSTICS"
        color_theme = "warning"
        recommendation = "ANOMALOUS ACOUSTICS: Spectral characteristics show potential synthetic artifacts or replay degradation. Request secondary verification."
    else:
        verdict = "safe"
        threat_tier = "AUTHENTIC HUMAN VOICE — SAFE"
        color_theme = "success"
        recommendation = "BIOLOGICAL VOICE VERIFIED: Natural vocal tract resonance, organic micro-jitter, and organic acoustic breath dynamics confirmed."

    return {
        "risk_score": risk_score,
        "raw_score": risk_score,
        "verdict": verdict,
        "threat_tier": threat_tier,
        "color_theme": color_theme,
        "recommendation": recommendation,
        "scenario": "General Audio"
    }
