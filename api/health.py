from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    return JSONResponse(
        content={"status": "healthy", "service": "Rx Assistant API"},
        status_code=200
    )

@app.get("/health")
async def health_check_alt():
    return JSONResponse(
        content={"status": "healthy", "service": "Rx Assistant API"},
        status_code=200
    )

@app.get("/")
async def root():
    return JSONResponse(
        content={"message": "Welcome to LP Assistant Healthcare API", "version": "2.0.0"},
        status_code=200
    )

# Vercel handler - this is the key for Vercel deployment
handler = app