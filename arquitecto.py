import os
import time
import shutil

src = os.path.expanduser("~/fractal-mind/")
out = "/sdcard/Download/SUBIR_A_IA.md"

# CONFIGURACIÓN DE TIEMPOS (en segundos)
TRES_DIAS = 3 * 24 * 60 * 60
SIETE_DIAS = 7 * 24 * 60 * 60

def gestionar_ciclo_vida():
    now = time.time()
    capas_dirs = {
        "1": os.path.join(src, "(1) reciente"),
        "2": os.path.join(src, "(2) doctrina"),
        "3": os.path.join(src, "(3) archivo"),
        "4": os.path.join(src, "(4) pausa")
    }
    for d in capas_dirs.values(): os.makedirs(d, exist_ok=True)

    # DEGRADACIÓN AUTOMÁTICA
    for f in os.listdir(src):
        f_path = os.path.join(src, f)
        if f.endswith('.md') and f not in ["PENDIENTES.md", "STATUS.md", "PROMPT_IA.md"]:
            # De Raíz a (1) reciente tras 3 días de inactividad
            if (now - os.path.getmtime(f_path)) > TRES_DIAS:
                shutil.move(f_path, os.path.join(capas_dirs["1"], f))
                print(f"📉 Moviendo a Reciente: {f}")

def definir_agente(texto):
    t = texto.lower()
    if any(k in t for k in ["backtest", "rsi", "profit", "v5"]): return "ESTRATEGA ALGORÍTMICO"
    if any(k in t for k in ["docker", "aws", "ssh"]): return "INGENIERO INFRAESTRUCTURA"
    return "AGENTE FULL STACK"

def resumir(lineas, capa):
    if capa == "0": return "".join(lineas)
    if capa == "1": return "".join(lineas[:max(1, len(lineas) // 2)])
    if capa == "2": return " | ".join([l.strip() for l in lineas if any(k in l.lower() for k in ["regla", "config", "v5"])])
    return " | ".join([l.strip() for l in lineas if "[" in l][:5])

def generate():
    gestionar_ciclo_vida()
    files = [f for f in os.listdir(src) if f.endswith('.md')]
    
    # Captura contexto para definir Agente
    contexto_c0 = ""
    for f in files:
        with open(os.path.join(src, f), "r") as arch: contexto_c0 += arch.read()
    
    agente = definir_agente(contexto_c0)
    content = f"# 📐 SISTEMA FRACTAL - ROL: {agente}\n\n"
    content += "## 🛠️ COMANDOS: git pull origin main | memo\n\n"

    # Procesar Capa 0
    content += "## 🎯 CAPA (0) - PRESENTE\n"
    for f in sorted(files):
        with open(os.path.join(src, f), "r") as arch:
            content += f"### 📂 {f}\n{arch.read()}\n\n"

    # Procesar Historial
    for c in ["1", "2", "3", "4"]:
        path = os.path.join(src, ["", "(1) reciente", "(2) doctrina", "(3) archivo", "(4) pausa"][int(c)])
        if not os.path.exists(path): continue
        for fname in os.listdir(path):
            with open(os.path.join(path, fname), "r") as f:
                content += f"#### 📂 {fname} (Capa {c})\n{resumir(f.readlines(), c)}\n\n"

    with open(out, "w") as f_out: f_out.write(content)
    print(f"✅ Ejecutado como {agente}. Archivo listo en Downloads.")

if __name__ == "__main__":
    generate()
