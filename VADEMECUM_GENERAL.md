# 🧠 VADEMÉCUM GENERAL (Cerebro Guru-Engine)
**Última Actualización:** 2026-01-02 | **Estado:** Operativo Blindado

## 🛠️ REPARACIÓN RECIENTE: mi-n8n
- **Acción:** Inyección de `safeExecute` para resiliencia de red.
- **IA:** Implementación de Entropía de Shannon para modular sentimientos de noticias.
- **Estado:** Código enviado a GitHub. Pendiente de 'git pull' en producción (AWS).

## 📋 PENDIENTES GLOBALES
- [ ] Sincronizar AWS (Entrar por SSH y hacer pull).
- [ ] Verificar logs de n8n para confirmar recepción de clusters.
- [ ] Monitorear efectividad del filtro de ruido en mercado real.

## 🚨 REGLAS DE ORO ACTUALIZADAS (06/01/2026)
- **Entorno Local:** Termux es la base de desarrollo. El 'src/' de aquí manda sobre el 'dist/' de AWS.
- **Compilación:** Siempre usar 'tsc -p .' tras tocar archivos en 'src/'.
- **Estructura:** Respetar a rajatabla los archivos .md (Fractal). No crear archivos nuevos sin orden.
- **Interacción:** El asistente debe dar comandos directos, no sugerencias manuales.

## 🌳 PROTOCOLO GIT (EL PUENTE TERMUX -> AWS)
- **¿POR QUÉ?**: Porque lo que arreglamos en Termux (local) no viaja solo al servidor de AWS. Git es el transporte.
- **¿CUÁNDO?**: Siempre que terminemos un hito (ej: "ya compila") o cuando arreglemos un error en los archivos .ts o .md.
- **PASOS CLAVE**:
  1. `git status`: Para ver qué archivos tocamos (el "radar").
  2. `git add .`: Para preparar los cambios (el "paquete").
  3. `git commit -m "mensaje"`: Para ponerle nombre al avance (el "sello").
  4. `git push origin main`: Para mandar todo a la nube (el "envío").

### 🤖 PROTOCOLO DE AGENTE (06/01/2026)
- El sistema debe priorizar el registro en archivos .md para el script de condensación.
- Toda solución debe ser 'comiteada' vía Git para sincronizar Termux con AWS.
