"""
Punto de entrada principal de la API FastAPI.
"""
from fastapi import FastAPI, Request
from .services.intent_service import detect_intent_service

app = FastAPI(title="CANACO-BOT", description="API de clasificación de intenciones con Saptiva")

@app.post("/detect_intent")
async def detect_intent(request: Request):
    """
    Endpoint principal que recibe un query y detecta la intención.
    """
    body = await request.json()
    from_user = body.get("from")
    query = body.get("query")

    if not from_user or not query:
        return {"error": "Faltan campos requeridos: from, query"}

    return await detect_intent_service(from_user, query)
