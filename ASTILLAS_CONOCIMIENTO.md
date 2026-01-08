# 💎 ASTILLAS DE CONOCIMIENTO (RESUMEN CRÍTICO)

## 🛠️ INFRAESTRUCTURA (AWS/DOCKER)
- **[AWS-DISCO]:** Las instancias de 8GB se llenan rápido. 'docker system prune -a --volumes -f' y 'sudo journalctl --vacuum-size=50M' son vitales.
- **[DOCKER-CONFLICT]:** Error 'name in use' se resuelve con 'docker rm -f [nombre]'.
- **[DOCKER-VERSION]:** El aviso 'version is obsolete' en compose es trivial, ignorar o borrar la línea 'version'.

## 📈 TRADING (FREQTRADE)
- **[DRY-RUN]:** Siempre verificar '"dry_run": true' en config.json antes de arrancar.
- **[FS-RESCATE]:** El bot de AWS era el "maestro". Se rescató vía Git para evitar pérdida de lógica.
- **[INDICADORES]:** El bot está operando en 5m con Binance Futures.

## 🧠 SISTEMA (MEMORIA FRACTAL)
- **[MEMO-V3]:** El script filtrado protege a la IA de la infoxicación. Solo lee la raíz de fractal-mind.
- **[SOPORTE-TERMUX]:** No usar nano para archivos grandes en móvil. cat/sed son más seguros.
