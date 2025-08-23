from fastapi import APIRouter, HTTPException
from services.followup_service import get_all_followups, delete_followup

router = APIRouter(prefix="/followups", tags=["Followups"])

@router.get("/")
def read_followups():
    followups = get_all_followups()
    return {"followups": followups}

@router.delete("/{followup_id}")
def remove_followup(followup_id: int):
    followup = delete_followup(followup_id)
    if not followup:
        raise HTTPException(status_code=404, detail="Follow-up not found")
    return {"status": "success", "id": followup_id}
