from fastapi import FastAPI
from routers import pdf_router, ai_router
from dotenv import load_dotenv

load_dotenv()    

app = FastAPI(title="Guest Relations API")

# Register routers
app.include_router(pdf_router.router)
app.include_router(ai_router.router)

@app.get("/")
def root():
    return {"message": "Guest Relations API running"}
