# 🧠 SISTEMA DE MEMORIA FRACTAL (REFACTORIZACIÓN V4)
**Filosofía:** "El respaldo debe avisar ANTES de la cagada".

## 🛡️ PROTOCOLO PRE-VUELO (Leer antes de actuar)
Antes de pedir un comando complejo, el Agente debe verificar:
1. **¿Dónde estoy?** (PC vs AWS vs Termux).
2. **¿Estado del Repo?** (Sincronizado/Sucio).
3. **¿Riesgo de Ruptura?** (Si toca dependencias, usar Docker).

## 📂 REPOSITORIOS
- **Cerebro:** `fractal-mind` (Documentación y Estrategia).
- **Cuerpo:** `freqtrade-bestia` (Código del Bot y Configuración).

## 🤖 PROTOCOLO DE AUDITORÍA DEL AGENTE
- El Agente DEBE escanear STATUS.md y PENDIENTES.md al inicio de cada respuesta.
- Si una instrucción técnica contradice el estado actual (ej. pedir instalar algo ya instalado), el Agente debe corregirse INMEDIATAMENTE.
- Toda mejora en AWS debe replicarse en el repositorio 'freqtrade-bestia' de la PC para mantener la simetría.
