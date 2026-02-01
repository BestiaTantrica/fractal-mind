import os
import time
import subprocess
import shutil

# Configuración de Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_HUB = os.path.join(BASE_DIR, "data_hub")
INBOX = os.path.join(DATA_HUB, "inbox")
PROCESSING = os.path.join(DATA_HUB, "processing")
OUTBOX = os.path.join(DATA_HUB, "outbox")

# Motores
PROJECTS_DIR = os.path.join(BASE_DIR, "projects")
IMAGE_ENGINE = os.path.join(PROJECTS_DIR, "image_engine", "main.py")
VIDEO_ENGINE = os.path.join(PROJECTS_DIR, "video_engine", "main.py")

def setup_folders():
    for folder in [INBOX, PROCESSING, OUTBOX]:
        os.makedirs(folder, exist_ok=True)

def process_file(file_path):
    filename = os.path.basename(file_path)
    tag = filename.lower()
    
    # Mover a procesamiento
    proc_path = os.path.join(PROCESSING, filename)
    shutil.move(file_path, proc_path)
    
    print(f"[*] Procesando: {filename}")
    
    # Leer contenido del archivo (supone que es un prompt o instrucción)
    with open(proc_path, 'r', encoding='utf-8') as f:
        instruction = f.read().strip()

    if "image" in tag:
        output_name = filename.replace(".txt", ".png")
        if not output_name.endswith(".png"): output_name += ".png"
        output_path = os.path.join(OUTBOX, output_name)
        
        print(f"[>] Lanzando Image Engine para: {instruction}")
        subprocess.run(["python", IMAGE_ENGINE, instruction, output_path])
        
    elif "video" in tag:
        print(f"[>] Lanzando Video Engine (Próximamente)...")
        # Aquí irá la lógica de MoviePy
        
    # Limpiar procesamiento
    os.remove(proc_path)
    print(f"[+] Finalizado: {filename}")

def watchdog():
    print("--- HYDROFLOW DISPATCHER ACTIVE ---")
    print(f"Buzón: {INBOX}")
    while True:
        files = [f for f in os.listdir(INBOX) if os.path.isfile(os.path.join(INBOX, f))]
        if files:
            for file in files:
                process_file(os.path.join(INBOX, file))
        time.sleep(2)

if __name__ == "__main__":
    setup_folders()
    watchdog()
