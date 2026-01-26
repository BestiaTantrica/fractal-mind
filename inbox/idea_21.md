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
**PROCESAMIENTO DE VÓMITO DE IDEAS - AIR-BOT**

Hemos transformado la entrada en dos documentos operativos: un 'Prompt de Ingeniería' para la construcción técnica del agente, y una 'Estrategia de Arranque' estructurada para la fase de lanzamiento.

---

## 1. PROMPT DE INGENIERÍA: AGENTE INTEGRAL (AIR-BOT)

### A. OBJETIVO Y RESTRICCIONES TÉCNICAS

**Objetivo:** Desarrollar `agente_air.py`, un bot de Telegram modular y de bajo consumo de recursos (RAM), que actúe como gestor de edición multimedia y generación de contenido mediante la API de Google Generative AI.

**Entorno:**
1.  **Plataforma:** Python 3.x.
2.  **SDKs:** `python-telegram-bot` (o `telebot`) y `google-generativeai`.
3.  **Restricción Crítica (AWS 1GB RAM):** El procesamiento de archivos debe priorizar el uso de `io.BytesIO` o flujos directos hacia la API para evitar la escritura y carga de archivos pesados en el disco duro del servidor. **Optimización de RAM prioritaria.**

### B. ARQUITECTURA DE PERSISTENCIA Y REGISTRO

Se requiere un sistema de persistencia simple y eficiente utilizando el repositorio `BestiaTantrica/fractal-mind`.

| Elemento | Propósito | Formato | Ubicación |
| :--- | :--- | :--- | :--- |
| **Cuota Diaria** | Contador global de imágenes procesadas. Máximo 100/día. | JSON (Recomendado) | `air_config/cuotas_air.json` |
| **Logs de Interacción** | Registro histórico detallado por usuario. | Markdown (.md) | `fractal-mind/proyectos/redes/clientes/[user_id].md` |

**Formato del Log de Interacción (.md):**
```markdown
# Cliente: [Nombre de Usuario - @alias]
## Fecha: [AAAA-MM-DD HH:MM:SS]
### Pedido Original:
[Texto completo del pedido del cliente]
### Resultado:
- Modelo utilizado: [Nano Banana / Gemini 3 Pro]
- Tipo de Salida: [Imagen Editada / Script de Contenido]
- Link al Resultado: [URL de la imagen alojada o referencia al contenido generado]
---
```

### C. LÓGICA DEL AGENTE (STATE MACHINE)

El flujo de ejecución debe basarse en la detección del tipo de mensaje y sus adjuntos.

| Condición de Entrada | Modelo a Utilizar | Acción (Función) | Output y Persistencia |
| :--- | :--- | :--- | :--- |
| **`/start`** | N/A | Bienvenida, instrucciones y estado de cuota gratuita (5 ediciones). | Envío de mensaje de bienvenida. |
| **Imagen + Texto (Caption)** | Google Generative AI (Nano Banana - Edición) | `handle_media_edit(img_bytes, prompt)` | 1. Deducción de -1 a la Cuota Diaria (si aplica). 2. Aplicar edición según el `prompt`. 3. Respuesta al usuario con la imagen editada. 4. Log en `.md`. |
| **Solo Texto** | Google Generative AI (Gemini 3 Pro) | `handle_content_generation(text_prompt)` | 1. Generar 3 Guiones de TikTok/Reels. 2. Generar 1 Sugerencia de Prompt de Imagen (Portada). 3. Respuesta al usuario con el texto estructurado. 4. Log en `.md`. |
| **Solo Imagen** | N/A | Rechazo o Solicitud de Prompt. | Mensaje de error: "Adjunta el texto con el cambio deseado." |
| **Exceso de Cuota** | N/A | Bloqueo o activación de `future_payment_module`. | Mensaje de "Límite Diario Alcanzado." |

### D. REQUERIMIENTOS DE CÓDIGO

1.  **Modularidad:** La gestión de la lógica de negocio (cuotas, edición, generación) debe estar separada del `main.py` (Telegram Handler). Se requiere un módulo dedicado, por ejemplo, `air_core.py`, y un módulo `persistence_handler.py`.
2.  **Manejo de Errores:** Implementar manejo de excepciones para la API de Google (errores de tasa, errores de contenido).
3.  **Garantía de Optimización:** Utilizar el método de la librería de Telegram para obtener el archivo en memoria (`file.download_as_bytearray()` o similar), garantizando que el `image_data` que se envía a la API de Google sea un objeto en memoria (e.g., `BytesIO`).

---

## 2. ESTRATEGIA DE ARRANQUE (PLAN DE ATAQUE INICIAL)

### A. DEFINICIÓN DE MARCA Y VENTAJA CLAVE

| Componente | Decisión | Definición |
| :--- | :--- | :--- |
| **Nombre** | **AIR: Agente Integral Reis** | Enfoque técnico y profesional. "AIR" sugiere ligereza y velocidad. |
| **Gancho Comercial (TOFU)** | 5 Ediciones Gratis | La prueba social y el impacto visual son la clave. Actúa como un *lead magnet* de alto valor (High-Impact Lead Magnet). |
| **Canal de Venta** | Telegram Portfolio (Vidriera) | Publicación constante de "Antes y Después" para demostrar la capacidad del Nano Banana. Enfoque 100% visual. |

### B. PROMPT DE LANZAMIENTO (BETA TESTERS)

**Objetivo:** Redactar un mensaje de lanzamiento de alto impacto y escasez para atraer 5 beta testers cualificados que proporcionarán los primeros casos de estudio (logística: Telegram, Tono: Directo y Exclusivo).

**PROMPT PARA COPYWRITER/GEMINI 3 PRO:**

> **Instrucción:** Eres un redactor enfocado en la conversión B2B/Creativo. Genera un post para Telegram/Redes sociales que anuncie la búsqueda de 5 "Beta Testers" para AIR-Bot. El objetivo es obtener contenido de alto impacto para la vidriera del canal.
>
> **Tono:** Urgente, exclusivo, técnico y enfocado en la solución de problemas de producción de contenido (TikTok, Reels).
>
> **Estructura Requerida:**
> 1.  Título Impactante (Problema/Solución).
> 2.  Definición de AIR-Bot (Qué es).
> 3.  La Oferta Exclusiva (El gancho de 5 ediciones).
> 4.  Requisito (Qué se espera del tester).
> 5.  Call To Action (CTA).

*(Nota: Este prompt generará el material necesario para iniciar la fase de captación sin perder tiempo en la redacción manual.)*