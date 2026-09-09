from fastapi import APIRouter
from db.database import get_history, clear_history

router = APIRouter(prefix="/history", tags=["History"])

@router.get("")
@router.get("/")
def read_history(limit: int = 50):
    """Returns past analysis scans stored in SQLite."""
    items = get_history(limit)
    return {"history": items, "count": len(items)}

@router.delete("")
@router.delete("/")
def delete_all_history():
    """Clears all scan history logs."""
    clear_history()
    return {"status": "success", "message": "All forensic history records deleted."}

@router.post("/clear")
def clear_all_history_post():
    """Alternative POST endpoint to clear all scan history logs."""
    clear_history()
    return {"status": "success", "message": "All forensic history records deleted."}
