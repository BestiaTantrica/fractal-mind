# 📋 ÓRDENES PERMANENTES - AGENTE PEGASO

## 🔄 SINCRONIZACIÓN AUTOMÁTICA

### Al INICIAR cualquier sesión

1. Ejecutar `/sync` para traer cambios del servidor y Git.
2. Revisar `inbox/` para ideas nuevas del celular.

### Al TERMINAR cualquier tarea que modifique archivos

1. Commit y push automático de cambios locales.
2. Si se modificó algo en el servidor, sincronizar logs a Git.

### Cuando el SERVER genera logs o archivos nuevos

1. Hacer commit/push desde el servidor.
2. Hacer pull en la PC para tener todo actualizado.

---

## 🏗️ ESTRUCTURA DEL PROYECTO

```
fractal-mind/
├── .agent/workflows/    → Protocolos de operación
├── inbox/               → Ideas del celular (sync desde móvil)
├── scripts/             → Agentes principales (agente_mente.py)
├── proyectos/           → Subproyectos (air-bot, etc.)
├── deploy/              → Servicios systemd
├── data/                → Datos persistentes
└── .env                 → Variables de entorno (NO commitear)
```

---

## 🚀 COMANDOS RÁPIDOS

| Acción | Comando |
|--------|---------|
| Sincronizar todo | `/sync` |
| Ver estado Git | `git status` |
| Ver logs server | `ssh ubuntu@158.101.117.130 "journalctl -u bot-fractal -n 50"` |

---

## ⚠️ REGLAS CRÍTICAS

1. **NUNCA** commitear archivos `.env` con tokens.
2. **SIEMPRE** sincronizar antes de empezar a trabajar.
3. **PRIORIDAD:** Si hay conflicto, la versión más reciente gana.
