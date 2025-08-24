from fastapi import FastAPI
from routers import pdf_router, ai_router, followup_router, case_router, workflow_router
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()    

app = FastAPI(title="Guest Relations API")

# Register routers
app.include_router(pdf_router.router)
app.include_router(ai_router.router)
app.include_router(followup_router.router)
app.include_router(case_router.router)
app.include_router(workflow_router.router)

# Allow React dev server
origins = [
    "http://localhost:5173",   # Vite default
    "http://localhost:5174",   # Vite alternative port
    "http://127.0.0.1:5173",   # sometimes needed
    "http://127.0.0.1:5174",   # alternative port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
)

@app.get("/")
def root():
    return {"message": "Guest Relations API running"}
