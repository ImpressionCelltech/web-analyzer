# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import logging
import time
import os
from starlette.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"success": False, "error": "Internal server error. Please try again."}
            )

app = FastAPI(
    title="Website Analyzer API",
    description="API for analyzing websites",
    version="1.0.0"
)

# Enhanced CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]  # Exposes all headers
)

# Add request logging middleware
app.add_middleware(RequestLoggingMiddleware)

# Mount static files if they exist
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class WebsiteList(BaseModel):
    urls: List[str]

class AnalysisResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
    error: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        return FileResponse("analyzer.html")
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return HTMLResponse(content="<html><body><h1>Website Analyzer</h1><p>Please use the API endpoint /api/analyze for analysis.</p></body></html>")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_websites(website_list: WebsiteList, request: Request):
    try:
        if not website_list.urls:
            raise HTTPException(status_code=400, detail="No URLs provided")

        # Log client information
        client_host = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        logger.info(f"Analysis request from {client_host} using {user_agent}")

        rater = WebsiteRater()
        results = rater.analyze_websites(website_list.urls)
        
        return AnalysisResponse(
            success=True,
            data=results,
            message=f"Successfully analyzed {results['successful_analyses']} websites"
        )

    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return AnalysisResponse(
            success=False,
            error=str(e)
        )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
