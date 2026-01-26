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
**PROCESAMIENTO DE VÓMITOS - PROYECTO AIR-BOT**

---

## 1. TRANSFORMACIÓN A PROMPT DE INGENIERÍA

**Mandato:** Desarrollar el agente principal (`agente_air.py`) en Python para la gestión de edición multimedia asistida por IA vía Telegram.

### A. CONTEXTO Y RESTRICCIONES OPERACIONALES

| Parámetro | Valor | Restricción Clave |
| :--- | :--- | :--- |
| **Nombre del Proyecto** | AIR: Agente Integral (Bot de Edición) | |
| **Plataforma Objetivo** | Telegram (Python SDK) | |
| **Infraestructura** | AWS Instance (1GB RAM) | **Prioridad:** Mínimo consumo de memoria y CPU. |
| **API Principal** | Google Generative AI (Gemini 3 Pro, Nano Banana) | |
| **Persistencia** | Repositorio `BestiaTantrica/fractal-mind` (Markdown) | |
| **Optimización RAM** | Uso obligatorio de `BytesIO` para manejo de archivos. Prohibido el almacenamiento temporal en disco para inputs/outputs de imagen. |

### B. ESPECIFICACIONES DE LÓGICA CORE (LCP)

El bot debe implementar una función de *handler* principal (`message_processor`) que discrimine la entrada:

1.  **LÓGICA DE EDICIÓN (Input: Imagen + Texto):**
    *   **Función:** `handle_image_edit(update, context)`
    *   **Acción:** Extraer la imagen binaria del mensaje, cargarla en `BytesIO`. Tomar el texto adjunto como instrucción de edición.
    *   **API:** Enviar `BytesIO` + Instrucción a Google Generative AI (Modelo Nano Banana).
    *   **Validación:** Verificar cuota (`quota_check`). Si es excedida, retornar un mensaje de error y detener el procesamiento.

2.  **LÓGICA DE CREACIÓN DE CONTENIDO (Input: Solo Texto):**
    *   **Función:** `handle_script_generation(update, context)`
    *   **Acción:** Usar el texto como tema central.
    *   **API:** Enviar a Gemini 3 Pro (o equivalente).
    *   **Output:** Generar un mensaje estructurado que contenga:
        *   3 opciones de guion técnico optimizado para TikTok/Reels (máx. 60 segundos c/u).
        *   1 sugerencia de *prompt* técnico (en inglés) para la generación de la imagen de portada/miniatura.

### C. GESTIÓN DE RECURSOS Y LOGGING

1.  **CONTADOR DE CUOTAS PERSISTENTE:**
    *   **Mecanismo:** Implementar una clase `QuotaManager` que gestione un contador diario de imágenes procesadas.
    *   **Almacenamiento:** Archivo JSON (`quota_status.json`) o un archivo Markdown dedicado para persistencia.
    *   **Límite Diario:** 100 imágenes. El contador debe resetearse a las 00:00 UTC.

2.  **INTEGRACIÓN FRACTAL-MIND (Logging Técnico):**
    *   Toda interacción exitosa debe generar un archivo de log.
    *   **Ruta:** `fractal-mind/proyectos/redes/clientes/[ID_Telegram_Usuario].md`
    *   **Formato de Registro (Append):**
        ```markdown
        ### Interacción [UUID]
        - Fecha/Hora: [YYYY-MM-DD HH:MM:SS]
        - Tipo: [EDICIÓN/GUION]
        - Pedido Original: "[Texto de la solicitud]"
        - Estado de Cuota: [X/100]
        - Link de Resultado: [URL del archivo generado/Respuesta completa del script]
        ```

### D. ESTRUCTURA DE CÓDIGO

*   El código debe ser modular.
*   **Módulos Clave:** `quota_manager.py`, `ai_interface.py` (conexión Gemini/Nano), `telegram_handlers.py`.
*   Reservar un *hook* o clase separada (`payment_module.py`) para futuras integraciones de cobro/suscripción.

---

## 2. ESTRATEGIA DE ARRANQUE TÉCNICO Y COMERCIAL

### A. BRANDING Y OBJETIVO

*   **Nombre Seleccionado:** **AIR: Agente Integral (AI-Ready)**.
*   **Propuesta de Valor (MVP):** Validación técnica del flujo de datos (Telegram -> BytesIO -> Google AI -> Logging MD).
*   **Fase 1 (MVP):** Priorizar el desarrollo de la Lógica de Edición y el Quota Manager. La Lógica de Contenido puede seguir inmediatamente después.

### B. PLAN DE ATAQUE (OPERACIONAL)

| Prioridad | Tarea | Requisito Técnico |
| :--- | :--- | :--- |
| **P1** | Configuración AWS y Entorno Python | Instalar dependencias esenciales (evitar bloat). Configurar variables de entorno (Telegram Token, Google API Key). |
| **P2** | Desarrollo del `QuotaManager` | Debe ser robusto y atómico para evitar inconsistencias en el contador. |
| **P3** | Desarrollo de `ai_interface` | Enfocarse en la gestión de `BytesIO`. Asegurar que la llamada a Nano Banana no requiere almacenamiento temporal. |
| **P4** | Implementación de `handle_image_edit` | Pruebas de bajo consumo de RAM. Validación del *workflow* completo de logueo en Fractal-Mind. |
| **P5** | Estrategia de Crecimiento | Implementación del plan de adquisición de Beta Testers. |

### C. GANCHO DE LANZAMIENTO (DRAFT)

**Objetivo:** Captar 5 *beta testers* para validar la infraestructura y el flujo de trabajo (P4).

**Canal:** Telegram / Grupos de Contenido.

> **ASUNTO: BETA INVITACIÓN - AIR: AGENTE INTEGRAL.**
>
> **MANDATO TÉCNICO:** Necesitamos 5 perfiles para estresar nuestra nueva infraestructura de IA de edición. AIR utiliza el motor Nano Banana (Google AI Plus) para optimizar visualmente contenido de redes.
>
> **TU BENEFICIO:** Acceso gratuito a **5 ediciones PRO** (imagen + instrucción de texto) para tu contenido. Evaluaremos el rendimiento, la latencia de respuesta y la precisión del modelo en la edición de color, detalle y composición.
>
> **REQUISITO:** Envía una imagen y la instrucción de edición. Si el resultado te sirve, compartiremos el caso de estudio (anónimo) en nuestros logs.
>
> **ACCIÓN:** El bot estará online en [@AIR_BestiaViral_Bot]. Los primeros 5 contactos que envíen `INICIAR BETA` serán agregados al *whitelist*.
>
> *Advertencia: Estamos monitoreando el consumo de recursos (1GB RAM). El tiempo de respuesta puede variar durante la fase inicial.*