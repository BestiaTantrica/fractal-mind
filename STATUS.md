# ⚡ STATUS.md
# 🎯 HITO: VALIDACIÓN LOCAL COMPLETADA -> OBJETIVO AWS (09/01/2026)
- **Realidad Actual:** Bot operativo en PC (Windows/Docker). Dependiente de WiFi hogareño (NO VIABLE para producción).
- **Objetivo Inmediato:** Replicar la arquitectura Docker en AWS para lograr autonomía 24/7.
- **Estrategia:** `GuruStrategy` (Multipares/Futuros) lista en el repo `freqtrade-bestia`.
- **Infraestructura:**
  - Desarrollo: PC Local.
  - Producción: AWS (Pendiente migrar a Docker).

# ⚡ PENDIENTES.md
# 🧭 BRÚJULA DE ACCIÓN
- [ ] AWS: Instalar Docker en el servidor (Amazon Linux 2023).
- [ ] AWS: Clonar `freqtrade-bestia` limpio (borrar basura vieja).
- [ ] AWS: Transferir `config.json` con claves reales (scp o nano seguro).
- [ ] MEMORIA: Refactorizar el sistema para que lance "Warnings" antes de ejecutar, no post-mortem.
