from fastapi import APIRouter
from services.ledger_service import get_chain, verify_chain, reset_chain

router = APIRouter(prefix="/ledger", tags=["Blockchain Ledger"])

@router.get("")
def read_ledger():
    """Returns all blocks in the immutable blockchain audit ledger with verification status."""
    chain = get_chain()
    verification = verify_chain()
    return {
        "chain": chain,
        "total_blocks": len(chain),
        "is_valid": verification.get("valid", False),
        "latest_block_hash": chain[-1]["hash"],
        "verification": verification
    }

@router.get("/verify")
def verify_ledger_integrity():
    """Runs a deep cryptographic audit across the entire chain."""
    return verify_chain()

@router.post("/reset")
def reset_ledger_chain():
    """Resets chain to genesis state."""
    reset_chain()
    return {"status": "success", "message": "Ledger reset to Genesis block."}
