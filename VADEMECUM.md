# 📚 MANUAL DE SUPERVIVENCIA SNIPER-V4
## 🛠️ Comandos de Mantenimiento (AWS Docker)
- **Ver logs:** docker-compose logs -f --tail 50
- **Actualizar:** git fetch origin produccion_limpia && git reset --hard origin/produccion_limpia && docker-compose down && docker-compose up -d --build
- **Acceso Web:** 56.125.187.241:8080
- [2026-01-11] TÉCNICO: Implementación de bloques 'entry_pricing' y 'exit_pricing' para validador Freqtrade 2025.12.
- [2026-01-11] ESTRUCTURA: SniperLab.py actualizado con 'can_short: True' y lógica de euforia/resistencia.
- [2026-01-11] OBSERVACIÓN: Resolución de conflictos de Python 3.13 y errores de validación de config.json (exit_pricing).
- [2026-01-11] OBSERVACIÓN: Credenciales validadas (freqtrader/SuperPassword123).
- [2026-01-11] TÉCNICO: Priorizar VolumePairlist por 'quoteVolume' para evitar activos de baja liquidez.
- [2026-01-12] REGLA DE ORO: El Agente es responsable de conocer la configuración actual antes de proponer cambios técnicos.
- [2026-01-12] ARQUITECTURA: SniperLab.py utiliza RSI y ADX con soporte/resistencia macro de 500 periodos.
- [2026-01-12] DOCTRINA: Se respetan los valores de Hyperopt para SniperLab.py. No modificar sin 100 trades de muestra.
- [2026-01-12] TÉCNICO: Diseñar script de extracción de SQL para automatizar reportes de profit neto.
- [2026-01-12] TÉCNICO: El bot de Telegram actual es el canal oficial de comunicación del Pool.
- [2026-01-12] PROTOCOLO: No se promete rentabilidad fija, sino devolución de capital + bono de testeo.
