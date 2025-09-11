"""
Módulo de configuración de la aplicación.
Se encarga de cargar variables de entorno y exponerlas al resto del proyecto.
"""
import os
from dotenv import load_dotenv, find_dotenv
from saptiva_agents import SAPTIVA_TURBO

# Cargar variables desde .env
load_dotenv(find_dotenv(), encoding="utf-8-sig")

# Clave de API
SAPTIVA_API_KEY = os.getenv("SAPTIVA_API_KEY")

if not SAPTIVA_API_KEY:
    raise ValueError("❌ No se encontró la API KEY en .env")

# Modelo por defecto (puede cambiar a SAPTIVA_OPS si es necesario)
MODEL = SAPTIVA_TURBO
