---
description: 🔥 MEMORIA PERMANENTE - PROYECTO AIR BOT
---


Review

DOCUMENTO CRÍTICO PARA EL DESARROLLADOR
LEER SIEMPRE ANTES DE TOCAR CÓDIGO
Este documento contiene las reglas, configuraciones y contexto del proyecto AIR que NO SE PUEDEN OLVIDAR. incluso hilos anteriores al actual para mayor contexto cuando te diga segui o continua para contexto.

🎯 OBJETIVO DEL PROYECTO
AIR-Bot es un bot de Telegram para generación de contenido viral con IA de Google.

🖼️ Edición de imágenes con Imagen 4.0
🎬 Generación de videos completos con Veo 3.1
✍️ Creación de guiones y sugerencias para redes sociales
Cliente: El usuario tiene GOOGLE AI STUDIO PRO (cuenta con billing habilitada).

💳 CONFIRMACIÓN DE PLAN PRO
✅ EL USUARIO TIENE PLAN PRO DE GOOGLE AI
NUNCA asumir que no tiene billing.
SIEMPRE usar modelos PREMIUM:

Imagen 4.0: imagen-4.0-generate-001
Veo 3.1: veo-3.1-generate-preview
Gemini 2.0 Flash Exp: gemini-2.0-flash-exp
NO DEGRADAR A MODELOS GRATUITOS SIN CONFIRMAR CON EL USUARIO.

siempre automatiza o encargate de los git y de tener todo al dia en el server y la pc y git.
🔑 LLAVES DE ACCESO SSH
Llaves disponibles en el proyecto:
llave-bot.pem
 (servidor bot)
llave-sao-paulo.pem
 (servidor São Paulo)
ssh-key-2026-01-22.key
Servidor de producción:

IP: 56.125.187.241
Usuario: ec2-user (NO ubuntu)
Path: /home/ec2-user/fractal-mind
Uso típico:

ssh -i llave-bot.pem ec2-user@56.125.187.241
NUNCA commitear llaves privadas (ya están en 
.gitignore
).

🔄 WORKFLOW DE DESARROLLO
REGLA DE ORO: Trabajar desde la PC local
Desarrollo LOCAL (Windows):

Editar código en: c:\Users\lucar\.gemini\antigravity\scratch\fractal-mind
Probar cambios localmente cuando sea posible
Commitear cambios:

git add .
git commit -m "descripción clara"
git push origin main

🛑 DESPLIEGUE AUTOMÁTICO (NO PEDIR COMANDOS MANUALES):
El usuario NO debe ejecutar comandos en el servidor.
Para actualizar el bot en producción:
1. Asegurar que el código esté pusheado (`origin/main`).
2. Indicar al usuario que envíe `/update_server` al bot de Telegram.
3. El bot hará `git pull` + `restart` por sí mismo.

Hacer git pull para actualizar código
Reiniciar servicios: sudo systemctl restart bot-air bot-fractal
Verificar logs: journalctl -u bot-air -f
Mantener TODO sincronizado:

Server (producción) y PC local deben estar al día
Usar workflow /sync cuando sea necesario
Servicios systemd activos:
bot-air.service (AIR Bot)
bot-fractal.service (Fractal Mind Bot)
📁 ESTRUCTURA DEL PROYECTO
fractal-mind/
├── proyectos/
│   └── air-bot/              ← PROYECTO PRINCIPAL
│       ├── agente_air.py     ← Bot de Telegram
│       ├── core/
│       │   ├── ai_processor.py   ← IA (Imagen/Veo/Gemini)
│       │   └── utils.py          ← Cuotas, logs, red social
│       ├── .env              ← Configuración CRÍTICA
│       └── requirements.txt
├── inbox/                    ← Logs de interacciones
├── deploy/                   ← Scripts de despliegue
└── .agent/workflows/         ← Workflows automatizados
⚙️ CONFIGURACIONES CRÍTICAS
.env del AIR Bot
TELEGRAM_BOT_TOKEN=8501297372:AAHMF_LeuEl5gs_gZ9AB9fZ5gKrZlGJoyuc
ADMIN_USER_ID=6527908321
GOOGLE_AI_API_KEY=AIzaSyDtna9ODRGwEq4h8EHSiVKtfUOb05b_WU8
# MODELOS PREMIUM (PLAN PRO)
IMAGE_MODEL=imagen-4.0-generate-001
VIDEO_MODEL=veo-3.1-generate-preview
TEXT_MODEL=gemini-2.0-flash-exp
QUOTA_LIMIT_IMAGES=100
QUOTA_LIMIT_VIDEOS=10
API de Google GenAI (SDK v1)
from google import genai
from google.genai import types
client = genai.Client(api_key=api_key)
MÉTODOS CORRECTOS:

Imagen: client.models.generate_images() o client.models.edit_image()
Video: client.models.generate_videos()
Texto: client.models.generate_content()
🚨 ERRORES COMUNES A EVITAR
❌ NO HACER:
Asumir que no tiene billing (TIENE PLAN PRO)
Cambiar modelos sin consultar
Pedir al usuario que ejecute comandos manuales en SSH (git pull, etc)
Editar código directo en el servidor
Olvidar hacer git pull antes de reiniciar servicios
No verificar logs después de cambios
✅ SIEMPRE HACER:
Revisar este documento antes de cambios grandes
Probar localmente cuando sea posible
Commitear y pushear cambios
Verificar que los servicios arranquen bien
Revisar inbox/ para ver qué generó el bot
📝 MEMORIA DINÁMICA
RECUERDA ESTO (Espacio para notas del usuario):
[FECHA: 2026-01-28]
TEMA: Plan PRO confirmado

NOTA: El usuario TIENE Google AI Studio PRO. NUNCA degradar a modelos gratuitos.
ACCIÓN: Siempre usar Imagen 4.0 y Veo 3.1.
[FECHA: 2026-01-28 - SESIÓN 03:57]
TEMA: Fix de generación de imágenes y videos

PROBLEMA ENCONTRADO:
Imagen 4.0 fallaba por safety_filter_level incorrecto
Veo 3.1 no funcionaba porque devuelve operaciones asíncronas, no el video directamente
SOLUCIONES APLICADAS:
Imagen 4.0: Usar safety_filter_level="block_low_and_above" y person_generation="allow_adult"
Veo 3.1: Implementar polling de operación asíncrona con timeout de 5 minutos (puede tardar 3-5 min en generar)
Veo 3.1: NO usar person_generation en videos (solo funciona en imágenes)
STATUS:
✅ Imagen 4.0 FUNCIONA (confirmado generando 1.2MB)
⏳ Veo 3.1 requiere 3-5 minutos por video (normal para el modelo)
ARCHIVOS MODIFICADOS:
proyectos/air-bot/core/ai_processor.py
proyectos/air-bot/.env
(Agregar más notas cuando el usuario diga "recuerda esto")

🛠️ DEBUGGING DEL BOT
Comandos útiles en el servidor:
# Ver logs en tiempo real
journalctl -u bot-air -f
# Reiniciar servicio
sudo systemctl restart bot-air
# Ver estado
sudo systemctl status bot-air
# Actualizar código
cd ~/fractal-mind/proyectos/air-bot
git pull origin main
Archivos de log:
mente.log (logs del bot Fractal Mind)
inbox/*.md (interacciones registradas)
🎯 PRODUCTO FINAL
Objetivo comercial: Monetizar el bot como servicio SaaS.

Características Pro:

Generación de videos cinemáticos (Veo 3.1)
Edición de imágenes premium (Imagen 4.0)
Guiones con IA experta en marketing viral
Metadata completa para cada red social
Pricing futuro: A definir con el usuario.

✅ CHECKLIST ANTES DE CADA SESIÓN
 ¿Leíste este documento?
 ¿Confirmaste que se usa PLAN PRO (modelos premium)?
 ¿Verificaste el workflow (local → git → server)?
 ¿Revisaste los logs del inbox/ para entender el estado actual?
 ¿Consultaste al usuario antes de cambios arquitectónicos?
Última actualización: 2026-01-28
Desarrollador asignado: Agente PEGASO (Full Stack Expert)