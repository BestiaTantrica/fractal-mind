# 📚 MANUAL DE SUPERVIVENCIA GURU-ENGINE
## ⚠️ Errores de "Principiante" (Lecciones del 09-01)
1. **-bash: .venv/bin/activate: No such file:** Ocurre por no entrar a la carpeta del bot. 
   - *Solución:* Siempre empezar con `cd ~/guru-engine`.
2. **-bash: python: command not found:** Ocurre porque en AWS el comando es `python3`. 
   - *Solución:* Usar siempre `python3`.
3. **ImportError: cannot import name 'NAN':** Es el error más hdp. Es un conflicto entre la versión 3.9 y la 3.11. 
   - *Solución:* Borrar `rm -rf ~/.local/lib/python3.9` y reinstalar el venv con `python3.11 -m venv .venv`.

## 🛠️ Comandos de Mantenimiento
- **Ver logs en vivo:** `screen -r sniper_v15`
- **Salir de los logs sin apagar:** `CTRL + A` y luego `D`.
- **Matar proceso si se traba:** `pkill -f freqtrade`
