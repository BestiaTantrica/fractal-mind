# 🚨 PROTOCOLO DE REANIMACIÓN
1. **RENDER:** Entrar a n8n y darle a "Execute Workflow" o activar el Webhook. Si da 404, es que el túnel está apagado.
2. **AWS (El Músculo):** Necesita el nuevo código para no morir. 
   - SSH a AWS
   - cd ~/mi-n8n
   - git pull
   - pm2 restart all
3. **VERIFICACIÓN:** Mirar `pm2 logs`. Si ves que llega un JSON con "clusters", el Monstruo ha despertado.

## ⚠️ HALLAZGO 2026-01-06:
- Confirmado: Webhook de Render caído (404 No Server).
- El bot en AWS está aislado. 
- PRIORIDAD 1: Reactivar servicio en el Dashboard de Render.

### ⚡ POST-COMPILACIÓN 06/01/2026
- [ ] Subir la carpeta 'src/' corregida de Termux a AWS.
- [ ] Borrar la carpeta 'dist/' en AWS y recompilar allá para eliminar los parches de 'sed'.
- [ ] Validar errores 404 de Binance Testnet con las nuevas interfaces.
