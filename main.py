from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import logging
import time
import os

from analyzer import WebsiteRater

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Website Analyzer API",
    description="API for analyzing websites",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WebsiteList(BaseModel):
    urls: List[str]

class AnalysisResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[dict] = None
    error: Optional[str] = None

@app.get("/")
async def root():
    try:
        return FileResponse("analyzer.html")
    except Exception as e:
        logger.error(f"Error serving index page: {str(e)}")
        return HTMLResponse("""
            <html>
                <body>
                    <h1>Website Analyzer</h1>
                    <p>Error loading the analyzer interface. Please try again.</p>
                </body>
            </html>
        """)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_websites(website_list: WebsiteList):
    try:
        if not website_list.urls:
            raise HTTPException(status_code=400, detail="No URLs provided")

        logger.info(f"Starting analysis of {len(website_list.urls)} websites")
        
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

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
