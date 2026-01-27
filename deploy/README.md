# Guía de Despliegue - Fractal Mind Bots

Este directorio contiene los archivos de configuración y scripts necesarios para "blindar" tus bots y asegurar que corran 24/7 en tu servidor AWS.

## Contenido

- `bot-fractal.service`: Configuración systemd para Agente Mente.
- `bot-air.service`: Configuración systemd para Agente AIR.
- `install_services.sh`: Script automático para instalar y arrancar todo.

## Instrucciones de Instalación (En tu servidor AWS)

1.  **Sube los cambios al servidor**:
    Si usas git en el servidor:
    ```bash
    cd ~/fractal-mind
    git pull
    ```
    O copia la carpeta `deploy` a `~/fractal-mind/deploy`.

2.  **Ejecuta el script de instalación**:
    ```bash
    cd ~/fractal-mind/deploy
    chmod +x install_services.sh
    ./install_services.sh
    ```

3.  **Verificación**:
    El script te mostrará el estado de los bots. Deberían decir "Active: active (running)".

## Comandos Útiles

- Ver logs de Fractal Mind: `journalctl -u bot-fractal -f`
- Ver logs de AIR Bot: `journalctl -u bot-air -f`
- Reiniciar bots: `sudo systemctl restart bot-fractal bot-air`
- Parar bots: `sudo systemctl stop bot-fractal bot-air`
