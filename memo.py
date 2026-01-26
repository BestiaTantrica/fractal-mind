import os
from dotenv import load_dotenv
load_dotenv()
import os

src = "/data/data/com.termux/files/home/fractal-mind/"
out = "/sdcard/Download/SUBIR_A_IA.md"

def generate():
    files = [f for f in os.listdir(src) if f.endswith('.md')]
    content = "# 🤖 AGENTE FRACTAL V3 (MEMORIA CONDENSADA)\n\n"
    
    # 1. PRIORIDAD MÁXIMA (Brújula)
    for target in ["STATUS.md", "PENDIENTES.md"]:
        if target in files:
            with open(os.path.join(src, target), "r") as f:
                content += f"## ⚡ {target}\n{f.read()}\n\n"

    # 2. CONTEXTO HISTÓRICO (Astillas)
    if "ASTILLAS_CONOCIMIENTO.md" in files:
        with open(os.path.join(src, "ASTILLAS_CONOCIMIENTO.md"), "r") as f:
            content += f"## 💎 MEMORIA HISTÓRICA\n{f.read()}\n\n"

    # 3. DETALLE TÉCNICO (Solo pre-visualización para no saturar)
    content += "## 📂 BITÁCORA DE APOYO (RESUMIDA)\n"
    for fname in files:
        if fname not in ["STATUS.md", "PENDIENTES.md", "ASTILLAS_CONOCIMIENTO.md", "SUBIR_A_IA.md"]:
            with open(os.path.join(src, fname), "r") as f:
                lines = f.readlines()
                # Solo toma las primeras 15 líneas de archivos de "estudio" o "notas"
                content += f"--- 📂 [{fname}] (Extracto) ---\n"
                content += "".join(lines[:15]) + "... [Truncado para ligereza]\n"

    with open(out, "w") as f_out:
        f_out.write(content)
    print(f"✅ Memoria Fractal Condensada en: {out}")

if __name__ == "__main__":
    generate()
