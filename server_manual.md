# 🦅 MANUAL DE OPERACIONES: CAZADOR REMOTO (24/7)

> [!IMPORTANT]
> **REGLA DE ORO:** TODO SE HACE EN EL SERVIDOR (`129.213.77.194`).
> La PC local NO participa en la cacería. No correr scripts localmente.

## 🔑 1. Acceso al Servidor

Para entrar al cerebro de la bestia, usar siempre este comando desde PowerShell (Windows):

```powershell
ssh -i C:\fractal-mind\ssh-key-2026-02-16.key ubuntu@129.213.77.194
```

- **IP:** `129.213.77.194`
- **Usuario:** `ubuntu`
- **Llave:** `C:\fractal-mind\ssh-key-2026-02-16.key`

---

## 👁️ 2. Auditoría y Control (Comandos Útiles)

Una vez dentro del servidor (o via SSH directo), usar estos comandos para ver qué pasa:

### Ver si los procesos están vivos

```bash
ps aux | grep python3
```

*Deberías ver dos procesos principales: `oracle_hunter_servidor.py` y `bot_telegram_cazador.py`.*

### Ver los Logs en Tiempo Real (La Verdad de la Milanesa)

Para ver qué está haciendo el cazador AHORA mismo:

```bash
tail -f cazador.log
```

*(Apretá `Ctrl+C` para salir)*

Para ver errores técnicos o crashes:

```bash
tail -n 20 out_servidor.log
tail -n 20 out_bot.log
```

---

## 🚑 3. Contingencia: ¿Qué hacer si se rompe todo?

Si el bot no responde o el cazador se detiene, ejecutar este **COMANDO DE RESURRECCIÓN** completo. Copiar y pegar en PowerShell local para reiniciar todo en el servidor de una sola vez:

```powershell
ssh -i C:\fractal-mind\ssh-key-2026-02-16.key ubuntu@129.213.77.194 "killall -u ubuntu python3 || true; sleep 2; nohup /usr/bin/python3 -u oracle_hunter_servidor.py > out_servidor.log 2>&1 & nohup /usr/bin/python3 -u bot_telegram_cazador.py > out_bot.log 2>&1 & sleep 2 && ps aux | grep python3"
```

**Este comando hace:**

1. Mata cualquier proceso Python viejo.
2. Espera 2 segundos.
3. Levanta el **Cazador** en segundo plano (persistente).
4. Levanta el **Bot** en segundo plano (persistente).
5. Te muestra la lista de procesos para confirmar que arrancaron.

---

## 📂 4. Archivos Clave en el Servidor

Todos los archivos viven en `/home/ubuntu/`:

- `.env`: Credenciales (Token, OCIDs). **(Rutas configuradas para Linux)**
- `oracle_hunter_servidor.py`: El cerebro que busca en Oracle.
- `bot_telegram_cazador.py`: El bot que te habla.
- `cazador.log`: Historial de intentos de cacería.
- `cazador_status.json`: Estado actual para el bot.

---

## ⚠️ 5. Nota sobre Persistencia

Los procesos se ejecutan con `nohup`, lo que significa que **sobreviven aunque cierres la ventana de SSH**.
**NO** ejecutar los scripts con `python3 script.py` a secas, porque se morirán al cerrar la conexión. Usar siempre el comando de resurrección de arriba.
