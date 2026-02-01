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
**Mente de Tomás Reis: Procesamiento y Planificación Técnica.**

El proyecto "AIR-Bot" es viable bajo las restricciones de recursos establecidas. La optimización de RAM mediante `BytesIO` es la estrategia crítica.

## 1. Plan de Ataque Técnico (Arquitectura del Sistema)

Para garantizar la modularidad, optimización y escalabilidad, el sistema se estructurará en tres módulos principales.

| Módulo | Objetivo | Optimización |
| :--- | :--- | :--- |
| `agente_air.py` | Controlador principal y manejo de handlers de Telegram. | Mínima lógica, solo enrutamiento. |
| `core/ai_processor.py` | Interfaz con `google-generativeai`. Manejo de la lógica de procesamiento (Texto vs. Imagen+Texto). | Implementación estricta de `BytesIO` para imágenes. |
| `core/utils.py` | Gestión de la persistencia: Cuotas y Logs. | Uso de JSON para cuotas (acceso rápido) y Markdown para logs (integración con Fractal-Mind). |

---

## 2. Prompt de Ingeniería (Generación de Código Base)

**Objetivo del Prompt:** Solicitar el código inicial (`agente_air.py`, `core/ai_processor.py`, `core/utils.py`) que implemente la lógica de entrada, la gestión de cuotas y la optimización de RAM.

---

**PROMPT PARA MODELO AVANZADO (EJ: GEMINI 3 PRO / GPT-4):**

```prompt
Actúa como un arquitecto de software experto en sistemas de bajo consumo de recursos (1GB RAM). Debes escribir el scaffold completo para un agente de Telegram en Python que interactúa con la API de Google Generative AI (Gemini).

**Requisitos Críticos del Sistema 'AIR-Bot':**

1.  **Librerías:** Usar `python-telegram-bot` (o `telebot`) y `google-generativeai`.
2.  **Optimización de Memoria (AWS 1GB RAM):** El bot NUNCA debe guardar archivos pesados en disco. Las imágenes recibidas deben ser manejadas en memoria usando el módulo `io.BytesIO` antes de ser enviadas a la API de Google.
3.  **Estructura Modular:** Generar 3 archivos: `agente_air.py` (Main), `core/ai_processor.py` (API Logic), `core/utils.py` (Persistence).
4.  **Gestión de Cuotas (AIR_QUOTA):** Implementar un sistema persistente en `core/utils.py` para llevar la cuenta de las ediciones de imagen realizadas hoy (límite 100). Usar un archivo JSON (`data/quota.json`) que almacene `{ "date": "YYYY-MM-DD", "count": 0 }`. Debe resetearse diariamente.
5.  **Logging (Fractal-Mind):** Cada interacción exitosa debe generar un archivo Markdown en la ruta `fractal-mind/proyectos/redes/clientes/[user_id].md` con formato append (o crear uno nuevo si no existe), siguiendo esta estructura:

    ```markdown
    ## [Fecha y Hora UTC]
    ### ID de Usuario: [user_id] - Pedido Original
    **Tipo de Interacción:** [IMAGEN_EDICION / SCRIPT_GENERACION]
    **Input:** [Texto original del usuario]
    **Estado de Cuota:** [X/100]
    **Link al Resultado:** [Link directo de Telegram al archivo final o URL de la imagen generada, si aplica]
    ---
    ```

**Funcionalidades de los Handlers:**

A. **Handler `/start`:** Bienvenida e instrucciones.
B. **Handler de Imagen + Texto (Edición):**
    *   Chequear Cuota. Si > 100, responder: "Cuota diaria agotada."
    *   Descargar imagen a `BytesIO`.
    *   Llamar a `gemini-nano-banana` (simulado por ahora) con la imagen y el texto de instrucción.
    *   Si es exitoso, actualizar la cuota y guardar el log.
    *   Enviar la imagen resultante al usuario.
C. **Handler de Solo Texto (Guion/Prompt):**
    *   Llamar a `gemini-3-pro` para generar:
        *   Título pegadizo.
        *   3 opciones de guion corto para TikTok/Reels.
        *   1 sugerencia de `prompt` para la imagen de portada.
    *   Formatear la respuesta en Markdown.
    *   Guardar el log (esta acción NO consume cuota de imagen).

**Instrucciones para el código:** Usar nombres de funciones claros (`process_image_edit`, `generate_script_and_prompt`). Incluir comentarios explicando la lógica de optimización de memoria.

---

## 3. Estrategia Operativa (Respuesta al "Plan de Ataque")

**Nombre del Negocio:**
Confirmado: **AIR: Agente Integral Reis.** (Directo, técnico, con resonancia personal).

**El Gancho (5 Ediciones Gratis):**
Estrategia aprobada. El impacto visual es el conversor más potente. La limitación de 100 al día permite gestionar 20 nuevos beta-testers diariamente sin impacto financiero, o escalar directamente a clientes de pago.

**Ventana de Venta (Telegram):**
Correcto. El canal de Telegram como escaparate ("Antes y Después") minimiza la inversión en infraestructura y mantiene el foco en la IA.

**Draft del Post de Lanzamiento (Beta Testers):**
El siguiente texto es directo, resalta el valor y establece la escasez (esencial para la conversión).

---

### POST DE LANZAMIENTO (BETA TESTER CALL)

**ASUNTO: ¡BUSCAMOS 5 MENTES VIZUALES! Beta de AIR: Agente Integral Reis (IA de Edición).**

Estoy lanzando **AIR**, mi nuevo agente de IA enfocado en la edición multimedia de alto impacto para redes (TikTok/Reels).

AIR utiliza modelos avanzados de Google (incluido 'Nano Banana' para retoque visual) y está diseñado para transformar tus productos, portadas o contenido en material **viral** en segundos, directamente desde Telegram.

**¿Qué necesitamos?** 5 beta testers dispuestos a desafiar la IA.

**¿Qué obtienes?**
Acceso prioritario y **5 ediciones de imagen de ALTA CALIDAD totalmente GRATIS**.
Solo envía la imagen y la instrucción ("Quiero que parezca más dramática y profesional"). AIR hace el resto.

**Requisitos para aplicar:**
1.  Enviar una imagen que necesites editar.
2.  Describir el objetivo de la edición (el texto que usarías en el bot).
3.  Permitirnos usar el "Antes y Después" de tu resultado en nuestro canal de showcase.

El impacto visual es lo que vende. Te muestro lo que la IA puede hacer por tu marca en 5 minutos.

Mándame un DM ahora con [TU PRODUCTO/MARCA] para asegurar tu cupo. El acceso es limitado por cuota diaria.

**[TU LINK DE TELEGRAM]**
#AIR #IA #EdicionViral #MarketingDigital #BetaTest