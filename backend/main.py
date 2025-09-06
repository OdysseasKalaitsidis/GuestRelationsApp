import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from logging_config import setup_logging
from routers import auth_route, user_router, document_router, followup_router, case_router, anonymization_router, rag_router

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
    "https://docguestrelations.netlify.app",  # Updated frontend domain
    "https://guestreationadomes.netlify.app",  # Keep old domain for backward compatibility
    "http://localhost:5173"
]
allowed_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
for origin in allowed_origins:
    origin = origin.strip()
    if origin and origin not in origins:
        origins.append(origin)

# Add Render public domain if available
render_domain = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_domain and f"https://{render_domain}" not in origins:
    origins.append(f"https://{render_domain}")

# Add the frontend domain explicitly
frontend_domain = "https://docguestrelations.netlify.app"  # Updated frontend domain
if frontend_domain not in origins:
    origins.append(frontend_domain)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)

logger.info(f"CORS origins configured: {origins}")

# Trusted host middleware
if ENVIRONMENT == "production":
    allowed_hosts = ["*"]
    if render_domain:
        allowed_hosts.append(render_domain)
        allowed_hosts.append(f"*.{render_domain}")
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=allowed_hosts)

# Startup event
@app.on_event("startup")
async def startup_event():
    try:
        # Initialize Supabase client instead of SQLAlchemy
        from supabase_client import initialize_supabase, test_supabase_connection
        
        # Initialize Supabase client
        if initialize_supabase():
            logger.info("Supabase client initialized successfully")
            
            # Test connection
            success = await test_supabase_connection()
            if success:
                logger.info("Supabase connection test successful")
            else:
                logger.warning("[!] Supabase connection test failed")
        else:
            logger.warning("[!] Supabase client initialization failed")
            
    except Exception as e:
        logger.error(f"Supabase initialization failed: {e}")

# Routers
app.include_router(auth_route.router, prefix="/api", tags=["Authentication"])
app.include_router(user_router.router, prefix="/api", tags=["Users"])
app.include_router(document_router.router, prefix="/api", tags=["Document Processing"])
app.include_router(followup_router.router, prefix="/api", tags=["Followups"])
app.include_router(case_router.router, prefix="/api", tags=["Cases"])
app.include_router(anonymization_router.router, prefix="/api", tags=["Anonymization"])
app.include_router(rag_router.router, prefix="/api", tags=["RAG"])

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
        "database": "available" if os.environ.get("SUPABASE_URL") else "unavailable"
    }

@app.options("/api/{path:path}")
async def options_handler(path: str):
    """Handle CORS preflight requests"""
    return {"message": "OK"}

@app.get("/api/debug/env")
def debug_env():
    """Debug endpoint to check environment variables (remove in production)"""
    return {
        "SUPABASE_URL": bool(os.environ.get("SUPABASE_URL")),
        "SUPABASE_SERVICE_ROLE_KEY": bool(os.environ.get("SUPABASE_SERVICE_ROLE_KEY")),
        "SUPABASE_ANON_KEY": bool(os.environ.get("SUPABASE_ANON_KEY")),
        "SECRET_KEY": bool(os.environ.get("SECRET_KEY")),
        "has_secret_key": bool(SECRET_KEY),
    }

@app.get("/api/debug/users")
async def debug_users():
    """Debug endpoint to list users (remove in production)"""
    try:
        from supabase_client import get_supabase
        supabase = get_supabase()
        response = supabase.table("users").select("id, username, email, is_admin").execute()
        
        if response.data:
            return {
                "users": response.data,
                "count": len(response.data)
            }
        else:
            return {
                "users": [],
                "count": 0,
                "message": "No users found"
            }
    except Exception as e:
        return {
            "error": str(e),
            "error_type": type(e).__name__
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
