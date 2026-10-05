"""API REST (FastAPI) que reenvía el chat al backend configurado en BACKEND_URL."""

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import backend

app = FastAPI(title="Chat API · Reto 07/10", version="1.0")


class Mensaje(BaseModel):
    role: str
    content: str


class PeticionChat(BaseModel):
    mensajes: list[Mensaje] | None = None
    prompt: str | None = None
    modelo: str | None = None


@app.get("/health")
def health():
    """Estado de la API y del backend al que apunta."""
    try:
        modelos = backend.listar_modelos()
        ok = True
    except requests.RequestException:
        modelos, ok = [], False
    return {"api": "ok", "backend": backend.modo(), "backend_url": backend.BACKEND_URL,
            "backend_ok": ok, "modelo": backend.MODEL, "modelos_disponibles": modelos}


@app.get("/modelos")
def modelos():
    try:
        return backend.listar_modelos()
    except requests.RequestException as e:
        raise HTTPException(502, f"Backend no disponible: {e}")


@app.post("/chat")
def chat(p: PeticionChat):
    if p.mensajes:
        mensajes = [m.model_dump() for m in p.mensajes]
    elif p.prompt:
        mensajes = [{"role": "user", "content": p.prompt}]
    else:
        raise HTTPException(422, "Envía 'prompt' o 'mensajes'")
    try:
        return backend.chat(mensajes, p.modelo)
    except requests.RequestException as e:
        raise HTTPException(502, f"Error del backend: {e}")
