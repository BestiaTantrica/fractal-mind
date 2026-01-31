---
description: Sincroniza automáticamente los cambios locales y remotos sin intervención del usuario
---

// turbo-all

## PROTOCOLO DE SINCRONIZACIÓN: SERVER ↔ GIT ↔ PC

### 1. Sincronizar cambios LOCALES (PC → Git)

```powershell
git add . ; git commit -m "PC: Cambios locales" ; git push origin main
```

### 2. Sincronizar desde Git (Git → PC)

```powershell
git pull --rebase origin main
```

### 3. Sincronizar SERVER (Oracle → Git)

```powershell
ssh -i "ssh-key-2026-01-22.key" ubuntu@158.101.117.130 "cd fractal-mind && git add . && git commit -m 'SERVER: Auto-sync logs e inbox' && git push origin main"
```

### 4. Traer cambios del SERVER a PC (después del paso 3)

```powershell
git pull --rebase origin main
```

---

## FLUJO COMPLETO (Ejecutar en orden)

### Opción A: Solo actualizar PC desde Git

```powershell
git pull --rebase origin main
```

### Opción B: Sincronización total (Server + PC)

```powershell
ssh -i "ssh-key-2026-01-22.key" ubuntu@158.101.117.130 "cd fractal-mind && git add . && git commit -m 'SERVER: Auto-sync' && git push origin main"
git pull --rebase origin main
```

---

## REGLA DE ORO

- **Antes de trabajar:** Siempre ejecutar `git pull --rebase origin main`
- **Después de trabajar:** Siempre ejecutar `git add . ; git commit -m "mensaje" ; git push origin main`
- **Para ver logs del server:** Ejecutar Opción B
