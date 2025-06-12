from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.responses import JSONResponse # type: ignore
from fastapi.exceptions import RequestValidationError # type: ignore
import uvicorn # type: ignore
from datetime import datetime 
import os

from app.routers import fraud

# Create FastAPI application 
app = FastAPI(title="Credit Card Fraud Detection API",
              description="API for detecting fraudulent credit card transactions using machine learning models.",
             version="1.0.0",
             docs_url="/docs",
             redoc_url="/redoc")

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(fraud.router)

# Root endpoint 
@app.get("/", tags=["root"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Credit Card Fraud Detection API",
        "version": "1.0.0",
        "status": "online",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "prediction": "/fraud/predict",
            "model_info": "/fraud/model_info",
            "metrics": "/fraud/metrics"
        }
    }


# Custom exception handlers
@app.exception_handler(RequestValidationError)
def validation_exception_handler(request, exc):
    """Handle validation errors with a friendly message"""
    return JSONResponse(
        status_code=422,
        content={"detail": "Invalid request format. Please check your input data.", "errors": exc.errors()}
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(Exception)
def general_exception_handler(request, exc):
    """Handle unexpected errors"""
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5004))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)