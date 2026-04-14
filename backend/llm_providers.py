"""
Module: calling external LLM APIs (OpenAI, Anthropic).

Each function returns a small dict: model label, text, optional error.
"""
from __future__ import annotations

import os
from typing import TypedDict

from app_constants import (
    ANTHROPIC_API_KEY_ENV,
    ANTHROPIC_MODEL,
    ANTHROPIC_PROVIDER_NAME,
    MODEL_OUTPUT_TOKEN_LENGTH,
    OPENAI_API_KEY_ENV,
    OPENAI_MODEL,
    OPENAI_PROVIDER_NAME,
)

class ModelResult(TypedDict, total=False):
    provider: str
    model: str
    text: str
    error: str


async def call_openai_chat(prompt: str) -> ModelResult:
    key = os.getenv(OPENAI_API_KEY_ENV, "").strip()
    if not key:
        return {
            "provider": OPENAI_PROVIDER_NAME,
            "model": OPENAI_MODEL,
            "error": f"{OPENAI_API_KEY_ENV} is not set",
        }

    from openai import AsyncOpenAI

    client = AsyncOpenAI(api_key=key)
    model = OPENAI_MODEL
    try:
        resp = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=MODEL_OUTPUT_TOKEN_LENGTH,
        )
        text = (resp.choices[0].message.content or "").strip()
        return {"provider": OPENAI_PROVIDER_NAME, "model": model, "text": text}
    except Exception as e:
        return {"provider": OPENAI_PROVIDER_NAME, "model": model, "error": str(e)}


async def call_anthropic(prompt: str) -> ModelResult:
    key = os.getenv(ANTHROPIC_API_KEY_ENV, "").strip()
    if not key:
        return {
            "provider": ANTHROPIC_PROVIDER_NAME,
            "model": ANTHROPIC_MODEL,
            "error": f"{ANTHROPIC_API_KEY_ENV} is not set",
        }

    from anthropic import AsyncAnthropic

    client = AsyncAnthropic(api_key=key)
    model = ANTHROPIC_MODEL
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
        return {"provider": ANTHROPIC_PROVIDER_NAME, "model": model, "text": text}
    except Exception as e:
        return {"provider": ANTHROPIC_PROVIDER_NAME, "model": model, "error": str(e)}
