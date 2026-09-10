import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("backend"))

def test_api():
    print("Testing SwarX System End-to-End...")
    
    # Import FastAPI TestClient
    from fastapi.testclient import TestClient
    from backend.main import app

    client = TestClient(app)

    # 1. Health Check
    res = client.get("/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    print("[OK] Health Check: OK ->", res.json())

    # 2. Get Sample Audios
    res = client.get("/sample-audios")
    assert res.status_code == 200
    samples = res.json()["samples"]
    print(f"[OK] Sample Audios: OK -> Found {len(samples)} presets")

    # 3. Analyze Real Audio Sample
    real_sample_path = "backend/sample_audio/legitimate_ceo_voice.wav"
    with open(real_sample_path, "rb") as f:
        res = client.post("/analyze-audio", files={"audio": ("legitimate_ceo_voice.wav", f, "audio/wav")}, data={"scenario": "Bank Transfer / Wire Authorization"})
    assert res.status_code == 200, f"Real audio analysis failed: {res.text}"
    real_data = res.json()
    print("[OK] Real Voice Scan: OK -> Verdict:", real_data["verdict"], f"(Risk: {real_data['risk_score']}%)", "Block Hash:", real_data["blockchain"]["block_hash"][:16] + "...")
    assert real_data["verdict"] == "safe", f"Expected 'safe', got {real_data['verdict']}"

    # 4. Analyze AI Cloned Audio Sample
    fake_sample_path = "backend/sample_audio/ai_clone_emergency_scam.wav"
    with open(fake_sample_path, "rb") as f:
        res = client.post("/analyze-audio", files={"audio": ("ai_clone_emergency_scam.wav", f, "audio/wav")}, data={"scenario": "Executive Impersonation / CEO Fraud"})
    assert res.status_code == 200, f"Fake audio analysis failed: {res.text}"
    fake_data = res.json()
    print("[OK] Fake Voice Scan: OK -> Verdict:", fake_data["verdict"], f"(Risk: {fake_data['risk_score']}%)", "Block Hash:", fake_data["blockchain"]["block_hash"][:16] + "...")
    assert fake_data["verdict"] in ("suspicious", "critical_clone"), f"Expected 'suspicious' or 'critical_clone', got {fake_data['verdict']}"

    # 5. Verify Blockchain Ledger
    res = client.get("/ledger")
    assert res.status_code == 200
    ledger = res.json()
    print(f"[OK] Ledger View: OK -> Total Blocks in Chain: {ledger['total_blocks']}")

    # 6. Run Cryptographic Audit Verification
    res = client.get("/ledger/verify")
    assert res.status_code == 200
    audit = res.json()
    print("[OK] Cryptographic Audit: OK -> Valid:", audit["valid"], f"(All {audit['total_blocks']} blocks chained & verified)")
    assert audit["valid"] is True, "Blockchain verification failed"

    # 7. Check SQLite History
    res = client.get("/history")
    assert res.status_code == 200
    hist = res.json()
    print(f"[OK] History DB: OK -> {hist['count']} scans stored in history.db")

    print("\n" + "=" * 50)
    print("ALL END-TO-END AUTOMATED VERIFICATION CHECKS PASSED!")
    print("=" * 50)

if __name__ == "__main__":
    test_api()
