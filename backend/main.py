import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from logging_config import setup_logging
from routers import auth_route, user_router, task_router, document_router, followup_router, case_router, anonymization_router
from test_router import router as test_router

# Load environment variables
load_dotenv()

# Logging
logger = setup_logging()

# Environment variables
SECRET_KEY = os.environ.get("SECRET_KEY", "").strip()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "").strip()
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

# FastAPI app
app = FastAPI(
    title="Guest Relations API",
    description="Guest relations API with document processing and AI-powered followups",
    version="1.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None
)

# CORS origins
origins = [
    "https://guestreationadomes.netlify.app",
    "http://localhost:5173"
]
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
for origin in allowed_origins:
    origin = origin.strip()
    if origin and origin not in origins:
        origins.append(origin)

# Add Railway public domain if available
railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
if railway_domain and f"https://{railway_domain}" not in origins:
    origins.append(f"https://{railway_domain}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS origins configured: {origins}")

# Trusted host middleware
if ENVIRONMENT == "production":
    allowed_hosts = ["*"]
    if railway_domain:
        allowed_hosts.append(railway_domain)
        allowed_hosts.append(f"*.{railway_domain}")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Startup event
@app.on_event("startup")
async def startup_event():
    try:
        from db import initialize_database, test_connection
        initialize_database()  # make sure engine + session are created
        success = await test_connection()
        if success:
            logger.info("Database connection test successful")
        else:
            logger.warning("[!] Database connection test failed")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")

# Routers
app.include_router(test_router, prefix="/api", tags=["Test"])
app.include_router(auth_route.router, prefix="/api", tags=["Authentication"])
app.include_router(user_router.router, prefix="/api", tags=["Users"])
app.include_router(task_router.router, prefix="/api", tags=["Tasks"])
app.include_router(document_router.router, prefix="/api", tags=["Document Processing"])
app.include_router(followup_router.router, prefix="/api", tags=["Followups"])
app.include_router(case_router.router, prefix="/api", tags=["Cases"])
app.include_router(anonymization_router.router, prefix="/api", tags=["Anonymization"])

# Static files
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

# Root and health endpoints
@app.get("/")
def root():
    return {"message": "Guest Relations API running", "environment": ENVIRONMENT}

@app.get("/api/health")
def api_health_check():
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "database": "available" if os.environ.get("DATABASE_URL") else "unavailable"
    }

@app.post("/api/auth/login-fallback")
def login_fallback():
    return {
        "access_token": "fallback_token",
        "token_type": "bearer",
        "user": {"id": 1, "username": "admin", "email": "admin@example.com", "is_admin": True},
        "message": "Database unavailable - using fallback authentication"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    origin = request.headers.get("origin")
    if origin:
        logger.info(f"CORS request from origin: {origin}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        reload=ENVIRONMENT == "development"
    )
