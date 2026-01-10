# 📚 MANUAL DE SUPERVIVENCIA GURU-ENGINE
## ⚠️ Errores de "Principiante" (Lecciones del 09-01)
1. **-bash: .venv/bin/activate: No such file:** Ocurre por no entrar a la carpeta del bot. 
   - *Solución:* Siempre empezar con `cd ~/reqtrade-bestia`.
2. **-bash: python: command not found:** Ocurre porque en AWS el comando es `python3`. 
   - *Solución:* Usar siempre `python3`.
3. **ImportError: cannot import name 'NAN':** Es el error más hdp. Es un conflicto entre la versión 3.9 y la 3.11. 
   - *Solución:* Borrar `rm -rf ~/.local/lib/python3.9` y reinstalar el venv con `python3.11 -m venv .venv`.

## 🛠️ Comandos de Mantenimiento
- **Ver logs en vivo:** `docker-compose logs -f`
- **Salir de los logs sin apagar:** `CTRL + A` y luego `D`.
- **Matar proceso si se traba:** `pkill -f freqtrade`

## 🚩 BITÁCORA DE UN DESASTRE TÉCNICO (09-01) - INFORME COMPLETO
### CONTEXTO: Intento fallido de despliegue v15 Sniper.

#### 1. CRONOLOGÍA DE ERRORES DEL AGENTE:
- **Incompatibilidad de Base:** Se forzó motor v2026 en Python 3.9 (AWS). Error de diseño inicial.
- **Confusión de Intérpretes:** El Agente no reseteó PM2 (pm2 kill), causando que Node.js intentara ejecutar Python.
- **Cascada de Dependencias:** Se intentó 'pip install' manual de: cachetools, arrow, pandas-ta. Todos fallaron por estar fuera de la arquitectura Git.
- **Corrupción de Repositorio:** El proceso de 'downgrade' borró la carpeta /freqtrade/ en Git, dejando el sistema inoperativo.

#### 2. ESTADO DE DEUDA TÉCNICA:
- El repositorio 'freqtrade-bestia' en GitHub está DESINCRONIZADO y le faltan archivos del núcleo.
- La AWS tiene un .venv contaminado y procesos PM2 fantasmas.

#### 3. ACCIÓN REQUERIDA (OBLIGATORIO):
- Borrar carpeta 'freqtrade-bestia' en AWS: 'rm -rf freqtrade-bestia'.
- Limpiar PM2: 'pm2 kill && rm -rf ~/.pm2'.
- Reconstruir en Termux usando la versión 2022.9 pura ANTES de volver a tocar la nube.

## 🔄 FLUJO DE TRABAJO DEFINITIVO (CELULAR -> NUBE)
**Pregunta:** ¿Cómo configuro el bot si está en Docker?
**Respuesta:**
1. **Termux:** Editás archivos en `~/freqtrade-bestia`.
2. **Termux:** `git add . && git commit -m "ajuste" && git push`.
3. **AWS (SSH):** Entrás al servidor.
   - `cd freqtrade-bestia`
   - `git pull`
   - `docker compose restart`
   
**Nota:** Docker lee los archivos actualizados al reiniciar. No hace falta "reinstalar" nada.

## ⚠️ PROHIBICIONES (NUEVAS REGLAS DE MEMORIA)
1. **PROHIBIDO** editar código en caliente en AWS con `nano`. Solo se edita en local/Termux y se sube.
2. **PROHIBIDO** cantar victoria si el bot corre en "localhost". Solo vale si corre en IP 56.x.x.x (AWS).
3. **PROHIBIDO** iniciar instalaciones sin verificar si existe una imagen Docker oficial.

## 🚀 DESPLIEGUE AWS DOCKER (2026-01-09)
- **Estructura:** El bot exige la carpeta 'user_data/' para ver config.json y estrategias.
- **Comando Reset:** docker-compose down && docker-compose up -d
- **Error KeyError 'exit_pricing':** Falta configuración de precios en el JSON.
- **Error Telegram Conflict:** Matar procesos viejos con 'sudo docker rm -f $(sudo docker ps -aq)'.

### 💎 FICHA TÉCNICA AWS (09-01-2026)
- **Acceso WebUI:** http://56.125.187.241:8080
- **Credenciales:** freqtrader / supersecretpassword
- **Estructura Crítica:** Los archivos deben vivir en 'user_data/'. Si no, Docker no los ve.
- **Comando de Oro:** 'docker-compose up -d' es el que arranca la Bestia.
- **Gestión de Errores:** Si hay conflicto de Telegram, 'sudo docker rm -f $(sudo docker ps -aq)'.
- [2026-01-10] ESTRUCTURA: Confirmado que config.json reside en user_data/.
