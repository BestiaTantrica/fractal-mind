---
description: Sincroniza automáticamente los cambios locales y remotos sin intervención del usuario
---

// turbo-all
1. Ejecutar commit de seguridad de cambios locales:
   ```powershell
   git add . ; git commit -m "Auto-sinc: Cambios locales detectados por Agente PEGASO"
   ```

2. Sincronizar con el repositorio remoto usando rebase para mantener la historia limpia:
   ```powershell
   git pull --rebase origin main --tags
   ```

3. Subir cambios para que estén disponibles en el móvil y otros dispositivos:
   ```powershell
   git push origin main
   ```
