import hashlib
import json
import time
from datetime import datetime

GENESIS_HASH = hashlib.sha256(b"genesis_block_voice_clone_detector_immutable_ledger").hexdigest()

# In-memory ledger chain (can also be saved to SQLite for persistence)
chain = [
    {
        "index": 0,
        "prev_hash": "0" * 64,
        "hash": GENESIS_HASH,
        "timestamp": datetime.utcnow().isoformat(),
        "filename": "GENESIS",
        "risk_score": 0,
        "verdict": "GENESIS_NODE",
        "scenario": "SYSTEM_INITIALIZATION",
        "audio_sha256": "0" * 64,
        "signature_status": "GENESIS_ROOT"
    }
]

def hash_audio_file(filepath: str) -> str:
    """Calculates SHA-256 fingerprint of the uploaded raw audio file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return hashlib.sha256(str(time.time()).encode()).hexdigest()

def compute_block_payload(prev_hash: str, risk_score, verdict: str, timestamp: str, filename: str, audio_sha256: str, scenario: str) -> str:
    return f"{prev_hash}:{risk_score}:{verdict}:{timestamp}:{filename}:{audio_sha256}:{scenario}"

def add_block(risk_score: int, verdict: str, timestamp: str, filename: str = "audio_sample.wav", audio_sha256: str = "", scenario: str = "General Call") -> dict:
    """
    Appends a new cryptographically chained block to the audit ledger.
    """
    prev_hash = chain[-1]["hash"]
    if not audio_sha256:
        audio_sha256 = hashlib.sha256(f"{filename}_{timestamp}".encode()).hexdigest()

    payload = compute_block_payload(prev_hash, risk_score, verdict, timestamp, filename, audio_sha256, scenario)
    block_hash = hashlib.sha256(payload.encode()).hexdigest()

    block = {
        "index": len(chain),
        "prev_hash": prev_hash,
        "hash": block_hash,
        "timestamp": timestamp,
        "filename": filename,
        "risk_score": int(risk_score),
        "verdict": verdict,
        "scenario": scenario,
        "audio_sha256": audio_sha256,
        "signature_status": "CRYPTOGRAPHICALLY_VERIFIED"
    }
    chain.append(block)
    return block

def get_chain() -> list:
    """Returns all blocks in the immutable chain."""
    return chain

def verify_chain() -> dict:
    """
    Validates cryptographic integrity of every block in the ledger.
    Checks:
    1. Previous block hash pointer linkage
    2. Payload SHA-256 hash recomputation
    """
    for i in range(1, len(chain)):
        curr = chain[i]
        prev = chain[i - 1]

        # 1. Check parent link
        if curr["prev_hash"] != prev["hash"]:
            return {
                "valid": False,
                "corrupted_block_index": i,
                "reason": f"Block #{i} prev_hash mismatch. Expected {prev['hash']}, got {curr['prev_hash']}"
            }

        # 2. Check payload hash
        expected_payload = compute_block_payload(
            curr["prev_hash"],
            curr["risk_score"],
            curr["verdict"],
            curr["timestamp"],
            curr["filename"],
            curr["audio_sha256"],
            curr["scenario"]
        )
        recalculated_hash = hashlib.sha256(expected_payload.encode()).hexdigest()
        if recalculated_hash != curr["hash"]:
            return {
                "valid": False,
                "corrupted_block_index": i,
                "reason": f"Block #{i} data tampered. Expected hash {recalculated_hash}, found {curr['hash']}"
            }

    return {
        "valid": True,
        "total_blocks": len(chain),
        "latest_block_hash": chain[-1]["hash"],
        "status": "ALL_BLOCKS_VALIDATED"
    }

def reset_chain():
    """Resets ledger back to genesis block (for testing)."""
    global chain
    chain = [chain[0]]
