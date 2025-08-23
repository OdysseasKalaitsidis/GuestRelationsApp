from fastapi import FastAPI
from routers import pdf_router, ai_router, followup_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()    

app = FastAPI(title="Guest Relations API")

# Register routers
app.include_router(pdf_router.router)
app.include_router(ai_router.router)
app.include_router(followup_router.router)

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, DELETE, OPTIONS, etc.
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Guest Relations API running"}
