import re
import re
import json, logging

from utils.match_rules import match_rules
from data.accionables import accionables
from prompts.prompts import build_prompt
from config import MODEL, SAPTIVA_API_KEY
import json, logging
from saptiva_agents.models import UserMessage, SystemMessage
from saptiva_agents.base import SaptivaAIChatCompletionClient

model_client = SaptivaAIChatCompletionClient(model=MODEL, api_key=SAPTIVA_API_KEY)

async def detect_intent_service(user: str, query: str) -> dict:
    # Capa 1: reglas
    rule_match = match_rules(query)
    if rule_match:
        print("solo match_rules")
        return {"from": user, **rule_match}

    # Capa 2: modelo con Prompteo
    print("Llamando al modelo")
    messages = [
        SystemMessage(content=build_prompt()),
        UserMessage(content=query, source="user")
    ]
    result = await model_client.create(messages)
    raw = result.content.strip()

    # 🔹 Extraer solo el JSON válido
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if match:
        raw = match.group(0)
    try:
        parsed = json.loads(raw)
    except Exception:
        logging.warning(f"Respuesta no JSON válida: {raw}")
        parsed = None

    return (
        {"from": user, "mensaje": parsed.get("mensaje"), "action": parsed.get("action")}
        if parsed and parsed.get("mensaje") and parsed.get("action")
        else {"from": user, "mensaje": accionables["pregunta_general"], "action": "pregunta_general"}
    )
