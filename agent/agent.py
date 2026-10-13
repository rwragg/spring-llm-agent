"""LLM agent logic — calls a local Ollama model.

Kept as a thin, testable module separate from the web layer so the core
"agent" behavior can be unit-tested without a running server.
"""
from __future__ import annotations

import httpx

DEFAULT_MODEL = "llama3.2"
OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = (
    "You are a concise technical assistant. Answer the user's question directly, "
    "in a few sentences, without fluff."
)


def build_payload(prompt: str, model: str = DEFAULT_MODEL) -> dict:
    return {
        "model": model,
        "prompt": f"{SYSTEM_PROMPT}\n\nUser: {prompt}\nAssistant:",
        "stream": False,
    }


def ask_ollama(prompt: str, model: str = DEFAULT_MODEL, timeout: float = 60.0) -> str:
    """Send a prompt to Ollama and return the model's text response."""
    payload = build_payload(prompt, model)
    with httpx.Client(timeout=timeout) as client:
        resp = client.post(OLLAMA_URL, json=payload)
        resp.raise_for_status()
        data = resp.json()
    return data.get("response", "").strip()


def ask(prompt: str, model: str = DEFAULT_MODEL) -> dict:
    """Public entry point: returns a structured result for the API layer."""
    try:
        answer = ask_ollama(prompt, model)
        return {"prompt": prompt, "model": model, "answer": answer, "error": None}
    except Exception as exc:  # noqa: BLE001 - surface any failure to the caller
        return {"prompt": prompt, "model": model, "answer": None, "error": str(exc)}