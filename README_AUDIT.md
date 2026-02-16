# 🏹 AUDITORÍA SISTEMA CAZADOR ARM (PEGASO 3.1)

Este documento describe la arquitectura y operación del sistema de caza de instancias ARM de Oracle Cloud.

## 🏗️ Arquitectura

El sistema opera de forma distribuida:

1. **Torre de Caza (Micro Instance):** Una instancia `VM.Standard.E2.1.Micro` con IP `129.213.77.194` que corre 24/7 en la nube de Oracle.
2. **Agente Cazador:** Script `oracle_hunter_servidor.py` ejecutándose en una sesión `screen` en el servidor. Rotación automática de ADs y manejo de errores 429.
3. **Monitor Telegram:** Script `bot_telegram_cazador.py` que provee interfaz en tiempo real al usuario.

## 🔐 Gestión de Accesos

| Recurso | Archivo de Llave | Propósito |
| :--- | :--- | :--- |
| **Servidor Cazador** | `ssh-key-2026-02-16.key` | Acceso SSH a la micro instancia (Ubuntu). |
| **OCI API** | `oci_api_key.pem` | Autenticación para peticiones de creación de recursos. |
| **Instancia ARM (Futura)** | `ssh_for_arm` | Llave que se inyectará en la instancia ARM al ser creada. |

## 🚀 Comandos Operativos

- **Acceso al Servidor:** `ssh -i C:\fractal-mind\ssh-key-2026-02-16.key ubuntu@129.213.77.194`
- **Ver Procesos:** `screen -ls`
- **Ver Logs en Vivo:** `tail -f cazador.log`

## 📂 Archivos en este Directorio (Esenciales)

- `bot_telegram_cazador.py`: Interfaz de monitoreo.
- `oracle_hunter_servidor.py`: Lógica principal (copia local del servidor).
- `oci_api_key.pem` / `.pub`: Credenciales de API.
- `ssh_for_arm` / `.pub`: Llaves para la presa.

---
**Entorno Sincronizado - Operación Full Stack Operativo**
