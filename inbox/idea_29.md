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
**PROCESANDO VÓMITOS DE TOMÁS REIS**

**IDENTIDAD:** Mente (Técnico, Experto en Trading y Tarot)
**PROYECTO:** AIR-Bot (Agente Integral Reis)
**OBJETIVO DE LA RESPUESTA:** Precisión técnica y coherencia estructural.

---

## I. PROMPT DE INGENIERÍA: AIR-BOT

Este prompt define los requisitos técnicos y operativos para el desarrollo del agente `agente_air.py`.

### A. ARQUITECTURA DEL SISTEMA

| Componente | Especificación Técnica | Optimización/Constraint |
| :--- | :--- | :--- |
| Servidor (Host) | AWS Instance (T2/T3 Nano o Micro) | **Optimización Crítica:** Uso máximo de 1GB RAM. Dependencia estricta de procesamiento *in-memory* (BytesIO). |
| Plataforma AI | Google AI Plus (Gemini 3 Pro para Texto, Nano Banana para Edición) | **Acceso:** Vía `google-generativeai` SDK. |
| Interfaz Pública | Telegram Bot (API) | Uso de `python-telegram-bot` (preferible por robustez asíncrona) o `telebot`. |
| Base de Conocimiento (Log) | BestiaTantrica/fractal-mind | Almacenamiento persistente en archivos `.md`. Uso de una librería ligera de manejo de archivos (ej. `pathlib`). |

### B. REQUISITOS FUNCIONALES CLAVE

1.  **Lógica Condicional de Entrada (Handler Principal):**
    *   **Condición 1 (Edición Multimedia):** `[Entrada = Imagen + Texto]`.
        *   **Acción:** Llamada a Nano Banana (API de Edición). El texto es el prompt de instrucción.
        *   **Procesamiento:** La imagen no se guarda en disco. Se transfiere en memoria (BytesIO) al payload de la API.
    *   **Condición 2 (Generación de Contenido):** `[Entrada = Solo Texto]`.
        *   **Acción:** Llamada a Gemini 3 Pro.
        *   **Output (JSON/Structured):** 3 Guiones detallados (TikTok/Reels) + 1 Sugerencia de Prompt de Imagen para Portada.

2.  **Gestión de Cuotas (Hard Limit):**
    *   **Límite Diario Global:** 100 ediciones de imagen (Nano Banana).
    *   **Mecanismo:** Contador persistente (`quota.json` o `quota.md`). Debe resetearse automáticamente cada 24 horas (UTC).
    *   **Control por Usuario (Onboarding Hook):** Implementar un contador secundario para ofrecer **5 ediciones gratuitas** por `user_id` único, gestionado por el mismo `quota_manager`.

3.  **Integración con Fractal-Mind (Logging Detallado):**
    *   **Ruta de Almacenamiento:** `fractal-mind/proyectos/redes/clientes/[user_id].md`
    *   **Estructura del Log (Append):**
        ```markdown
        ---
        Fecha: [YYYY-MM-DD HH:MM:SS]
        Tipo de Interacción: [EDICION_IMAGEN | GENERACION_TEXTO]
        ---
        ## Pedido Original
        [Contenido del mensaje de Telegram]

        ## Resultado
        [Link Directo al Archivo Multimedia o Texto Generado]
        [Uso de Cuota: SI/NO]
        ```

### C. REQUISITOS DE OPTIMIZACIÓN (RAM/LATENCIA)

*   **Procesamiento In-Memory (BytesIO):** Absolutamente obligatorio para manejo de archivos grandes. La función de Telegram handler debe capturar la imagen y convertirla inmediatamente a un buffer de bytes antes de pasarla al SDK de Google AI.
*   **Asincronía:** Utilizar programación asíncrona (`async/await`) si se usa `python-telegram-bot` para manejar múltiples peticiones concurrentes sin saturar el bajo recurso de RAM.

---

## II. ESTRUCTURA DE CÓDIGO OPTIMIZADO

Se requiere una estructura modular clara para aislar la lógica de negocio (AI/API) de la infraestructura (Telegram/Logging).

```
air-bot/
├── agente_air.py               # 1. Main Handler (Telegram entry point)
├── config.py                   # 2. Configuración: Claves, límites y paths.
├── core/
│   ├── __init__.py
│   └── gemini_processor.py     # 3. Lógica AI: Comunicación con Google SDK.
└── utils/
    ├── __init__.py
    ├── quota_manager.py        # 4. Gestión de cuotas (100 diarias / 5 por usuario).
    └── logging_fractal.py      # 5. Escribir logs en formato Markdown.
```

### ESQUELETO DE FUNCIÓN CRÍTICA (`gemini_processor.py`)

```python
import io
from google import genai
# ...

def process_image_edit(image_bytes: io.BytesIO, instruction: str):
    """
    Procesa la edición de una imagen usando Nano Banana (o equivalente).
    La imagen se pasa como BytesIO, NO se accede al disco.
    """
    # 1. Verificar Cuota (Llamada a quota_manager)
    # 2. Inicializar modelo
    # 3. Crear el objeto GenerativePart a partir del buffer de BytesIO
    # 4. Llamada a la API de edición (Ej. Imagen + Prompt)
    # 5. Devolver el resultado (BytesIO o URL)
    pass

def generate_content_script(topic: str):
    """
    Genera 3 guiones y 1 prompt de imagen usando Gemini 3 Pro.
    """
    # 1. Definir la estructura JSON requerida en el prompt.
    # 2. Llamada a la API
    # 3. Devolver objeto estructurado.
    pass
```

---

## III. REFINAMIENTO ESTRATÉGICO

### A. NOMBRE DE NEGOCIO

**Nombre Confirmado:** **AIR: Agente Integral Reis** (Claro, técnico, fácil de recordar).

### B. EL GANCHO COMERCIAL (Onboarding Técnico)

*   **Implementación:** El `quota_manager.py` debe asignar un *flag* de `first_use` o un contador `free_edits` inicializado en 5 a cada nuevo `user_id` detectado.
*   **Métrica de Éxito:** La conversión de usuarios que consumen sus 5 ediciones gratuitas a usuarios que intentan la sexta (momento en que se introduce el módulo de "Cobro/Suscripción" futuro).
*   **Valor Añadido:** El foco no debe ser solo la cantidad (100 imágenes), sino la **velocidad** del procesamiento in-memory, diferenciándose de soluciones que requieren largos uploads/downloads.

### C. ESTRATEGIA DE VENTA (TELEGRAM FOCUS)

*   **Canal Vidriera:** El canal de Telegram debe ser utilizado como un repositorio de *case studies*. Cada publicación debe ser: `[Pedido Original del Cliente] -> [Resultado AIR-Bot]`.
*   **Automatización de Resultados:** Considerar si el `logging_fractal.py` puede generar automáticamente el *texto* para el post de lanzamiento, usando los datos del log de un usuario.

---

## IV. DRAFT DE LANZAMIENTO (BETA TESTERS)

**Canal:** Telegram / Redes
**Tono:** Directo, búsqueda de alto rendimiento.

**ASUNTO:** ⚠️ [AVISO TÉCNICO] AIR-Bot necesita 5 Beta Testers para edición multimedia IA.

**CUERPO DEL MENSAJE:**

He liberado el **AIR: Agente Integral Reis**, mi nuevo motor de edición multimedia potenciado por Gemini 3 Pro y Nano Banana.

AIR es un agente de Telegram diseñado para maximizar la conversión en Reels y TikToks, sin sobrecargar recursos. Necesito 5 perfiles exigentes que quieran llevar su contenido al siguiente nivel.

**¿Qué hace AIR?**

1.  **Edición Visual Instantánea:** Envías tu imagen + la instrucción de edición ("Haz el fondo más dramático", "Añade neón cyberpunk"). AIR lo procesa *in-memory* y te devuelve el resultado optimizado.
2.  **Guionización de Contenido:** Envías un tema ("Cómo ganar dinero con la IA"), y AIR te devuelve 3 guiones completos de 45 segundos + un prompt exacto para generar tu portada viral.

**OFERTA BETA (CRÍTICA DE RENDIMIENTO):**

Los 5 elegidos obtendrán **5 ediciones visuales COMPLETAMENTE GRATUITAS** (0% coste de prueba) para que evalúen la velocidad y calidad del motor Nano Banana.

**Requisito:** Documentar la latencia y la precisión del resultado.

Interesados, comenten con "BETA" y les daré acceso a la API privada del bot.

---
*Mente de Tomás Reis. Confirmado.*