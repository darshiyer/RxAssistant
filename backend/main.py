"""
Simplified FastAPI application for deployment without database dependencies
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple in-memory storage for demo
demo_data = {
    "prescriptions": [],
    "medicines": [],
    "chat_history": []
}

class HealthResponse(BaseModel):
    status: str
    message: str
    timestamp: str

class MedicineInfo(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    side_effects: Optional[List[str]] = None
    interactions: Optional[List[str]] = None

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "demo_user"

class ChatResponse(BaseModel):
    response: str
    timestamp: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    logger.info("🚀 Starting RxAssistant API (Simplified Version)")
    yield
    logger.info("🛑 Shutting down RxAssistant API")

# Create FastAPI app
app = FastAPI(
    title="RxAssistant API",
    description="Simplified Health Management System API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="RxAssistant API is running (Simplified Version)",
        timestamp=datetime.now().isoformat()
    )

# OCR endpoint (simplified)
@app.post("/api/v1/ocr/extract-text")
async def extract_text_from_image(file: UploadFile = File(...)):
    """Extract text from uploaded image (mock implementation)"""
    try:
        # Mock OCR response
        mock_text = """
        Patient: John Doe
        Date: 2024-01-15
        
        Prescription:
        1. Amoxicillin 500mg - Take 3 times daily for 7 days
        2. Ibuprofen 400mg - Take as needed for pain
        3. Vitamin D3 1000IU - Take once daily
        
        Doctor: Dr. Smith
        """
        
        return {
            "success": True,
            "extracted_text": mock_text.strip(),
            "confidence": 0.95,
            "processing_time": "1.2s"
        }
    except Exception as e:
        logger.error(f"OCR extraction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract text from image")

# Medicine extraction endpoint
@app.post("/api/v1/medicines/extract")
async def extract_medicines(text: str = Form(...)):
    """Extract medicine names from text"""
    try:
        # Mock medicine extraction
        mock_medicines = [
            {
                "name": "Amoxicillin",
                "dosage": "500mg",
                "frequency": "3 times daily",
                "duration": "7 days",
                "confidence": 0.92
            },
            {
                "name": "Ibuprofen", 
                "dosage": "400mg",
                "frequency": "as needed",
                "duration": "for pain",
                "confidence": 0.88
            },
            {
                "name": "Vitamin D3",
                "dosage": "1000IU", 
                "frequency": "once daily",
                "duration": "ongoing",
                "confidence": 0.95
            }
        ]
        
        return {
            "success": True,
            "medicines": mock_medicines,
            "total_found": len(mock_medicines)
        }
    except Exception as e:
        logger.error(f"Medicine extraction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract medicines")

# Medicine information endpoint
@app.get("/api/v1/medicines/{medicine_name}")
async def get_medicine_info(medicine_name: str):
    """Get detailed information about a medicine"""
    try:
        # Mock medicine information
        mock_info = {
            "name": medicine_name,
            "generic_name": medicine_name.lower(),
            "description": f"Information about {medicine_name}",
            "uses": [
                "Treats bacterial infections",
                "Reduces inflammation",
                "Supports immune system"
            ],
            "side_effects": [
                "Nausea",
                "Dizziness", 
                "Headache"
            ],
            "interactions": [
                "May interact with blood thinners",
                "Avoid with alcohol"
            ],
            "dosage_info": "Follow prescription instructions",
            "warnings": "Consult doctor before use"
        }
        
        return {
            "success": True,
            "medicine": mock_info
        }
    except Exception as e:
        logger.error(f"Medicine info error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get medicine information")

# Chat endpoint
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat_with_assistant(message: ChatMessage):
    """Chat with the health assistant"""
    try:
        # Mock chat responses
        responses = [
            "I understand you're asking about your medication. Please consult with your healthcare provider for personalized advice.",
            "Based on general medical knowledge, here's what I can tell you about that condition...",
            "It's important to take medications as prescribed. Would you like me to help you understand the dosage instructions?",
            "For any serious health concerns, please contact your doctor immediately. I'm here to provide general information only.",
            "That's a great question about health management. Let me provide some general guidance..."
        ]
        
        # Simple response selection based on message content
        response_text = responses[len(message.message) % len(responses)]
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process chat message")

# Authentication endpoints (mock)
@app.post("/api/v1/auth/register")
async def register():
    """Mock registration endpoint"""
    return {"message": "Registration disabled in demo mode", "success": False}

@app.post("/api/v1/auth/login")
async def login():
    """Mock login endpoint"""
    return {"message": "Login disabled in demo mode", "success": False}

@app.post("/api/v1/auth/logout")
async def logout():
    """Mock logout endpoint"""
    return {"message": "Logout disabled in demo mode", "success": True}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to RxAssistant API (Simplified Version)",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "ocr": "/api/v1/ocr/extract-text",
            "medicines": "/api/v1/medicines/extract",
            "chat": "/api/v1/chat"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)