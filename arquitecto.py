import os
import time
import shutil

src = os.path.expanduser("~/fractal-mind/")
out = "/sdcard/Download/SUBIR_A_IA.md"
TRES_DIAS = 3 * 24 * 60 * 60

def gestionar_orden():
    now = time.time()
    capas_dirs = {"1": "(1) reciente", "2": "(2) doctrina", "3": "(3) archivo", "4": "(4) pausa"}
    for d in capas_dirs.values():
        os.makedirs(os.path.join(src, d), exist_ok=True)

    for f in os.listdir(src):
        f_path = os.path.join(src, f)
        if not f.endswith('.md') or f == "SUBIR_A_IA.md": continue

        movido = False
        # Mover por prefijo (1), (2), etc.
        for c, folder in capas_dirs.items():
            if f.startswith(f"({c})"):
                shutil.move(f_path, os.path.join(src, folder, f))
                movido = True
                break
        
        # Degradación por tiempo (excepto el núcleo PROMPT_IA.md)
        if not movido and f != "PROMPT_IA.md":
            if (now - os.path.getmtime(f_path)) > TRES_DIAS:
                shutil.move(f_path, os.path.join(src, capas_dirs["1"], f))

def definir_agente(texto):
    t = texto.lower()
    if any(k in t for k in ["backtest", "rsi", "v5", "winrate"]): return "ESTRATEGA ALGORÍTMICO"
    if any(k in t for k in ["docker", "aws", "ssh", "logs"]): return "INGENIERO INFRAESTRUCTURA"
    return "AUDITOR FULL STACK"

def resumir(lineas, capa):
    if capa == "0": return "".join(lineas)
    return " | ".join([l.strip() for l in lineas if "[" in l or "Hito:" in l][:10])

def generate():
    gestionar_orden()
    files_c0 = [f for f in os.listdir(src) if f.endswith('.md')]
    contexto = ""
    for f in files_c0:
        with open(os.path.join(src, f), "r") as arch:
            contexto += arch.read()
    
    agente = definir_agente(contexto)
    content = f"# 📐 SISTEMA FRACTAL - ROL: {agente}\n\n"
    content += "## 🎯 CAPA (0) - PRESENTE Y PROTOCOLO\n"
    
    for f in sorted(files_c0):
        with open(os.path.join(src, f), "r") as arch:
            content += f"### 📂 {f}\n{arch.read()}\n\n"

    dirs = {"1": "(1) reciente", "2": "(2) doctrina", "3": "(3) archivo", "4": "(4) pausa"}
    for c, folder in sorted(dirs.items()):
        path = os.path.join(src, folder)
        if not os.path.exists(path): continue
        files = [f for f in os.listdir(path) if f.endswith('.md')]
        if not files: continue
        content += f"## 🗂️ CAPA ({c}) - {folder.upper()}\n"
        for fname in files:
            with open(os.path.join(path, fname), "r") as f:
                content += f"- **{fname}**: {resumir(f.readlines(), c)}\n"
        content += "\n"

    with open(out, "w") as f_out:
        f_out.write(content)
    print(f"✅ Reporte V20 generado como {agente}.")

if __name__ == "__main__":
    generate()
