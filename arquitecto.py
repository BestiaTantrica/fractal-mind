import os
import subprocess
import sys

# --- CONFIGURACIÓN DINÁMICA ---
# Detecta si estamos en Termux (Android) o en PC (Windows/Linux)
IS_TERMUX = os.path.exists("/data/data/com.termux")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if IS_TERMUX:
    OUT_FILE = "/sdcard/Download/SUBIR_A_IA.md"
else:
    OUT_FILE = os.path.join(BASE_DIR, "SUBIR_A_IA.md")


def obtener_contexto_entorno():
    return "TERMUX (Móvil)" if IS_TERMUX else f"PC ({sys.platform})"


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
            "CONCIENCIA: FRAGMENTADA (Modo Supervivencia - Prioridad ALTA)",
        )
    if magia:
        return (
            "✨ PULSO: CREATIVO. Foco en evolución y metáforas estratégicas.",
            "CONCIENCIA: EXPANDIDA (Modo Oráculo - Visión Global)",
        )
    if orden:
        return (
            "📐 PULSO: ESTRUCTURAL. Foco en orden y simetría del sistema.",
            "CONCIENCIA: INTEGRAL (Modo Arquitecto - Consolidación)",
        )
    if estrategia:
        return (
            "⚔️ PULSO: GUERRERO. Foco en optimización y rentabilidad.",
            "CONCIENCIA: ENFOCADA (Modo Bestia - Ejecución Táctica)",
        )
    if aprendizaje:
        return (
            "🧠 PULSO: COGNITIVO. Foco en absorción de nuevo conocimiento.",
            "CONCIENCIA: RECEPTIVA (Modo Aprendiz - Exploración)",
        )

    return (
        "✅ PULSO: ESTABLE. Ciber-Arquitecto en guardia.",
        "CONCIENCIA: VIGILANTE (Modo Centinela - Esperando Input)",
    )


def generate():
    files = [
        f for f in os.listdir(BASE_DIR) if f.endswith(".md") and f != "SUBIR_A_IA.md"
    ]

    # 1. CAPTURA DEL ESTADO ACTUAL
    full_text = ""
    for f in ["STATUS.md", "PENDIENTES.md"]:
        if f in files:
            with open(os.path.join(BASE_DIR, f), "r", encoding="utf-8") as arch:
                full_text += arch.read()

    pulso, conciencia = analizar_pulso(full_text)
    entorno = obtener_contexto_entorno()

    content = f"# 📐 REPORTE CIBER-ARQUITECTO\n"
    content += f"## 🔗 ENCLAVE DE SESIÓN\n> {pulso}\n"
    content += f"> {conciencia}\n"
    content += f"> ENTORNO: {entorno}\n"
    content += f"> FECHA: {subprocess.check_output('date /t' if os.name == 'nt' else 'date', shell=True).decode().strip()}\n\n"

    content += "## 🗺️ MAPA DE PODER\n- Cerebro: fractal-mind\n- Infra: /infra (Centralizado)\n- AWS: 56.125.187.241 (30GB)\n\n"

    # 2. PROCESAMIENTO MODULAR DE ARCHIVOS
    for fname in sorted(files):
        with open(os.path.join(BASE_DIR, fname), "r", encoding="utf-8") as f:
            lines = f.readlines()
            # Prioridad máxima a STATUS y PENDIENTES
            if fname in ["STATUS.md", "PENDIENTES.md"]:
                content += f"## ⚡ {fname} (COMPLETO)\n" + "".join(lines) + "\n\n"
            else:
                # El resto en extractos para ligereza
                content += f"## 📂 {fname} (EXTRACTO)\n" + "".join(lines[:20])
                if len(lines) > 20:
                    content += "\n> ... [Contenido truncado para optimizar contexto]\n"
                content += "\n\n"

    with open(OUT_FILE, "w", encoding="utf-8") as f_out:
        f_out.write(content)

    print(f"OK: Arquitecto ha consolidado la memoria en: {OUT_FILE}")


if __name__ == "__main__":
    generate()
