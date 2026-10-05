"""Cliente común para Ollama y la VM de Azure.

Los dos exponen la API compatible con OpenAI (/v1/models y /v1/chat/completions),
así que cambiar de local a remoto es solo cambiar BACKEND_URL.
"""

import os
import time

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://ollama:11434").rstrip("/")
BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")
MODEL = os.getenv("MODEL", "gemma4:e4b")
TIMEOUT = int(os.getenv("BACKEND_TIMEOUT", "300"))

_cabeceras = {"Authorization": f"Bearer {BACKEND_API_KEY}"} if BACKEND_API_KEY else {}


def modo():
    return "local" if "ollama" in BACKEND_URL or "localhost" in BACKEND_URL else "remoto"


def listar_modelos():
    r = requests.get(f"{BACKEND_URL}/v1/models", headers=_cabeceras, timeout=10)
    r.raise_for_status()
    return [m["id"] for m in r.json().get("data", [])]


def chat(mensajes, modelo=None, max_tokens=800):
    inicio = time.perf_counter()
    r = requests.post(f"{BACKEND_URL}/v1/chat/completions", headers=_cabeceras, timeout=TIMEOUT, json={
        "model": modelo or MODEL,
        "messages": mensajes,
        "max_tokens": max_tokens,
        "reasoning_effort": "none",  # Ollama: desactiva el modo thinking de Gemma 4
    })
    r.raise_for_status()
    d = r.json()
    total = time.perf_counter() - inicio
    tokens = d.get("usage", {}).get("completion_tokens", 0)
    return {
        "respuesta": d["choices"][0]["message"]["content"].strip(),
        "modelo": d.get("model", modelo or MODEL),
        "backend": modo(),
        "tiempo_s": round(total, 2),
        "tokens": tokens,
        "tok_s": round(tokens / total, 1) if total and tokens else None,
    }
