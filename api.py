"""
FastAPI server for the Agentic AI Security System.
Provides REST API endpoints for the chatbot functionality.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from workflow import process_input
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agentic AI Security System API",
    description="REST API for secure AI interactions with LangGraph workflow",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    """Chat request model."""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model."""
    response: str
    session_id: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Agentic AI Security System API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Agentic AI Security System"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process a chat message through the Agentic workflow.
    
    Args:
        request: ChatRequest with message and optional session_id
    
    Returns:
        ChatResponse with the AI response
    """
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        logger.info(f"Processing message: {request.message[:50]}...")
        
        # Process through workflow
        response = process_input(request.message)
        
        logger.info(f"Generated response: {response[:50]}...")
        
        return ChatResponse(
            response=response,
            session_id=request.session_id
        )
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.post("/analyze")
async def analyze_input(request: ChatRequest):
    """
    Analyze input for security threats without generating a response.
    """
    try:
        if not request.message or not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # This can be extended to return detailed analysis
        response = process_input(request.message)
        
        return {
            "message": request.message,
            "response": response
        }
    except Exception as e:
        logger.error(f"Error analyzing input: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
