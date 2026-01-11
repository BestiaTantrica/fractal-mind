# 📚 MANUAL DE SUPERVIVENCIA SNIPER-V4
## 🛠️ Comandos de Mantenimiento (AWS Docker)
- **Ver logs:** docker-compose logs -f --tail 50
- **Actualizar:** git fetch origin produccion_limpia && git reset --hard origin/produccion_limpia && docker-compose down && docker-compose up -d --build
- **Acceso Web:** 56.125.187.241:8080
- [2026-01-11] TÉCNICO: Implementación de bloques 'entry_pricing' y 'exit_pricing' para validador Freqtrade 2025.12.
- [2026-01-11] ESTRUCTURA: SniperLab.py actualizado con 'can_short: True' y lógica de euforia/resistencia.
- [2026-01-11] OBSERVACIÓN: Resolución de conflictos de Python 3.13 y errores de validación de config.json (exit_pricing).
