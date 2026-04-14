"""
Module: HTTP API — receives the user prompt and returns all model outputs.

Later you can add: auth, rate limits, streaming, RAG context injection, orchestration.
"""
from __future__ import annotations

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from llm_providers import call_anthropic, call_openai_chat

## App Constants
########################################################
# Load .env from project root (parent of backend/)
_root = Path(__file__).resolve().parent.parent
load_dotenv(_root / ".env")

app = FastAPI(title="AI-Verse Lab", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## Data Model classes
########################################################
## Handle Request format from UI to Backend
## Max Length of 32000 characters can handle ~8000 token at the application level
## Contributes in governing the context window size of the input
class RequestHandler(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=32000)

## Handle Response format from Models 
class ResponseHandler(BaseModel):
    prompt: str
    results: list[dict]

@app.post("/api/compare", response_model=ResponseHandler)
async def compare_models(body: RequestHandler):
    p = body.prompt.strip()
    if not p:
        raise HTTPException(status_code=400, detail="Prompt is empty")

    # Run all providers in parallel — same user message, independent API calls.
    results = await asyncio.gather(
        ## We are passing the single prompt to both models
        ## Currently this code does not provide history of user prommpt and model responses
        call_openai_chat(p),
        call_anthropic(p),
    )
    return ResponseHandler(prompt=p, results=list(results)) # returning the response to the client


_static = _root / "frontend"
if _static.is_dir():
    app.mount("/assets", StaticFiles(directory=_static / "assets"), name="assets")

