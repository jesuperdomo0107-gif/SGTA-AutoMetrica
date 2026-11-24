#!/usr/bin/env bash
# Script de construcción para Render (Backend FastAPI + PostgreSQL)
set -o errexit

echo "=== 1. Actualizando pip e instalando dependencias ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== 2. Ejecutando sincronización de esquema y creación de superusuario ==="
python init_prod.py

echo "=== 3. Verificando carpeta de archivos estáticos ==="
mkdir -p static

echo "=== Build completado exitosamente ==="
