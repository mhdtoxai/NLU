import os
import json
import logging
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Request
from saptiva_agents import SAPTIVA_LEGACY  # puedes cambiar a SAPTIVA_OPS según necesidad
from saptiva_agents.base import SaptivaAIChatCompletionClient
from saptiva_agents.models import UserMessage, SystemMessage

# Cargar .env
load_dotenv(find_dotenv(), encoding="utf-8-sig")

app = FastAPI()

# Configuración del cliente de Saptiva
SAPTIVA_API_KEY = os.getenv("SAPTIVA_API_KEY")
MODEL = SAPTIVA_LEGACY  # recomendado para clasificación de intención

if not SAPTIVA_API_KEY:
    raise ValueError("❌ No se encontró la API KEY en .env")

model_client = SaptivaAIChatCompletionClient(
    model=MODEL,
    api_key=SAPTIVA_API_KEY
)

# Diccionario de acciones
accionables = {
    "crear_credenciales": "Estoy generando tu credencial, un momento...",
    "solicitud_eventos": "Un momento, estoy generando solicitud_eventos.",
    "informacion_perfil": "Aquí tienes la información de tu perfil...",
    "informacion_membresia": "Aquí tienes la información de tu Membresía...",
    "informacion_beneficios": "Aquí tienes la información de los beneficios...",
    "informacion_comunidad": "Aquí tienes la información de las comunidades/noticias/informes...",
    "constancia_miembro": "Aquí tienes la información de la constancia...",
    "pregunta_general": "¿En qué puedo ayudarte?"
}

# Prompt dinámico
def prompt_member():
    prompt = """
Eres el asistente virtual de CANACO SERVYTUR León.

Tu tarea es analizar el mensaje del usuario y responder SOLO con un JSON válido que contenga:
- "mensaje": texto fijo y específico para cada acción.
- "action": una acción válida.

Acciones válidas y sus mensajes asociados:
"""
    for action, mensaje in accionables.items():
        prompt += f"""
- {action}
  {{
    "mensaje": "{mensaje}",
    "action": "{action}"
  }}
"""
    prompt += """
Ejemplos de frases personales (activan acción):

- "dame mi credencial"
- "quiero mis eventos"
- "dame mi perfil"
- "qué beneficios tengo"
- "dame mi constancia"
- "quiero saber de mi comunidad"
- "quiero saber de mis cursos"
- "quiero ver mis capacitaciones"

Ejemplos generales (responder con pregunta_general):

- "cómo consigo una credencial"
- "qué eventos hay en CANACO"
- "cómo puedo afiliarme"
- "perdí mi credencial"
- "noticias generales"

Si no estás seguro de la intención, responde con:
{
  "mensaje": "¿En qué puedo ayudarte?",
  "action": "pregunta_general"
}

Responde SOLO con el JSON válido, sin texto adicional ni explicaciones.
"""
    return prompt

@app.post("/detect_intent")
async def detect_intent(request: Request):
    body = await request.json()
    from_user = body.get("from")
    query = body.get("query")

    if not from_user or not query:
        return {"error": "Faltan campos requeridos: from, query"}

    # Construir mensajes con el SDK oficial
    messages = [
        SystemMessage(content=prompt_member()),
        UserMessage(content=query, source="user")
    ]

    # Llamada al modelo
    result = await model_client.create(messages)
    raw = result.content.strip()

    # Intentar parsear JSON
    try:
        parsed = json.loads(raw)
    except Exception:
        logging.warning(f"Respuesta no JSON válida: {raw}")
        parsed = None

    output = (
        {"from": from_user, "mensaje": parsed.get("mensaje"), "action": parsed.get("action")}
        if parsed and parsed.get("mensaje") and parsed.get("action")
        else {"from": from_user, "mensaje": accionables["pregunta_general"], "action": "pregunta_general"}
    )

    return output
