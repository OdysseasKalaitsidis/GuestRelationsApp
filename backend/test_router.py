from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def test_endpoint():
    """Simple test endpoint to verify CORS is working"""
    return {"message": "CORS is working!", "status": "success"}

@router.post("/test")
def test_post_endpoint():
    """Simple test POST endpoint to verify CORS is working"""
    return {"message": "POST request successful!", "status": "success"}
