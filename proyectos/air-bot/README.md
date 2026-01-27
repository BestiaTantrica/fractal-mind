# 🤖 AIR-Bot - Agente Integral Reis

Bot de Telegram para generación completa de contenido para redes sociales usando Google Generative AI (Veo 3.1, Gemini Pro).

## 🎯 ¿Qué hace?

**Paquete completo de contenido listo para publicar:**

### 🖼️ 1. Edición de Imágenes
- Edita fotos con IA  
- Optimiza para redes sociales
- Cuota: 100 imágenes/día

### 🎬 2. Generación de Videos 
- Videos de 8 segundos con audio nativo
- Formato optimizado por plataforma (TikTok, Instagram, YouTube Shorts, etc.)
- Incluye: caption, descripción, hashtags, CTA, mejor horario
- Powered by Google Veo 3.1

### ✍️ 3. Guiones Creativos
- 3 opciones de guión por solicitud
- Sugerencias de portada
- Hashtags optimizados
- ¡No consume cuota!

## 📱 Plataformas Soportadas

- ✅ TikTok
- ✅ Instagram Reels
- ✅ YouTube Shorts
- ✅ Facebook
- ✅ WhatsApp

## 🚀 Instalación

### Prerequisitos

- Python 3.9 o superior
- Cuenta de Google AI con acceso a Gemini y Veo
- Bot de Telegram (creado con @BotFather)
- Repositorio fractal-mind clonado (para logs)

### Pasos

1. **Clonar el proyecto**
```bash
cd c:\Users\lucar\.gemini\antigravity\scratch
cd air-bot
```

2. **Crear entorno virtual**
```bash
python -m venv venv
.\venv\Scripts\activate  # En Windows
# source venv/bin/activate  # En Linux/Mac
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar el archivo de ejemplo
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Editar .env con tus credenciales
# Necesitas:
# - TELEGRAM_BOT_TOKEN (de @BotFather)
# - GOOGLE_AI_API_KEY (de Google AI Studio)
```

5. **Configurar fractal-mind**
```bash
# Asegúrate de que la ruta en .env apunte a tu repo fractal-mind
# Por defecto: FRACTAL_MIND_PATH=../fractal-mind
```

## 🔑 Obtener Credenciales

### Token de Telegram

1. Abre Telegram y busca `@BotFather`
2. Envía `/newbot`
3. Sigue las instrucciones
4. Copia el token que te da

### API Key de Google AI

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea un nuevo proyecto o selecciona uno existente
3. Genera una nueva API key
4. Copia la clave

**Nota:** Google Veo 3.1 está en preview limitado. Si no tienes acceso, el bot funcionará con simulación de metadata (caption, hashtags, etc.) pero sin generación real de video.

## ▶️ Ejecutar el Bot

```bash
python agente_air.py
```

Deberías ver:
```
==================================================
🤖 AIR-BOT - AGENTE INTEGRAL REIS
==================================================
✅ Bot iniciado correctamente
📊 Cuota imágenes: 100/día
🎬 Cuota videos: 50/día
⏳ Escuchando mensajes...
==================================================
```

## 📖 Uso

### Comandos Disponibles

- `/start` - Mensaje de bienvenida
- `/ayuda` - Guía de uso
- `/cuota` - Ver estado de cuotas

### Ejemplos de Uso

**Editar Imagen:**
```
1. Envía una foto
2. En el caption: "Hazla más profesional y dramática"
3. ¡Listo!
```

**Generar Video:**
```
Usuario: "Video de café humeante para TikTok"
Bot devuelve:
  - Video optimizado (simulado en dev)
  - Caption: "POV: Descubriste el café perfecto ☕✨"
  - Descripción completa con CTAs
  - Hashtags: #FYP #CoffeeTok #Viral...
  - Mejor horario: 7-9 AM o 6-8 PM
```

**Generar Guiones:**
```
Usuario: "Ideas para Reels de gimnasio"
Bot devuelve:
  - 3 guiones creativos completos
  - Sugerencia de imagen de portada
  - Hashtags optimizados
  - Mejor horario de publicación
```

## 📂 Estructura del Proyecto

```
air-bot/
├── agente_air.py              # Bot principal
├── core/
│   ├── __init__.py
│   ├── ai_processor.py        # Google AI integration
│   └── utils.py               # Cuotas y logging
├── data/
│   └── quota.json             # Cuotas diarias (auto-generado)
├── .env                       # Configuración (crear desde .env.example)
├── .env.example               # Plantilla de configuración
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔧 Configuración Avanzada

### Límites de Cuota

Edita en `.env`:
```env
QUOTA_LIMIT_IMAGES=100
QUOTA_LIMIT_VIDEOS=50
```

### Modelos de IA

Edita en `.env`:
```env
IMAGE_MODEL=gemini-pro-vision
VIDEO_MODEL=veo-3.1
TEXT_MODEL=gemini-pro
```

### Ruta de fractal-mind

Ajusta según tu instalación:
```env
FRACTAL_MIND_PATH=../fractal-mind
```

## 📊 Logs y Seguimiento

Los logs de usuarios se guardan en:
```
fractal-mind/proyectos/redes/clientes/[user_id].md
```

Formato:
```markdown
## 2026-01-26 21:00:00 UTC
### ID de Usuario: 123456 - Video Generado
**Tipo:** VIDEO_GENERACION
**Input:** "Video de café para TikTok"
**Caption:** "El café perfecto ☕✨"
**Hashtags:** #FYP #CoffeeTok #Viral
**Cuota Video:** 5/50
---
```

## 🚨 Solución de Problemas

### Error: "TELEGRAM_BOT_TOKEN no configurado"
- Verifica que creaste el archivo `.env`
- Asegúrate de copiar correctamente el token de @BotFather

### Error: "google-generativeai no está disponible"
- Ejecuta: `pip install -r requirements.txt`

### El bot no responde
- Verifica que el bot esté corriendo (`python agente_air.py`)
- Revisa los logs en consola

### Videos no se generan
- Google Veo 3.1 requiere acceso preview
- El bot generará todo el metadata pero el video será placeholder
- Contacta a Google AI para acceso a Veo

## 🌐 Despliegue en AWS

### Preparación

1. **Crear instancia EC2**
   - Ubuntu 22.04 LTS
   - Mínimo: t2.micro (1GB RAM)
   - Puertos: 22 (SSH), 443 (HTTPS opcional)

2. **Conectar y configurar**
```bash
ssh -i tu-key.pem ubuntu@tu-ip

# Instalar Python y dependencias
sudo apt update
sudo apt install python3-pip python3-venv git -y

# Clonar proyectos
git clone https://github.com/BestiaTantrica/fractal-mind.git
# Subir air-bot con scp o git
```

3. **Configurar como servicio**
```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/air-bot.service
```

Contenido:
```ini
[Unit]
Description=AIR Bot Service
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/air-bot
Environment="PATH=/home/ubuntu/air-bot/venv/bin"
ExecStart=/home/ubuntu/air-bot/venv/bin/python agente_air.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Iniciar servicio**
```bash
sudo systemctl daemon-reload
sudo systemctl enable air-bot
sudo systemctl start air-bot
sudo systemctl status air-bot
```

## 📝 Notas de Desarrollo

- ⚠️ **Google Veo 3.1** está en preview limitado. El sistema está listo pero necesita acceso a la API.
- ✅ **Edición de imágenes** actualmente usa Gemini Vision para análisis. Para edición real, integrar con API de edición de imágenes.
- ✅ **Todos los módulos** están optimizados para 1GB RAM usando BytesIO.

## 🤝 Contribuir

Este es un proyecto personal. Para sugerencias o reportes de bugs, contacta directamente.

## 📄 Licencia

Proyecto privado - Todos los derechos reservados

---

**Desarrollado por Tomás Reis**  
AIR: Agente Integral Reis  
Powered by Google Generative AI
