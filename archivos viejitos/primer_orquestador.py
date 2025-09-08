import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from saptiva_agents import SAPTIVA_OPS  # SAPTIVA_TURBO
from saptiva_agents.base import SaptivaAIChatCompletionClient
from saptiva_agents.models import UserMessage, SystemMessage

# Cargar .env
load_dotenv(dotenv_path=".env", encoding="utf-8-sig")

app = FastAPI()

# Configuración del cliente de Saptiva
SAPTIVA_API_KEY = os.getenv("SAPTIVA_API_KEY")
MODEL = SAPTIVA_OPS  # recomendado para clasificación robusta y rápida

if not SAPTIVA_API_KEY:
    raise ValueError("❌ No se encontró la API KEY en .env")

model_client = SaptivaAIChatCompletionClient(
    model=MODEL,
    api_key=SAPTIVA_API_KEY
)

# Prompt de clasificación 
def prompt_member():
    return """
Eres el asistente virtual de CANACO SERVYTUR León.

Tu tarea es analizar el mensaje del usuario y responder SOLO con un JSON válido que contenga:

- "mensaje": texto fijo y específico para cada acción.
- "action": una acción válida.

Acciones válidas y sus mensajes asociados:

- crear_credenciales
  {
    "mensaje": "Estoy generando tu credencial, un momento...",
    "action": "crear_credenciales"
  }

- solicitud_eventos / capacitaciones / cursos
  {
    "mensaje": "Un momento, estoy generando solicitud_eventos.",
    "action": "solicitud_eventos"
  }

- informacion_perfil
  {
    "mensaje": "Aquí tienes la información de tu perfil...",
    "action": "informacion_perfil"
  }

- informacion_membresia / Pago_membresias
  {
    "mensaje": "Aquí tienes la información de tu Membresía...",
    "action": "informacion_membresia"
  }

- informacion_beneficios
  {
    "mensaje": "Aquí tienes la información de los beneficios...",
    "action": "informacion_beneficios"
  }

- informacion_comunidad / informacion_noticias / informacion_informes
  {
    "mensaje": "Aquí tienes la información de las comunidades/noticias/informes...",
    "action": "informacion_comunidad"
  }

- constancia_miembro
  {
    "mensaje": "Aquí tienes la información de la constancia...",
    "action": "constancia_miembro"
  }

- pregunta_general
  {
    "mensaje": "¿En qué puedo ayudarte?",
    "action": "pregunta_general"
  }

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

    # 1️⃣ Llamada al modelo para clasificación
    result = await model_client.create(messages)
    raw = result.content.strip()

    # Intentar parsear JSON
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = None

    action = parsed.get("action") if parsed else "pregunta_general"
    mensaje = parsed.get("mensaje") if parsed else "¿En qué puedo ayudarte?"

    # 2️⃣ Orquestador: validaciones de datos adicionales según la acción
    # Ejemplo: para credenciales pedimos número de socio (5 dígitos)
    if action == "crear_credenciales":
        numero_socio = body.get("numero_socio")
        if not numero_socio or not numero_socio.isdigit() or len(numero_socio) != 5:
            return {
                "from": from_user,
                "mensaje": "Para generar tu credencial necesito tu número de socio (5 dígitos). ¿Podrías compartirlo?",
                "action": "solicitar_dato",
                "dato_requerido": "numero_socio"
            }

    # Ejemplo: para membresías pedimos RFC
    if action == "informacion_membresia":
        rfc = body.get("rfc")
        if not rfc or len(rfc) not in (12, 13):
            return {
                "from": from_user,
                "mensaje": "Para mostrarte tu Membresía necesito tu RFC (12 o 13 caracteres). ¿Me lo proporcionas?",
                "action": "solicitar_dato",
                "dato_requerido": "rfc"
            }

    # Ejemplo: para eventos/capacitaciones podemos pedir una fecha
    if action == "solicitud_eventos":
        fecha = body.get("fecha")
        if not fecha:
            return {
                "from": from_user,
                "mensaje": "¿Sobre qué fecha te interesa ver los eventos o capacitaciones?",
                "action": "solicitar_dato",
                "dato_requerido": "fecha"
            }

    # 3️⃣ Respuesta final
    return {
        "from": from_user,
        "mensaje": mensaje,
        "action": action
    }
