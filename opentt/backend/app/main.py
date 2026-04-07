from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException,
    ForbiddenException,
    not_found_exception_handler,
    conflict_exception_handler,
    validation_exception_handler,
    forbidden_exception_handler,
    request_validation_exception_handler,
)
from app.api.routes import (
    institutions,
    teachers,
    subjects,
    buildings,
    students,
    activities,
    constraints,
    solve,
)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Open Source Timetable Management System with OR-Tools CP-SAT Solver",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register exception handlers
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(ConflictException, conflict_exception_handler)
app.add_exception_handler(ValidationException, validation_exception_handler)
app.add_exception_handler(ForbiddenException, forbidden_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "OpenTT API",
        "version": settings.APP_VERSION,
        "docs": "/api/docs",
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "opentt-api"}


# Include all routers
app.include_router(
    institutions.router,
    prefix=f"{settings.API_V1_PREFIX}/institutions",
    tags=["institutions"],
)

app.include_router(
    teachers.router,
    prefix=settings.API_V1_PREFIX,
    tags=["teachers"],
)

app.include_router(
    subjects.router,
    prefix=settings.API_V1_PREFIX,
    tags=["subjects"],
)

app.include_router(
    buildings.router,
    prefix=settings.API_V1_PREFIX,
    tags=["buildings", "rooms"],
)

app.include_router(
    students.router,
    prefix=settings.API_V1_PREFIX,
    tags=["students"],
)

app.include_router(
    activities.router,
    prefix=settings.API_V1_PREFIX,
    tags=["activities"],
)

app.include_router(
    constraints.router,
    prefix=settings.API_V1_PREFIX,
    tags=["constraints"],
)

app.include_router(
    solve.router,
    prefix=settings.API_V1_PREFIX,
    tags=["solve"],
)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION} starting up...")
    print(f"📚 API Documentation: http://localhost:8000/api/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print(f"👋 {settings.APP_NAME} shutting down...")


# Run with uvicorn
if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
