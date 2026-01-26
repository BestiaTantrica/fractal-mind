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

## 🧪 HIPÓTESIS DE VALIDACIÓN (Semana 19/01/2026)
- **Capital Real:** 300-400 USD (Preservación Absoluta).
- **Prueba 1 (Stake Dinámico):** Validar si el bot ajusta % de entrada correctamente ante rachas negativas.
- **Prueba 2 (Filtro de Volumen):** Ajuste Proporcional: El tamaño de la entrada debe escalar según el volumen del par (Stake vs Liquidez).
- **Prueba 3 (Estrés 1 Año):** Backtest total en PC para detectar "Drawdown de Ruina".
