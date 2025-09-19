from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('.env')

# Create a simple FastAPI app
app = FastAPI(
    title="LP Assistant Healthcare API",
    description="AI-powered healthcare assistant",
    version="2.0.0"
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Welcome to LP Assistant Healthcare API", "version": "2.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Rx Assistant API"}