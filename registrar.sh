#!/bin/bash
# Uso: ./registrar.sh "Mensaje del hito o error"
FECHA=$(date +%Y-%m-%d)
echo "- [$FECHA] $1" >> bitacora_fractal.md
echo "Registrado en bitacora_fractal.md"
