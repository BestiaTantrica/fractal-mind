import subprocess
import os
import sys
import json
import logging

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("hydroflow.log"),
        logging.StreamHandler()
    ]
)

class HydroFlowDispatcher:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "base_path": os.getcwd(),
                "data_hub": "data_hub",
                "projects_path": "projects"
            }

    def run_stage(self, project_name, input_path, output_path, params=None):
        logging.info(f"Iniciando Stage: {project_name}")
        
        project_dir = os.path.join(self.config['projects_path'], project_name)
        main_script = os.path.join(project_dir, 'main.py')
        
        if not os.path.exists(main_script):
            logging.error(f"No se encontró el script principal en {main_script}")
            return False, "Script no encontrado"

        cmd = [sys.executable, main_script, input_path, output_path]
        if params:
            cmd.extend(params)

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )
            logging.info(f"Stage {project_name} completado con éxito.")
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            error_msg = f"Error en {project_name}. Código: {e.returncode}\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}"
            logging.error(error_msg)
            return False, error_msg

    def dispatch_air_refinement(self, prompt_text):
        logging.info("--- Iniciando Refinamiento para Bot AIR ---")
        
        # Guardamos el prompt original en el hub
        input_file = os.path.join(self.config['data_hub'], "stage_1_output", "air_request.txt")
        output_file = os.path.join(self.config['data_hub'], "final_products", "air_refined_prompt.txt")
        
        with open(os.path.join(self.config['base_path'], input_file), 'w') as f:
            f.write(prompt_text)

        success, msg = self.run_stage(
            "agente_mente_refiner", 
            input_file, 
            output_file
        )
        
        if success:
            with open(os.path.join(self.config['base_path'], output_file), 'r') as f:
                return f.read()
        return "Error en el refinamiento."

    def dispatch_social_production(self, title, script_text, image_prompt):
        logging.info(f"--- Iniciando Producción de Contenido: {title} ---")
        
        # Rutas de trabajo ABSOLUTAS
        base_hub = os.path.join(self.config['base_path'], self.config['data_hub'])
        audio_file = os.path.join(base_hub, "stage_1_output", f"{title}_audio.mp3")
        image_file = os.path.join(base_hub, "stage_1_output", f"{title}_image.jpg")
        video_file = os.path.join(base_hub, "final_products", f"{title}_final.mp4")

        # 1. Generar Voz
        success_v, msg_v = self.run_stage("voice_engine", script_text, audio_file)
        if not success_v: return False, "Fallo en Voz"

        # 2. Generar Imagen vía Bot AIR
        success_i, msg_i = self.run_stage("air_bridge", image_prompt, image_file)
        if not success_i: return False, "Fallo en AIR (Imagen)"

        # 3. Ensamblar Video
        success_vid, msg_vid = self.run_stage(
            "video_engine", 
            image_file, 
            audio_file, 
            params=[video_file, script_text]
        )
        
        if success_vid:
            logging.info(f"Producción exitosa: {video_file}")
            return True, video_file
        return False, "Fallo en Ensamblado"

if __name__ == "__main__":
    dispatcher = HydroFlowDispatcher()
    # Test de Producción Social
    dispatcher.dispatch_social_production(
        "Legado_Digital", 
        "Este es un legado para mis hijos, un arsenal de producción digital gratuito.", 
        "A futuristic library with digital interfaces and children learning, cinematic style"
    )
