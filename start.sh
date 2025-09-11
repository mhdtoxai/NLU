#!/bin/bash
# Script para iniciar Saptiva BOT con Uvicorn
uvicorn main:app --host 0.0.0.0 --port 8080 --reload