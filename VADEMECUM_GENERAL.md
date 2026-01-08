# 🧠 VADEMÉCUM: SOBERANÍA DIGITAL (07/01/2026)

## 🏗️ ARQUITECTURA DE TRABAJO
1. **~/fractal-mind**: Centro de Inteligencia (Notas y Scripts de IA).
2. **~/guru-engine**: Código del Orquestador (TypeScript).
3. **~/freqtrade-bestia**: Bot de Trading (Estrategia y Config).

## 🚨 REGLAS DE ORO ACTUALIZADAS
- **Rescate Local:** El bot rescatado de AWS ahora vive en Git (BestiaTantrica/freqtrade-bestia).
- **Flujo de Verdad:** Termux -> GitHub -> AWS. Nunca al revés.
- **Asertividad:** El script 'memo' solo debe leer archivos de la carpeta fractal-mind.

## 🚨 LECCIONES DE INFRAESTRUCTURA (08/01/2026)
- **AWS Free:** Si falla la instalación con 'Python.h', ejecutar: sudo yum install python3-devel.
- **Espacio en Disco:** Si sale 'Errno 28', limpiar con: rm -rf ~/.cache/pip y sudo rm -rf /tmp/*.
- **Arquitectura:** No compilar Freqtrade en Termux (usar tur-repo o simplemente usarlo como editor).

## 🚨 PROTOCOLO DE CRISIS (DISCO LLENO)
1. **Comando de Diagnóstico:** sudo du -sh /* 2>/dev/null | sort -h
2. **Limpieza de Emergencia:**
   - sudo journalctl --vacuum-time=1s
   - sudo yum clean all
   - sudo swapoff /swapfile && sudo rm -f /swapfile
3. **Regla de Oro:** Si el disco llega al 95%, mover operaciones de compilación a la PC.
