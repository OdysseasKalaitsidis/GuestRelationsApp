import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from sqlalchemy import create_engine
from routers import (
    document_router, followup_router, case_router, 
    auth_route, user_router, task_router, anonymization_router
)
from test_router import router as test_router
from logging_config import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

# Get environment
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

app = FastAPI(
    title="Guest Relations API",
    description="A comprehensive API for managing guest relations cases, document processing (PDF/DOCX), and AI-powered followups",
    version="1.0.0",
    docs_url="/docs" if ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if ENVIRONMENT == "development" else None
)

@app.on_event("startup")
async def startup_event():
    """Test database connection on startup"""
    try:
        from db import initialize_database
        
        # Try to initialize database connection
        if initialize_database():
            logger.info("✅ Database connection initialized successfully")
            
            # Test the connection
            from db import get_engine
            engine = get_engine()
            with engine.connect() as conn:
                result = conn.execute("SELECT 1")
                logger.info(f"✅ MySQL connection test successful! Test query returned: {result.fetchone()}")
        else:
            logger.warning("⚠️ MySQL environment variables not found - database features will be unavailable")
            
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        # Don't raise the exception - let the app start but log the error
        # This allows the app to start even if DB is temporarily unavailable

# Register routers
app.include_router(test_router, prefix="/api", tags=["Test"])
app.include_router(auth_route.router, prefix="/api", tags=["Authentication"])
app.include_router(user_router.router, prefix="/api", tags=["Users"])
app.include_router(task_router.router, prefix="/api", tags=["Tasks"])
app.include_router(document_router.router, prefix="/api", tags=["Document Processing"])
app.include_router(followup_router.router, prefix="/api", tags=["Followups"])
app.include_router(case_router.router, prefix="/api", tags=["Cases"])
app.include_router(anonymization_router.router, prefix="/api", tags=["Anonymization"])

# Mount static files (built frontend)
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

# CORS Configuration
if ENVIRONMENT == "development":
    origins = [
        "http://localhost:5173",   # Vite default
        "http://localhost:5174",   # Vite alternative port
        "http://127.0.0.1:5173",   # sometimes needed
        "http://127.0.0.1:5174",   # alternative port
    ]
else:
    # Production CORS - allow specific origins
    origins = [
        "https://guestreationadomes.netlify.app",  # Netlify frontend
        "https://guestrelationsapp-production.up.railway.app",  # Railway domain
    ]
    
    # Add any additional origins from environment variable
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    for origin in allowed_origins:
        origin = origin.strip()
        if origin and origin not in origins:
            origins.append(origin)
    
    # Add Railway domain if available
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_domain and f"https://{railway_domain}" not in origins:
        origins.append(f"https://{railway_domain}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Log CORS configuration
logger.info(f"CORS origins configured: {origins}")

# Add trusted host middleware for production
if ENVIRONMENT == "production":
    allowed_hosts = ["*"]  # Railway handles this
    railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
    if railway_domain:
        allowed_hosts.append(railway_domain)
        allowed_hosts.append(f"*.{railway_domain}")
    
    app.add_middleware(
        TrustedHostMiddleware, 
        allowed_hosts=allowed_hosts
    )

@app.get("/")
def root():
    return {"message": "Guest Relations API running", "environment": ENVIRONMENT}

@app.get("/health")
def health_check():
    return {"status": "healthy", "environment": ENVIRONMENT}

@app.options("/{full_path:path}")
async def options_handler(full_path: str):
    """Handle CORS preflight requests"""
    return {"message": "CORS preflight handled"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    
    # Log CORS-related headers
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
    port=int(os.getenv("PORT", 8000)),
    reload=ENVIRONMENT == "development"
)

    
