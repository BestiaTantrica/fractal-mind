# 📚 MANUAL DE SUPERVIVENCIA GURU-ENGINE

## ⚠️ Errores de "Principiante" (Lecciones del 09-01)

1. **-bash: .venv/bin/activate: No such file:** Ocurre por no entrar a la carpeta del bot.
   - *Solución:* Siempre empezar con `cd ~/reqtrade-bestia`.
2. **-bash: python: command not found:** Ocurre porque en AWS el comando es `python3`.
   - *Solución:* Usar siempre `python3`.
3. **ImportError: cannot import name 'NAN':** Es el error más hdp. Es un conflicto entre la versión 3.9 y la 3.11.
   - *Solución:* Borrar `rm -rf ~/.local/lib/python3.9` y reinstalar el venv con `python3.11 -m venv .venv`.

## 🛠️ Comandos de Infraestructura

- **Ver estado del servidor (AWS):** `ssh ubuntu@56.125.187.241`
- **Sincronización:** Git es el puente único. `git push` desde local, `git pull` en remoto.

## 🔄 FLUJO DE TRABAJO (LAB -> ORÁCULO)

1. **Ideación:** Tomás vuelca ideas en `PENDIENTES.md` o por voz.
2. **Refinamiento:** Se genera contexto con `arquitecto.py`.
3. **Despliegue:** La estrategia refinada se sube al Cerebro.

## ⚠️ REGLAS FILOSÓFICAS

1. **PROHIBIDO** mezclar lógica operativa con estratégica aquí.
2. **PRIORIDAD:** Claridad absoluta en los prompts para que la IA no alucine.

### 💎 FICHA TÉCNICA (CEREBRO)

- **Repo Central:** `fractal-mind`
- **Nube AWS:** 56.125.187.241 (IP de consulta para logs estratégicos)
- **Nube Oracle:** 158.101.117.130 (Procesamiento de IA)
