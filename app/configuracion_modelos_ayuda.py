import os
from dotenv import load_dotenv, find_dotenv
from saptiva_agents.base import SaptivaAIChatCompletionClient

# Cargar variables de entorno
load_dotenv(find_dotenv(), encoding="utf-8-sig")
SAPTIVA_API_KEY = os.getenv("SAPTIVA_API_KEY")

if not SAPTIVA_API_KEY:
    raise ValueError("❌ No se encontró la API KEY en .env")

# 🔹 Saptiva Turbo
turbo_client = SaptivaAIChatCompletionClient(
    model="gemma2:27b",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva Cortex
cortex_client = SaptivaAIChatCompletionClient(
    model="qwen3:30b",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva Ops
ops_client = SaptivaAIChatCompletionClient(
    model="qwen2.5:72b-instruct",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva Legacy
legacy_client = SaptivaAIChatCompletionClient(
    model="llama3.3:70b",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva Coder
coder_client = SaptivaAIChatCompletionClient(
    model="deepseek-coder-v2:236b",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva OCR
ocr_client = SaptivaAIChatCompletionClient(
    model="Nanonets-OCR-s:F16",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva Embed (para embeddings, no chat)
embed_client = SaptivaAIChatCompletionClient(
    model="qwen3-embedding:8b",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva Guard
guard_client = SaptivaAIChatCompletionClient(
    model="llama-guard3:8b",
    api_key=SAPTIVA_API_KEY
)

# 🔹 Saptiva Multimodal
multimodal_client = SaptivaAIChatCompletionClient(
    model="gemma3:27b",
    api_key=SAPTIVA_API_KEY
)
