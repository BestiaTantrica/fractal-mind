import os
import subprocess
import sys
import time
import shutil

# --- CONFIGURACIÓN DINÁMICA ---
IS_TERMUX = os.path.exists("/data/data/com.termux")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Si estamos en PC, usamos la ruta actual, si estamos en Termux expandimos
SRC_DIR = BASE_DIR if not IS_TERMUX else os.path.expanduser("~/fractal-mind/")

if IS_TERMUX:
    OUT_FILE = "/sdcard/Download/SUBIR_A_IA.md"
else:
    OUT_FILE = os.path.join(BASE_DIR, "SUBIR_A_IA.md")

TRES_DIAS = 3 * 24 * 60 * 60


def obtener_contexto_entorno():
    return "TERMUX (Móvil)" if IS_TERMUX else f"PC ({sys.platform})"


def gestionar_orden():
    now = time.time()
    capas_dirs = {
        "1": "(1) reciente",
        "2": "(2) doctrina",
        "3": "(3) archivo",
        "4": "(4) pausa",
    }
    for d in capas_dirs.values():
        os.makedirs(os.path.join(SRC_DIR, d), exist_ok=True)

    for f in os.listdir(SRC_DIR):
        f_path = os.path.join(SRC_DIR, f)
        if not f.endswith(".md") or f == "SUBIR_A_IA.md":
            continue

        movido = False
        # Mover por prefijo (1), (2), etc.
        for c, folder in capas_dirs.items():
            if f.startswith(f"({c})"):
                target = os.path.join(SRC_DIR, folder, f)
                if f_path != target:
                    shutil.move(f_path, target)
                movido = True
                break

        # Degradación por tiempo (excepto núcleos)
        nucleos = ["PROMPT_IA.md", "STATUS.md", "PENDIENTES.md", "VADEMECUM.md"]
        if not movido and f not in nucleos:
            if (now - os.path.getmtime(f_path)) > TRES_DIAS:
                shutil.move(f_path, os.path.join(SRC_DIR, capas_dirs["1"], f))


def analizar_pulso(files_content):
    # Detección de estados mentales y operativos
    tormenta = any(
        p in files_content.lower()
        for p in [
            "mierda",
            "carajo",
            "harto",
            "puto",
            "violento",
            "cojones",
            "caos",
            "error",
            "falla",
        ]
    )
    magia = any(
        p in files_content.lower()
        for p in ["cangrejo", "magia", "metafora", "tarot", "fluir", "intuicion"]
    )
    orden = any(
        p in files_content.lower()
        for p in [
            "limpieza",
            "estructura",
            "centralizado",
            "saneamiento",
            "consolidacion",
        ]
    )
    estrategia = any(
        p in files_content.lower()
        for p in [
            "backtest",
            "hyperopt",
            "sharpe",
            "profit",
            "trade",
            "mercado",
            "bot",
            "ganancia",
        ]
    )
    aprendizaje = any(
        p in files_content.lower()
        for p in ["investigar", "aprender", "leer", "estudiar", "tutorial", "docs"]
    )

    if tormenta:
        return (
            "🔥 PULSO: TORMENTA. Foco en resolución de errores inmediatos.",
            "CONCIENCIA: FRAGMENTADA (Modo Supervivencia)",
        )
    if magia:
        return (
            "✨ PULSO: CREATIVO. Foco en evolución y metáforas estratégicas.",
            "CONCIENCIA: EXPANDIDA (Modo Oráculo)",
        )
    if orden:
        return (
            "📐 PULSO: ESTRUCTURAL. Foco en orden y simetría del sistema.",
            "CONCIENCIA: INTEGRAL (Modo Arquitecto)",
        )
    if estrategia:
        return (
            "⚔️ PULSO: GUERRERO. Foco en optimización y rentabilidad.",
            "CONCIENCIA: ENFOCADA (Modo Bestia)",
        )
    if aprendizaje:
        return (
            "🧠 PULSO: COGNITIVO. Foco en absorción de nuevo conocimiento.",
            "CONCIENCIA: RECEPTIVA (Modo Aprendiz)",
        )

    return (
        "✅ PULSO: ESTABLE. Ciber-Arquitecto en guardia.",
        "CONCIENCIA: VIGILANTE (Modo Centinela)",
    )


def definir_agente(texto):
    t = texto.lower()
    if any(k in t for k in ["backtest", "rsi", "v5", "winrate"]):
        return "ESTRATEGA ALGORÍTMICO"
    if any(k in t for k in ["docker", "aws", "ssh", "logs", "telegram"]):
        return "INGENIERO INFRAESTRUCTURA"
    return "AUDITOR FULL STACK"


def resumir(lineas, capa):
    if capa == "0":
        return "".join(lineas[:10])  # Limitar para el resumen de capas
    return " | ".join(
        [linea.strip() for linea in lineas if "[" in linea or "Hito:" in linea][:10]
    )


def generate():
    gestionar_orden()

    # 1. CAPTURA DEL ESTADO ACTUAL (Capa 0)
    files_c0 = [
        f for f in os.listdir(SRC_DIR) if f.endswith(".md") and f != "SUBIR_A_IA.md"
    ]
    full_text = ""
    for f in ["STATUS.md", "PENDIENTES.md", "STORY.md"]:
        if f in files_c0:
            with open(os.path.join(SRC_DIR, f), "r", encoding="utf-8") as arch:
                full_text += arch.read()

    pulso, conciencia = analizar_pulso(full_text)
    entorno = obtener_contexto_entorno()
    agente = definir_agente(full_text)

    content = f"# 📐 SISTEMA FRACTAL - ROL: {agente}\n"
    content += f"## 🔗 ENCLAVE DE SESIÓN\n> {pulso}\n"
    content += f"> {conciencia}\n"
    content += f"> ENTORNO: {entorno}\n"
    content += f"> FECHA: {subprocess.check_output('date /t' if os.name == 'nt' else 'date', shell=True).decode().strip()}\n\n"

    content += "## 🎯 CAPA (0) - PRESENTE Y PROTOCOLO\n"
    for fname in sorted(files_c0):
        with open(os.path.join(SRC_DIR, fname), "r", encoding="utf-8") as f:
            lines = f.readlines()
            content += f"### 📂 {fname}\n"
            if fname in ["STATUS.md", "PENDIENTES.md", "PROMPT_IA.md"]:
                content += "".join(lines) + "\n\n"
            else:
                content += "".join(lines[:30])
                if len(lines) > 30:
                    content += "\n> ... [Contenido truncado para optimizar]\n"
                content += "\n\n"

    # 2. PROCESAMIENTO DE CAPAS HISTÓRICAS
    dirs = {
        "1": "(1) reciente",
        "2": "(2) doctrina",
        "3": "(3) archivo",
        "4": "(4) pausa",
    }
    for c, folder in sorted(dirs.items()):
        path = os.path.join(SRC_DIR, folder)
        if not os.path.exists(path):
            continue
        files = [f for f in os.listdir(path) if f.endswith(".md")]
        if not files:
            continue
        content += f"## 🗂️ CAPA ({c}) - {folder.upper()}\n"
        for fname in files:
            with open(os.path.join(path, fname), "r", encoding="utf-8") as f:
                content += f"- **{fname}**: {resumir(f.readlines(), c)}\n"
        content += "\n"

    with open(OUT_FILE, "w", encoding="utf-8") as f_out:
        f_out.write(content)

    print(f"✅ Reporte consolidado como {agente} en {OUT_FILE}")


if __name__ == "__main__":
    generate()
