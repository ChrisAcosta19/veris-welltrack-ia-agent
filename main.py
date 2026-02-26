"""
API REST con FastAPI para exponer el agente conversacional de WellTrack.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from agent import run_agent

load_dotenv()

app = FastAPI(
    title="WellTrack IA Agent API",
    description="API para el agente conversacional de onboarding de WellTrack",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    response: str
    is_final: bool
    summary: Optional[Dict[str, Any]] = None

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.session_id or not request.message.strip():
        raise HTTPException(status_code=400, detail="session_id y message son requeridos y no pueden estar vacíos")
    
    try:
        result = run_agent(request.session_id, request.message)
        
        return ChatResponse(
            response=result["response"],
            is_final=result["is_final"],
            summary=result["summary"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del agente: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "API de WellTrack conectada"}
