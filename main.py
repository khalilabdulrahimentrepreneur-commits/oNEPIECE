"""
FastAPI Application - Core Routing and API Setup
Handles API requests with Uvicorn ASGI server
Integrated with Mindfighter Algorithm
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Optional
import asyncio
import hashlib
import json
from mindfighter import generate, ProcessingStrategy, ContentType, mindfighter as mindfighter_instance

# Initialize FastAPI application
app = FastAPI(
    title="OnePiece API - Mindfighter Engine",
    description="Structured FastAPI application with Mindfighter auto-generator",
    version="1.0.0"
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
# REQUEST MODELS
# ============================================================================

class GenerationRequest(BaseModel):
    """Request model for Mindfighter generation"""
    data: Any
    strategy: str = "hybrid"
    content_type: str = "json"
    max_depth: int = 5


class CharacterRequest(BaseModel):
    """Request model for character creation"""
    name: str
    role: str
    bounty: Optional[str] = None


class HelloRequest(BaseModel):
    """Simple hello request for demonstration"""
    name: Optional[str] = "World"
    strategy: Optional[str] = "hybrid"
    content_type: Optional[str] = "text"
    max_depth: Optional[int] = 2


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
        "service": "OnePiece API with Mindfighter",
        "version": "1.0.0",
        "mindfighter_ready": True
    }


# ============================================================================
# STARTUP & SHUTDOWN EVENTS (Engine Mounting + Lock + Cache)
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Execute on application startup"""
    # Mount the MindfighterEngine instance into the app state for DI
    app.state.mindfighter = mindfighter_instance
    app.state.mindfighter_lock = asyncio.Lock()
    app.state.generate_cache = {}

    print("🚀 FastAPI application starting...")
    print(f"📁 Base directory: {BASE_DIR}")
    print(f"🔧 Mindfighter Engine: Initialized")
    print(f"🎯 API Documentation: http://localhost:8000/docs")
    print(f"🧠 Mindfighter Ready: True")


@app.on_event("shutdown")
async def shutdown_event():
    """Execute on application shutdown"""
    print("🛑 FastAPI application shutting down...")


# ============================================================================
# HELLO WORLD - DIVE
# ============================================================================

@app.get("/api/v1/hello", tags=["Hello"])
async def hello_world():
    """Simple Hello World endpoint with Mindfighter demo"""
    try:
        base_message = "Hello, World!"
        # Generate a few variants using Mindfighter for demonstration
        # Use the mounted engine for consistency
        async with app.state.mindfighter_lock:
            gen = await asyncio.to_thread(
                app.state.mindfighter.generate,
                {"greeting": base_message},
                ProcessingStrategy.HYBRID,
                ContentType.TEXT,
                1
            )
        # gen is a GenerationResult object; format into public dict
        response = {
            "message": base_message,
            "mindfighter_variant": gen.output,
            "confidence": gen.confidence_score
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/hello", tags=["Hello"])
async def hello_generate(req: HelloRequest):
    """Generate Hello variations using specified strategy/content-type"""
    try:
        name = req.name or "World"
        greeting = f"Hello, {name}!"

        try:
            strategy_enum = ProcessingStrategy[req.strategy.upper()]
        except Exception:
            strategy_enum = ProcessingStrategy.HYBRID
        try:
            content_type_enum = ContentType[req.content_type.upper()]
        except Exception:
            content_type_enum = ContentType.TEXT

        # Use cache to short-circuit repeated calls
        key_obj = {
            "greeting": greeting,
            "strategy": strategy_enum.value,
            "content_type": content_type_enum.value,
            "max_depth": req.max_depth
        }
        key_str = json.dumps(key_obj, sort_keys=True)
        key = hashlib.sha256(key_str.encode()).hexdigest()

        if key in app.state.generate_cache:
            cached = app.state.generate_cache[key]
            return {
                "input_greeting": greeting,
                "generated": cached["output"],
                "strategy": cached["strategy"],
                "confidence": cached["confidence"],
                "processing_time": cached["processing_time"],
                "cached": True
            }

        async with app.state.mindfighter_lock:
            gen = await asyncio.to_thread(
                app.state.mindfighter.generate,
                {"greeting": greeting, "name": name},
                strategy_enum,
                content_type_enum,
                req.max_depth
            )

        result = {
            "output": gen.output,
            "strategy": gen.strategy_used.value,
            "processing_time": gen.processing_time,
            "depth": gen.depth_reached,
            "transformations": gen.transformations_applied,
            "confidence": gen.confidence_score,
            "metadata": gen.metadata
        }

        # Store in cache
        app.state.generate_cache[key] = result

        return {
            "input_greeting": greeting,
            "generated": result["output"],
            "strategy": result["strategy"],
            "confidence": result["confidence"],
            "processing_time": result["processing_time"],
            "cached": False
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Hello generation failed: {str(e)}")


# ============================================================================
# MINDFIGHTER GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/v1/generate", tags=["Mindfighter"])
async def api_generate(request: GenerationRequest):
    """Generate content using the mounted Mindfighter engine (persistent instance)

    This implementation uses app.state.mindfighter with a lock and an in-memory cache
    to provide consistent metrics and avoid duplicate heavy computations.
    """
    try:
        # resolve strategy/content_type enums
        try:
            strategy_enum = ProcessingStrategy[request.strategy.upper()]
        except Exception:
            strategy_enum = ProcessingStrategy.HYBRID
        try:
            content_type_enum = ContentType[request.content_type.upper()]
        except Exception:
            content_type_enum = ContentType.JSON

        # prepare cache key
        key_obj = {
            "data": request.data,
            "strategy": strategy_enum.value,
            "content_type": content_type_enum.value,
            "max_depth": request.max_depth
        }
        key_str = json.dumps(key_obj, sort_keys=True, default=str)
        key = hashlib.sha256(key_str.encode()).hexdigest()

        if key in app.state.generate_cache:
            cached = app.state.generate_cache[key]
            return {"success": True, "cached": True, "result": cached}

        # Run generation in threadpool to avoid blocking the event loop
        async with app.state.mindfighter_lock:
            gen = await asyncio.to_thread(
                app.state.mindfighter.generate,
                request.data,
                strategy_enum,
                content_type_enum,
                request.max_depth
            )

        result = {
            "output": gen.output,
            "strategy": gen.strategy_used.value,
            "processing_time": gen.processing_time,
            "depth": gen.depth_reached,
            "transformations": gen.transformations_applied,
            "confidence": gen.confidence_score,
            "metadata": gen.metadata
        }

        # cache result
        app.state.generate_cache[key] = result

        return {"success": True, "cached": False, "result": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Generation failed: {str(e)}")


@app.get("/api/v1/generate/strategies", tags=["Mindfighter"])
async def get_strategies():
    """Get available Mindfighter strategies"""
    return {
        "strategies": [
            "semantic",
            "syntactic",
            "hybrid",
            "recursive",
            "iterative"
        ],
        "descriptions": {
            "semantic": "Meaning-based analysis and synthesis",
            "syntactic": "Structure-based reorganization",
            "hybrid": "Combined semantic and syntactic approach",
            "recursive": "Hierarchical nested processing",
            "iterative": "Loop-based quality refinement"
        }
    }


@app.get("/api/v1/generate/content-types", tags=["Mindfighter"])
async def get_content_types():
    """Get available output content types"""
    return {
        "content_types": [
            "text",
            "json",
            "markdown",
            "html",
            "code",
            "api_response"
        ]
    }


# ============================================================================
# API ENDPOINTS (v1)
# ============================================================================

@app.get("/api/v1/status", tags=["Status"])
async def api_status():
    """Get API status and system information"""
    return {
        "api_status": "running",
        "mindfighter_status": "operational",
        "endpoints_available": [
            "/api/v1/status",
            "/api/v1/generate",
            "/api/v1/characters",
            "/api/v1/arcs",
            "/docs"
        ]
    }


@app.get("/api/v1/characters", tags=["Characters"])
async def get_characters():
    """Fetch all characters"""
    return {
        "characters": [
            {"id": 1, "name": "Monkey D. Luffy", "role": "Captain", "bounty": "3,000,000,000"},
            {"id": 2, "name": "Roronoa Zoro", "role": "Swordsman", "bounty": "1,111,000,000"},
            {"id": 3, "name": "Nami", "role": "Navigator", "bounty": "366,000,000"},
            {"id": 4, "name": "Usopp", "role": "Sniper", "bounty": "200,000,000"},
            {"id": 5, "name": "Sanji", "role": "Cook", "bounty": "1,032,000,000"}
        ]
    }


@app.get("/api/v1/characters/{character_id}", tags=["Characters"])
async def get_character(character_id: int):
    """Fetch a specific character by ID"""
    characters = {
        1: {"id": 1, "name": "Monkey D. Luffy", "role": "Captain", "bounty": "3,000,000,000", "crew": "Straw Hat"},
        2: {"id": 2, "name": "Roronoa Zoro", "role": "Swordsman", "bounty": "1,111,000,000", "crew": "Straw Hat"},
        3: {"id": 3, "name": "Nami", "role": "Navigator", "bounty": "366,000,000", "crew": "Straw Hat"},
        4: {"id": 4, "name": "Usopp", "role": "Sniper", "bounty": "200,000,000", "crew": "Straw Hat"},
        5: {"id": 5, "name": "Sanji", "role": "Cook", "bounty": "1,032,000,000", "crew": "Straw Hat"}
    }
    
    if character_id not in characters:
        raise HTTPException(status_code=404, detail="Character not found")
    
    return characters[character_id]


@app.post("/api/v1/characters", tags=["Characters"])
async def create_character(character: CharacterRequest):
    """Create a new character (uses Mindfighter for enrichment)"""
    
    # Use Mindfighter to enrich character data
    enrichment = generate(
        input_data={
            "name": character.name,
            "role": character.role,
            "bounty": character.bounty or "Unknown"
        },
        strategy="semantic",
        content_type="json"
    )
    
    return {
        "character": character.dict(),
        "enrichment": enrichment["output"],
        "mindfighter_confidence": enrichment["confidence"]
    }


@app.get("/api/v1/arcs", tags=["Story Arcs"])
async def get_arcs():
    """Fetch all story arcs"""
    return {
        "arcs": [
            {"id": 1, "name": "East Blue", "chapters": "1-100", "saga": "Introduction"},
            {"id": 2, "name": "Grand Line", "chapters": "101-346", "saga": "Adventure"},
            {"id": 3, "name": "Sky Island", "chapters": "181-195", "saga": "Adventure"},
            {"id": 4, "name": "Water 7", "chapters": "322-381", "saga": "Adventure"},
            {"id": 5, "name": "Marineford", "chapters": "456-489", "saga": "War"}
        ]
    }


@app.get("/api/v1/arcs/{arc_id}", tags=["Story Arcs"])
async def get_arc(arc_id: int):
    """Fetch specific story arc by ID"""
    arcs = {
        1: {"id": 1, "name": "East Blue", "chapters": "1-100", "saga": "Introduction", "events": "Crew formation"},
        2: {"id": 2, "name": "Grand Line", "chapters": "101-346", "saga": "Adventure", "events": "Major battles"},
        3: {"id": 3, "name": "Sky Island", "chapters": "181-195", "saga": "Adventure", "events": "Sky exploration"},
        4: {"id": 4, "name": "Water 7", "chapters": "322-381", "saga": "Adventure", "events": "Ship crisis"},
        5: {"id": 5, "name": "Marineford", "chapters": "456-489", "saga": "War", "events": "Major war"}
    }
    
    if arc_id not in arcs:
        raise HTTPException(status_code=404, detail="Arc not found")
    
    return arcs[arc_id]


# ============================================================================
# ADVANCED ENDPOINTS
# ============================================================================

@app.post("/api/v1/analyze", tags=["Analysis"])
async def analyze_data(data: dict):
    """Analyze data using Mindfighter with detailed breakdown"""
    results = {}
    for strategy in ["semantic", "syntactic", "hybrid"]:
        result = generate(
            input_data=data,
            strategy=strategy,
            content_type="json"
        )
        results[strategy] = result
    
    return {
        "input": data,
        "analysis": results,
        "best_strategy": max(results.items(), key=lambda x: x[1]["confidence"])[0]
    }


@app.get("/api/v1/metrics", tags=["Metrics"])
async def get_metrics():
    """Get Mindfighter performance metrics"""
    from mindfighter import mindfighter
    
    return {
        "strategy_metrics": mindfighter.strategy_metrics,
        "transformation_history_count": len(mindfighter.transformation_history),
        "cache_size": len(mindfighter.cache)
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "status_code": 500,
            "detail": str(exc)
        }
    )


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
