# Idea de Tomás

## Entrada:
Proyecto "AIR-Bot"
Contexto del Sistema:

Servidor: AWS Instance (1GB RAM) - Optimizar para bajo consumo de recursos.

Plan Activo: Google AI Plus (200GB) - Acceso a Gemini 3 Pro y Nano Banana (100 imágenes/día).

Base de Conocimiento: Integrar con el repositorio BestiaTantrica/fractal-mind para guardar logs y preferencias en Markdown.

Objetivo: Desarrollar un script en Python (agente_air.py) que gestione un bot de Telegram para edición multimedia mediante IA.

Especificaciones Técnicas:

Lógica de Entrada:

Si recibe Imagen + Texto: Usar el modelo de edición de imagen (Nano Banana) para aplicar los cambios pedidos por el cliente.

Si recibe Solo Texto: Generar 3 opciones de guion para TikTok/Reels y una sugerencia de prompt de imagen para la portada.

Gestión de Cuotas: - Implementar un contador persistente en un archivo JSON o Markdown para no exceder las 100 imágenes diarias.

Optimización de RAM:

No descargar archivos pesados al server. Usar BytesIO para procesar imágenes en memoria o enviarlas directamente a la API de Google Generative AI.

Almacenamiento en Fractal-Mind:

Cada interacción debe generar un archivo .md en fractal-mind/proyectos/redes/clientes/[nombre_usuario].md con: Fecha, Pedido original, y Link al resultado.

Código Requerido:

Usar python-telegram-bot o telebot.

Usar google-generativeai (SDK de Google).

Estructura modular para que yo pueda agregar la función de "Cobro/Suscripción" en el futuro.

Tu estrategia de arranque (El "Plan de Ataque")
Mientras el mejorador te arma el código, podés ir haciendo esto para no perder tiempo:

Nombre del Negocio: Algo que pegue, como "Bestia Viral" o "AIR: Agente Integral".

El Gancho: Como tenés 100 imágenes por día, podés darte el lujo de regalar 5 ediciones gratis por cliente nuevo. No te cuesta nada y el impacto visual de ver su producto "embellecido" por la IA es lo que cierra la venta.

Venta por Telegram: No te vuelvas loco con webs. Un canal de Telegram donde publiques el "Antes y Después" de lo que hace tu bot es tu mejor vidriera.

¿Te gustaría que redacte el primer post de "Lanzamiento" para que lo compartas en tus grupos o redes y ver quién pica? Podés decir que estás buscando 5 "beta testers" para tu nueva IA de edición.

## Respuesta Mente:
Recibido. Proceso los datos.

## PROCESAMIENTO DE IDEAS: PROYECTO AIR-BOT

La estrategia de arranque es sólida. Procedo a estructurar la arquitectura técnica y a transformar la estrategia comercial en un **Prompt de Ingeniería** de alta eficiencia.

---

## I. ARQUITECTURA TÉCNICA Y OPTIMIZACIÓN (AWS 1GB RAM)

El enfoque principal debe ser la eficiencia de memoria y la minimización de latencia en I/O de disco.

### 1. Optimización Crítica de Recursos

| Componente | Requisito | Estrategia de Optimización |
| :--- | :--- | :--- |
| **Memoria (RAM)** | AWS 1GB Constraint | Uso exclusivo de `io.BytesIO` para manejo de imágenes. **Prohibido** guardar archivos temporales en el disco del servidor. La imagen se carga a memoria (RAM) desde Telegram y se envía directamente al SDK de Google. |
| **Quota Counter** | Persistencia, bajo I/O | Usar un archivo `quota_status.json` simple para el contador diario (UserID: {count, last_reset}). JSON es más rápido y liviano de parsear que Markdown para esta función específica. |
| **SDK Telegram** | Rendimiento | Se utilizará `python-telegram-bot` (o `telebot`), priorizando un enfoque asíncrono (`asyncio`) para manejar múltiples peticiones sin bloquear el hilo principal. |
| **Base de Conocimiento** | `fractal-mind` | Utilizar el SDK de Git o comandos del sistema para realizar *commit* y *push* diferidos (batch logging) cada 10 o 20 interacciones, en lugar de en cada log, para reducir la carga de CPU y la latencia de red. |

### 2. Estructura Modular de `agente_air.py`

La estructura debe ser modular (modularidad exigida para la futura integración de "Cobro/Suscripción").

| Módulo | Responsabilidad | Dependencias Clave |
| :--- | :--- | :--- |
| `core_bot.py` | Inicialización del bot, manejo de comandos (`/start`, `/help`), y enrutamiento de mensajes. | `python-telegram-bot` |
| `quota_manager.py` | Gestión del contador persistente (`quota_status.json`). Lógica de reinicio diario de las 100 imágenes y gestión de las 5 ediciones gratuitas por cliente nuevo. | `json`, `datetime` |
| `fractal_logger.py` | Creación de archivos `.md` en `fractal-mind/proyectos/redes/clientes/[usuario].md`. Gestión del formato (Fecha, Pedido, Link Resultado). | `git` (o API de repositorio) |
| `ai_handler.py` | Interacción directa con `google-generativeai`. Contiene la lógica de decisión: si es imagen+texto (Nano Banana), o solo texto (Gemini Pro). | `google-generativeai`, `io.BytesIO` |
| `config.py` | Almacenamiento seguro de tokens y rutas (Telegram, Google API Key, ruta `fractal-mind`). | `dotenv` |

### 3. Lógica de Decisión (Flujo de Entrada)

El módulo `core_bot.py` debe implementar la siguiente lógica para el procesamiento de mensajes:

1.  **Recepción:** Obtener el ID de Usuario y el mensaje entrante.
2.  **Verificación de Quota:** `quota_manager.check_quota(user_id)`. Si es excedida y el usuario no está en la lista de beta testers, enviar mensaje de "Cuota Excedida".
3.  **Tipo de Entrada:**
    *   **Si `message.photo` Y `message.caption` (Imagen + Texto):**
        *   Llamar a `quota_manager.decrement_quota(user_id)`.
        *   Obtener el archivo de la imagen, cargarlo a `BytesIO`.
        *   Llamar a `ai_handler.edit_image(image_bytes, caption, model='nano-banana')`.
        *   Registrar en `fractal_logger.log_success()`.
        *   Enviar resultado al usuario.
    *   **Si `message.text` Y NO `message.photo` (Solo Texto):**
        *   Llamar a `ai_handler.generate_scripts(text, model='gemini-3-pro')` para obtener: 3 guiones y 1 prompt de portada.
        *   Registrar en `fractal_logger.log_success()` (sin decrementar quota, ya que no se consume una imagen del límite diario).
        *   Enviar resultados al usuario.

---

## IV. PLAN DE ATAQUE Y PROMPT DE INGENIERÍA

El objetivo es convertir la estrategia comercial en un *prompt* que genere el contenido de alto impacto para el lanzamiento.

### 1. Nombre y Gancho Definidos

*   **Nombre del Negocio:** **AIR: Agente Integral (Inteligencia de Redes)**
*   **Gancho:** 5 ediciones de video/imagen gratuitas para los primeros 5 beta testers.
*   **Canal:** Telegram (Vidriera "Antes y Después").

### 2. Prompt de Ingeniería para el Lanzamiento

**Objetivo del Prompt:** Generar una publicación corta, de alta conversión, optimizada para Telegram/RRSS, buscando 5 beta testers.

**[PROMPT DE INGENIERÍA]**

**Rol:** Eres un Copywriter técnico y directo, enfocado en la conversión inmediata. El tono debe ser urgente, profesional y orientado al valor (FOMO/Beta Test).

**Contexto del Producto (AIR):** Bot de Telegram para edición de contenido (TikTok/Reels) asistida por IA. Utiliza modelos avanzados (Nano Banana) para transformar imágenes y Gemini Pro para crear guiones de video. El principal dolor que resuelve es la *creación rápida de contenido visualmente superior*.

**Requisito de la Campaña:** Necesitamos 5 Beta Testers que nos permitan usar su contenido (Antes/Después) como prueba social.

**Instrucciones de Salida:**

1.  **Título (Emoji-Driven):** Máximo 8 palabras. Foco en "IA", "Edición" y "Gratis".
2.  **Cuerpo (El Gancho):**
    *   Declarar el límite de 5 cupos.
    *   Definir la oferta: 5 ediciones *premium* totalmente gratuitas (valoradas en $X).
    *   Claridad sobre el intercambio: Necesitamos su "Antes" para mostrar el "Después" en nuestro canal.
    *   Definición del público objetivo: Creadores de contenido, emprendedores digitales, e-commerce.
3.  **Llamada a la Acción (CTA):** Clara y única. Debe dirigir a un DM o un link de grupo específico de Telegram.
4.  **Hashtags (Técnicos/Virales):** Incluir #AI, #EdicionIA, #BetaTest.

**Formato:** Entregar en 3 versiones (Formal, Directo (Telegram), y Versión para Post de Twitter/X).

---

**Resumen de la Tarea:**

1.  **Ejecutar:** Implementación modular de `agente_air.py` siguiendo la arquitectura definida, priorizando `BytesIO` y el contador `quota_status.json`.
2.  **Generar:** Ejecutar el Prompt de Ingeniería para obtener el material de lanzamiento del Beta Test.
3.  **Integrar:** Asegurar que `fractal_logger.py` tenga credenciales de repositorio y pueda gestionar la ruta `fractal-mind/proyectos/redes/clientes/`.