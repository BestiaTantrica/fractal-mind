import os
import subprocess

# Configuración de rutas
src = "/data/data/com.termux/files/home/fractal-mind/"
out = "/sdcard/Download/SUBIR_A_IA.md"

def obtener_ubicacion_real():
    try:
        return subprocess.check_output("pwd", shell=True).decode().strip()
    except:
        return "Desconocida"

def analizar_pulso(texto):
    tormenta = any(p in texto.lower() for p in ["mierda", "carajo", "harto", "puto", "violento", "boludo"])
    magia = any(p in texto.lower() for p in ["cangrejo", "magia", "metafora", "tarot", "astrologia"])
    
    if tormenta:
        return "PULSO: TORMENTA. Tomás necesita pragmatismo puro. Cero sermones. Soluciones directas. Empatía silenciosa."
    if magia:
        return "PULSO: MAGIA/SINCRONICIDAD. Fase creativa/existencial. Usa metáforas y profundidad."
    return "PULSO: ESTABLE. Ciber-Arquitecto operativo."

def generate():
    files = [f for f in os.listdir(src) if f.endswith('.md')]
    ubi = obtener_ubicacion_real()
    
    # 1. CAPTURA DEL PULSO
    texto_base = ""
    for f in ["STATUS.md", "PENDIENTES.md"]:
        if f in files:
            with open(os.path.join(src, f), "r") as arch:
                texto_base += arch.read()
    
    pulso = analizar_pulso(texto_base)
    
    content = f"# 📐 ARQUITECTO PROCESO\n"
    content += f"## 🔗 ENCLAVE DE SESIÓN\n> {pulso}\n"
    content += f"> UBICACIÓN ACTUAL: {ubi}\n\n"
    
    content += "## 🗺️ MAPA FIJO\n- Cerebro: ~/fractal-mind\n- Bot: ~/freqtrade-bestia\n- Servidor: AWS 30GB\n\n"

    for fname in files:
        if fname == "SUBIR_A_IA.md": continue
        with open(os.path.join(src, fname), "r") as f:
            lines = f.readlines()
            full_text = "".join(lines)
            if "::MAGIA::" in full_text:
                content += f"## 📂 {fname} (INTEGRO)\n{full_text}\n\n"
            else:
                content += f"## 📂 {fname} (EXTRACTO)\n" + "".join(lines[:20]) + "\n\n"

    with open(out, "w") as f_out:
        f_out.write(content)
    print(f"✅ Arquitecto listo. Ubicación capturada: {ubi}")

if __name__ == "__main__":
    generate()