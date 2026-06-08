"""
FastAPI Application - Core Routing and API Setup
Handles API requests with Uvicorn ASGI server
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from pathlib import Path

# Initialize FastAPI application
app = FastAPI(
    title="OnePiece API",
    description="Structured FastAPI application with template rendering",
    version="1.0.0"
)

# Configure base directory
BASE_DIR = Path(__file__).resolve().parent

# Mount static files (CSS, JavaScript, images)
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Setup Jinja2 template engine
templates_dir = BASE_DIR / "templates"
if templates_dir.exists():
    templates = Jinja2Templates(directory=str(templates_dir))


# ============================================================================
# ROOT & HEALTH CHECK ENDPOINTS
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main dashboard/index page"""
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Template error: {str(e)}")


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "OnePiece API",
        "version": "1.0.0"
    }


# ============================================================================
# API ENDPOINTS (v1)
# ============================================================================

@app.get("/api/v1/status", tags=["Status"])
async def api_status():
    """Get API status and system information"""
    return {
        "api_status": "running",
        "endpoints_available": [
            "/api/v1/status",
            "/api/v1/characters",
            "/api/v1/arcs"
        ]
    }


@app.get("/api/v1/characters", tags=["Characters"])
async def get_characters():
    """Fetch all characters"""
    return {
        "characters": [
            {"id": 1, "name": "Monkey D. Luffy", "role": "Captain"},
            {"id": 2, "name": "Roronoa Zoro", "role": "Swordsman"},
            {"id": 3, "name": "Nami", "role": "Navigator"}
        ]
    }


@app.get("/api/v1/characters/{character_id}", tags=["Characters"])
async def get_character(character_id: int):
    """Fetch a specific character by ID"""
    characters = {
        1: {"id": 1, "name": "Monkey D. Luffy", "role": "Captain", "bounty": "3,000,000,000"},
        2: {"id": 2, "name": "Roronoa Zoro", "role": "Swordsman", "bounty": "1,111,000,000"},
        3: {"id": 3, "name": "Nami", "role": "Navigator", "bounty": "366,000,000"}
    }
    
    if character_id not in characters:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return characters[character_id]


@app.get("/api/v1/arcs", tags=["Story Arcs"])
async def get_arcs():
    """Fetch all story arcs"""
    return {
        "arcs": [
            {"id": 1, "name": "East Blue", "chapters": "1-100"},
            {"id": 2, "name": "Grand Line", "chapters": "101-346"},
            {"id": 3, "name": "Sky Island", "chapters": "181-195"}
        ]
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return {
        "error": exc.detail,
        "status_code": exc.status_code,
        "path": str(request.url)
    }


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler"""
    return {
        "error": "Internal Server Error",
        "status_code": 500,
        "detail": str(exc)
    }


# ============================================================================
# STARTUP & SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    print("🚀 FastAPI application starting...")
    print(f"📁 Base directory: {BASE_DIR}")
    print(f"🎯 API Documentation: http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    print("🛑 FastAPI application shutting down...")


if __name__ == "__main__":
    import uvicorn
    
    # Run Uvicorn server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
