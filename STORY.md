# 📂 HITOS DE RENTABILIDAD (08/01/2026)
- **Hito:** De Profit Negativo (-3.9%) a Positivo (+1.85%).
- **Evolución:** Se realizaron 6 iteraciones de Backtest.
- **Clave:** La reducción del RSI de entrada a 30 y el ajuste estricto de Stoploss a 1.5%.
- **Resultado Final:** 53 trades | WinRate 37.7% | Profit Factor 1.12.

# 📂 BITÁCORA DE RESILIENCIA (08/01/2026)
- **Hito:** Superado el error de compilación de Python.h en AWS instalando python3-devel.
- **Bloqueo:** El disco EBS de AWS (8GB) se llenó al instalar dependencias.
- **Aprendizaje:** La persistencia en Termux/Nube tiene un límite físico. La PC es la herramienta de fuerza bruta necesaria ahora.

# 📂 BITÁCORA DE RESILIENCIA (08/01/2026)
- **Hito:** Superado el error 'Account Locked' en AWS. Se aprendió que con disco al 100% el comando 'sudo' falla.
- **Aprendizaje:** No se puede compilar Freqtrade en 8GB de disco si el sistema ya ocupa 6GB. 
- **Decisión:** Reset total o ampliación a 30GB es el único camino en la nube.
- [2026-01-09] ACCIÓN: Reiniciar contenedor en AWS para refrescar mercados.
- [2026-01-10] TEST: Ejecutando forcebuy tras limpieza de Telegram Conflict.
- [2026-01-10] HITO: El bot ejecutó su primer trade automático (ADA/USDT) en modo Dry Run.
- [2026-01-10] OBJETIVO: Familiarizarse con los indicadores de la 8080 antes de pasar a Real.
- [2026-01-10] HITO: Sniper V4 alcanzó Win Rate 100% y Drawdown 0.00% en Backtest. Implementado Escudo 0.99.
- [2026-01-10] HITO: Sniper V4 listo para despliegue. Protección 0.99 validada.
- [2026-01-10] ERROR: Intento de uso de rutas Unix (~) en CMD de Windows detectado.
- [2026-01-10] NOTA: En Windows CMD usar rutas completas (C:\...) o relativas desde el perfil de usuario.
- [2026-01-10] DUDA: Confusión entre entorno de pruebas y repositorio de producción.
- [2026-01-10] RESOLUCIÓN: La carpeta 'freqtrade-bestia' en Windows es el repositorio local vinculado a la rama 'produccion_limpia'.
- [2026-01-10] HITO: Verificado repositorio remoto en GitHub: BestiaTantrica/freqtrade-bestia.git.
- [2026-01-10] STATUS: Rama activa 'produccion_limpia'. Preparando empuje de Sniper V4.
- [2026-01-10] CAMBIO: Se unificó config_test.json en config.json. Versión moderada eliminada.
- [2026-01-10] HITO: Ruptura de bloqueo .gitignore detectado; archivos core forzados con git add -f.
- [2026-01-10] TÉCNICO: Conversión CRLF a LF (Windows a Linux) completada con éxito.
- [2026-01-10] STATUS: Sniper V4 cargado en GitHub rama 'produccion_limpia' y sincronizado con AWS.
- [2026-01-10] HITO: Localización real en AWS confirmada en '~/freqtrade-bestia'.
- [2026-01-10] ACCIÓN: Despliegue de Sniper V4 mediante acceso directo sin carpeta intermedia.
- [2026-01-10] BLOQUEO: Divergencia de ramas detectada en AWS durante el pull.
- [2026-01-10] ACCIÓN: Ejecución de 'git reset --hard' para forzar la paridad con la Bóveda V4.
- [2026-01-10] HITO: Sincronización forzada (Reset Hard) exitosa en AWS.
- [2026-01-10] STATUS: Sniper V4 operando en segundo plano bajo sesión 'sniper_v4'.
- [2026-01-10] NOTA: El bot está ejecutando la estrategia con el escudo 0.99 y VolumePairList.
