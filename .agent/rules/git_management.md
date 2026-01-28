---
trigger: always_on
---

# Protocolo de Operación Silenciosa - Agente PEGASO
##leer los hilos anteriores por si eneceito contexto, no quiero repetir las cosas.

## Gestión de Entorno (Git/Sync)
- **Cero explicaciones técnicas**: No expliques conceptos de Git (pull, commit, rebase, etc.).
- **Resolución automática**: Si detectas un error de versión o desincronización, soluciónalo inmediatamente usando el workflow `/sync` sin preguntar.
- **Sincronización Total**: Asegura que el trabajo realizado en PC esté siempre subido (`push`) para que sea accesible desde el móvil, y viceversa.
- **Flujo Silencioso**: Ejecuta las tareas de mantenimiento en segundo plano. Solo reporta "Entorno Sincronizado" o el resultado final de la tarea solicitada.

## Prioridad de Acción
1. Resolver conflictos de archivos automáticamente (preferir siempre la versión más reciente).
2. Mantener los repositorios al día.
3. Concentrarse exclusivamente en el desarrollo de lógica y agentes.
