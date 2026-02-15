import os
import json
import shutil

def setup():
    # Directorio actual
    target_dir = os.getcwd()
    print(f"🚀 Iniciando instalación de HydroFlow en: {target_dir}")

    # Estructura de carpetas
    folders = [
        "HydroFlow_System/data_hub/stage_1_output",
        "HydroFlow_System/data_hub/stage_2_audits",
        "HydroFlow_System/data_hub/final_products",
        "HydroFlow_System/projects",
        "HydroFlow_System/telegram_handler"
    ]

    for folder in folders:
        path = os.path.join(target_dir, folder)
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"✅ Carpeta creada: {folder}")

    # Configuración de Agentes (Rutas Absolutas Maestras)
    # Asumimos que los agentes viven en fractal-mind central
    base_agents_path = "c:/fractal-mind/scripts"
    
    config = {
        "project_name": os.path.basename(target_dir),
        "agents": {
            "mente": os.path.join(base_agents_path, "agente_mente_v7.py"),
            "air": os.path.join(base_agents_path, "agente_air.py"), # Referencia cruzada
            "mentor": os.path.join(base_agents_path, "oraculo.py"),
            "pm": "Antigravity (System)"
        },
        "status": "OPERATIONAL"
    }

    config_path = os.path.join(target_dir, "HydroFlow_System", "config.json")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)
    
    print(f"✅ Archivo de configuración generado en: {config_path}")
    print("\n🎉 ¡Sistema HydroFlow listo! Ahora puedes pedirme orquestación en este repositorio.")

if __name__ == "__main__":
    setup()
