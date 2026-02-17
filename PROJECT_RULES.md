# 🛑 REGLAS DE ORO - PROYECTO CAZADOR

> [!CAUTION]
> **LEER ANTES DE TOCAR CUALQUIER COSA**

## 1. ☁️ "TRABAJAMOS SOLO EN SERVER"

- **IP:** `129.213.77.194`
- **Toda ejecución debe ocurrir en la nube.**
- **JAMÁS** ejecutar `python oracle_hunter_servidor.py` en la PC local.
- La PC del usuario es sagrada/virgen. No debe tener procesos de Python cazando.

## 2. 🔄 PERSISTENCIA 24/7

- Los scripts en el servidor deben correr SIEMPRE con `nohup` o `screen`.
- Comando de resurrección: `server_manual.md`.

## 3. 🚀 DESPLIEGUE ATÓMICO

- Si se edita código local, se sube INMEDIATAMENTE con `scp`.
- No dejar versiones desincronizadas.

## 4. 📉 ESTRATEGIA 429

- Cooldown actual: **5 minutos**.
- Razón: Oracle banea IPs si martillamos la API durante un bloqueo. 5 min es el límite seguro "agresivo".
