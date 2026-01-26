# 📚 MANUAL DE SUPERVIVENCIA GURU-ENGINE

## 🛠️ Comandos de Infraestructura

- **Ver estado del servidor (AWS):** `ssh ubuntu@56.125.187.241`
- **Sincronización:** Git es el puente único. `git push` desde local, `git pull` en remoto.
- **Telegram:** El server se encarga de mantener vivo el sistema y reportar.

## ⚠️ Reglas de Oro (Sincronía Fractal)

1. **Simetría:** El entorno de pruebas (PC) sea Dockerizado para igualar producción (AWS).
2. **Hardware Limitado (Android):** El almacenamiento DEBE ser JSON. Se amputa validación por ejecución pesada.
3. **Persistencia:** No mezclar lógica operativa con estratégica aquí.

## ⚠️ Errores Conocidos

1. **-bash: .venv/bin/activate:**cd ~/freqtrade-bestia primero.
2. **ImportError: cannot import name 'NAN':** Conflicto Python 3.9/3.11. Borrar `.local/lib/python3.9` y usar venv 3.11.

### 💎 FICHA TÉCNICA (CEREBRO)

- **Repo Central:** `fractal-mind`
- **IP AWS:** 56.125.187.241
- **IP Oracle:** 158.101.117.130
