import os
from dotenv import load_dotenv

# Forzar carga desde el archivo .env con soporte para BOM
load_dotenv(dotenv_path=".env", encoding="utf-8-sig")

api_key = os.getenv("SAPTIVA_API_KEY")

if api_key:
    print("✅ API Key detectada:", api_key[:8] + "..." + api_key[-4:])
else:
    print("❌ No se encontró SAPTIVA_API_KEY en el .env")
