"""
Module: calling external LLM APIs (OpenAI, Anthropic).

Each function returns a small dict: model label, text, optional error.
"""
from __future__ import annotations

import os
from typing import TypedDict

## Contributes in governing the response token length from the models
## The model response would be cut off as soon as this limit is breached
## Overall Context Window size = Input token length from application level + Output token length set here
MODEL_OUTPUT_TOKEN_LENGTH = 1024

class ModelResult(TypedDict, total=False):
    provider: str
    model: str
    text: str
    error: str


async def call_openai_chat(prompt: str) -> ModelResult:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return {
            "provider": "OpenAI",
            "model": "gpt-4o-mini",
            "error": "OPENAI_API_KEY is not set",
        }

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=key)
    model = "gpt-4o-mini"
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MODEL_OUTPUT_TOKEN_LENGTH,
        )
        text = (resp.choices[0].message.content or "").strip()
        return {"provider": "OpenAI", "model": model, "text": text}
    except Exception as e:
        return {"provider": "OpenAI", "model": model, "error": str(e)}


async def call_anthropic(prompt: str) -> ModelResult:
    key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not key:
        return {
            "provider": "Anthropic",
            "model": "claude-3-5-haiku-20241022",
            "error": "ANTHROPIC_API_KEY is not set",
        }

    from anthropic import AsyncAnthropic

    client = AsyncAnthropic(api_key=key)
    model = "claude-3-5-haiku-20241022"
    try:
        msg = await client.messages.create(
            model=model,
            max_tokens=MODEL_OUTPUT_TOKEN_LENGTH,
            messages=[{"role": "user", "content": prompt}],
        )
        parts = []
        for block in msg.content:
            if hasattr(block, "text"):
                parts.append(block.text)
        text = "".join(parts).strip()
        return {"provider": "Anthropic", "model": model, "text": text}
    except Exception as e:
        return {"provider": "Anthropic", "model": model, "error": str(e)}
