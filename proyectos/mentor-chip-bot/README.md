# 🛠️ Mentor Chip Bot (C.H.I.P.)

¡Bienvenido Luca! Este es tu propio bot de inteligencia artificial diseñado para ayudarte a aprender sobre reparación de hardware (PCs, celulares) y programación.

## 🚀 Cómo empezar

1. **Configuración**: Abre el archivo `.env` y coloca tus claves:
   - `TELEGRAM_TOKEN`: El token que te da BotFather en Telegram.
   - `GEMINI_API_KEY`: Tu clave de Google Gemini (puedes usar la de tu papá por ahora).
   - `ADMIN_USER_ID`: Tu ID de Telegram (para que solo tú puedas controlarlo si quieres).

2. **Instalar dependencias**:
   Abre una terminal en esta carpeta y escribe:

   ```cmd
   pip install -r requirements.txt
   ```

3. **Ejecutar el bot**:

   ```cmd
   python main.py
   ```

## 🌐 Despliegue en Servidor (Oracle)

Si vas a dejar el bot corriendo 24/7 en el servidor:

1. Sincroniza la carpeta al server.
2. Copia el archivo `bot-mentor.service` a `/etc/systemd/system/` (necesitas sudo).
3. Habilita el servicio:

   ```bash
   sudo systemctl enable bot-mentor
   sudo systemctl start bot-mentor
   ```

## 🛠️ Modificaciones Avanzadas e Instancia 24G

- **La Personalidad**: En `bot_logic.py`, puedes cambiar lo que dice `self.system_instruction`. Si quieres que sea más gracioso, más serio, o que sepa más de Python, ¡cámbialo ahí!
- **Nuevas Funciones**: Podrías agregarle que busque precios en sitios de repuestos, o que guarde lo que vas aprendiendo en un archivo.

### 💡 Tip para conseguir la instancia ARM 24GB (A1.Flex)

Si Ashburn está lleno, no te rindas. Usa un **Python Script Automator (OCI Instance Requester)** que intente crear la instancia cada 1 minuto. A veces se liberan recursos y el script los captura antes que nadie. ¡Es tu primer reto de automatización!

## 📜 Reglas del Mentor Chip

1. El diagnóstico es gratis, las herramientas se pagan con lo que ganes reparando.
2. La seguridad es primero: ¡Cuidado con la estática!
3. Aprender a buscar en YouTube y foros es una superpotencia.

¡Diviértete modificándolo y arreglando cosas!
