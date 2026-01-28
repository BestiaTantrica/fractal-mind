"""
AIR-Bot - Módulo de Utilidades
Gestión de cuotas y logging a fractal-mind
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QuotaManager:
    """Gestiona las cuotas diarias de imágenes y videos"""
    
    def __init__(self, quota_file: str = "data/quota.json"):
        self.quota_file = Path(quota_file)
        self.quota_file.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_quota_file()
    
    def _ensure_quota_file(self):
        """Crea el archivo de cuotas si no existe"""
        if not self.quota_file.exists():
            self._reset_quota()
    
    def _reset_quota(self):
        """Resetea las cuotas a 0"""
        quota_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "imagenes": 0,
            "videos": 0
        }
        self._write_quota(quota_data)
        logger.info("Cuotas reseteadas")
    
    def _read_quota(self) -> Dict:
        """Lee el archivo de cuotas"""
        try:
            with open(self.quota_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error leyendo cuotas: {e}")
            self._reset_quota()
            return self._read_quota()
    
    def _write_quota(self, data: Dict):
        """Escribe el archivo de cuotas de forma atómica"""
        try:
            # Escribir a archivo temporal primero
            temp_file = self.quota_file.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Renombrar atómicamente
            temp_file.replace(self.quota_file)
        except Exception as e:
            logger.error(f"Error escribiendo cuotas: {e}")
            raise
    
    def verificar_cuota(self, tipo: str = "imagen", limite_img: int = 100, limite_vid: int = 50) -> Tuple[bool, int]:
        """
        Verifica si hay cuota disponible
        
        Args:
            tipo: "imagen" o "video"
            limite_img: Límite diario de imágenes
            limite_vid: Límite diario de videos
        
        Returns:
            (tiene_cuota: bool, restante: int)
        """
        quota_data = self._read_quota()
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Resetear si es un nuevo día
        if quota_data.get("date") != today:
            self._reset_quota()
            quota_data = self._read_quota()
        
        # Verificar cuota según tipo
        campo = "imagenes" if tipo == "imagen" else "videos"
        limite = limite_img if tipo == "imagen" else limite_vid
        usado = quota_data.get(campo, 0)
        restante = max(0, limite - usado)
        
        tiene_cuota = usado < limite
        logger.info(f"Cuota {tipo}: {usado}/{limite} (restante: {restante})")
        
        # COSTO FIJO (1 crédito por acción)
        costo = 1
        
        return tiene_cuota, restante, costo
    
    def incrementar_cuota(self, tipo: str = "imagen"):
        """
        Incrementa el contador de cuota
        
        Args:
            tipo: "imagen" o "video"
        """
        quota_data = self._read_quota()
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Resetear si es un nuevo día
        if quota_data.get("date") != today:
            self._reset_quota()
            quota_data = self._read_quota()
        
        # Incrementar
        campo = "imagenes" if tipo == "imagen" else "videos"
        quota_data[campo] = quota_data.get(campo, 0) + 1
        
        self._write_quota(quota_data)
        logger.info(f"Cuota {tipo} incrementada: {quota_data[campo]}")


class LogManager:
    """Gestiona el logging de interacciones a fractal-mind"""
    
    def __init__(self, fractal_path: str = "../fractal-mind"):
        self.fractal_path = Path(fractal_path)
        self.clientes_path = self.fractal_path / "proyectos" / "redes" / "clientes"
        self.clientes_path.mkdir(parents=True, exist_ok=True)
    
    def registrar_interaccion(
        self,
        user_id: int,
        tipo: str,
        input_texto: str,
        output_info: Dict,
        cuota_actual: Optional[int] = None
    ):
        """
        Registra una interacción en el archivo del usuario
        """
        user_file = self.clientes_path / f"{user_id}.md"
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Construir el log
        log_entry = f"\n## {timestamp}\n"
        log_entry += f"### ID de Usuario: {user_id} - {self._get_tipo_nombre(tipo)}\n"
        log_entry += f"**Tipo de Interacción:** {tipo}\n"
        log_entry += f"**Input:** \"{input_texto}\"\n"
        
        # Agregar info según tipo
        if tipo == "VIDEO_GENERACION":
            log_entry += f"**Caption:** {output_info.get('caption', 'N/A')}\n"
            log_entry += f"**Descripción:** {output_info.get('descripcion', 'N/A')[:100]}...\n"
            log_entry += f"**Hashtags:** {' '.join(output_info.get('hashtags', []))}\n"
            log_entry += f"**Red Social:** {output_info.get('red_social', 'N/A')}\n"
            if cuota_actual is not None:
                log_entry += f"**Cuota Video:** {cuota_actual}/día\n"
        elif tipo == "IMAGEN_EDICION":
            if cuota_actual is not None:
                log_entry += f"**Estado de Cuota:** {cuota_actual}/100\n"
        elif tipo == "GUION_GENERACION":
            log_entry += f"**Hashtags:** {' '.join(output_info.get('hashtags', []))}\n"
            log_entry += f"**Red Social:** {output_info.get('red_social', 'N/A')}\n"
        
        log_entry += f"**Link al Resultado:** [Ver resultado](https://t.me/...)\n"
        log_entry += "-----"
        
        # Escribir al archivo
        try:
            # Crear archivo si no existe
            if not user_file.exists():
                with open(user_file, 'w', encoding='utf-8') as f:
                    f.write(f"# Historial de Usuario {user_id}\n")
                    f.write(f"_Generado automáticamente por AIR-Bot_\n\n")
            
            # Anexar log
            with open(user_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
            
            logger.info(f"Log registrado para usuario {user_id}")
            
            # Guardar en inbox para sincronización (VERSIÓN COMPLETA)
            saved_path = self.save_to_inbox(log_entry)
            return saved_path
            
        except Exception as e:
            logger.error(f"Error escribiendo log: {e}")
            return None

    def save_to_inbox(self, content: str):
        """
        Guarda el contenido en la carpeta inbox del proyecto raíz
        """
        try:
            # Aseguramos que fractal_path sea absoluto
            abs_path = self.fractal_path.absolute()
            inbox_dir = abs_path / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)
            
            # Buscar el siguiente número disponible
            existing_files = [f for f in os.listdir(inbox_dir) if f.startswith("idea_") and f.endswith(".md")]
            numbers = []
            for f in existing_files:
                try:
                    num = int(f.replace("idea_", "").replace(".md", ""))
                    numbers.append(num)
                except ValueError:
                    continue
            
            next_num = max(numbers) + 1 if numbers else 1
            file_name = f"idea_{next_num}.md"
            file_path = inbox_dir / file_name
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            logger.info(f"Guardado en inbox: {file_name}")
            
            # Sincronización automática (Git Push) - Robusta
            self._git_sync(abs_path, file_path, file_name)
            
            return file_path
            
        except Exception as e:
            logger.error(f"Error guardando en inbox: {e}")
            return None

    def _git_sync(self, repo_path: Path, file_path: Path, file_name: str):
        """Ejecuta la sincronización de git de forma segura"""
        try:
            # Comando de git
            cmd = f'git add "{file_path}" && git commit -m "Auto-save (AIR-Bot): {file_name}" && git push origin main'
            
            # Ejecutar en segundo plano de forma robusta
            if os.name == 'nt':
                # Windows: usamos shell=True y quitamos el '&' que causaba problemas
                subprocess.Popen(cmd, shell=True, cwd=repo_path)
            else:
                # Linux/Unix
                subprocess.Popen(f"{cmd} &", shell=True, cwd=repo_path)
                
            logger.info(f"Git sync disparado para {file_name}")
        except Exception as e:
            logger.error(f"Error en git_sync: {e}")

    def sync_manual(self):
        """Fuerza un push manual del repositorio"""
        try:
            abs_path = self.fractal_path.absolute()
            cmd = 'git add . && git commit -m "Manual sync from Bot" && git push origin main'
            
            result = subprocess.run(cmd, shell=True, cwd=abs_path, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Sincronización manual exitosa")
                return True, "Sincronización exitosa."
            else:
                logger.error(f"Error en sincronización manual: {result.stderr}")
                return False, f"Error: {result.stderr}"
        except Exception as e:
            logger.error(f"Excepción en sync_manual: {e}")
            return False, str(e)

    def _get_tipo_nombre(self, tipo: str) -> str:
        """Convierte el tipo a nombre legible"""
        nombres = {
            "VIDEO_GENERACION": "Video Generado",
            "IMAGEN_EDICION": "Imagen Editada",
            "GUION_GENERACION": "Guiones Generados"
        }
        return nombres.get(tipo, "Interacción")


# Funciones de utilidad adicionales

def generar_hashtags_base(tema: str, red_social: str = "tiktok") -> list:
    """
    Genera hashtags base según el tema y red social
    Esto será mejorado por Gemini Pro en ai_processor.py
    """
    hashtags_comunes = {
        "tiktok": ["#FYP", "#Viral", "#TikTok"],
        "instagram": ["#Reels", "#Instagram", "#InstaDaily"],
        "youtube": ["#Shorts", "#YouTube", "#YT"],
        "facebook": ["#Facebook", "#FB"],
        "whatsapp": ["#WhatsApp", "#WA"]
    }
    
    return hashtags_comunes.get(red_social.lower(), ["#Viral"])


def calcular_horario_optimo(red_social: str = "tiktok", tipo_contenido: str = "general") -> Dict:
    """
    Calcula los mejores horarios para publicar según la red social
    
    Returns:
        Diccionario con horarios optimizados
    """
    horarios = {
        "tiktok": {
            "dias_semana": "7:00-9:00 AM, 12:00-1:00 PM, 6:00-8:00 PM",
            "fin_semana": "9:00-11:00 AM, 7:00-9:00 PM"
        },
        "instagram": {
            "dias_semana": "11:00 AM - 1:00 PM, 7:00-9:00 PM",
            "fin_semana": "10:00 AM - 12:00 PM, 6:00-9:00 PM"
        },
        "youtube": {
            "dias_semana": "2:00-4:00 PM, 8:00-10:00 PM",
            "fin_semana": "9:00-11:00 AM, 5:00-7:00 PM"
        },
        "facebook": {
            "dias_semana": "1:00-3:00 PM, 7:00-9:00 PM",
            "fin_semana": "12:00-2:00 PM"
        }
    }
    
    return horarios.get(red_social.lower(), horarios["tiktok"])


def detectar_red_social(texto: str) -> str:
    """
    Detecta la red social mencionada en el texto del usuario
    
    Returns:
        Nombre de la red social detectada (por defecto: "tiktok")
    """
    texto_lower = texto.lower()
    
    if "youtube" in texto_lower or "shorts" in texto_lower:
        return "youtube"
    elif "instagram" in texto_lower or "reels" in texto_lower or "ig" in texto_lower:
        return "instagram"
    elif "tiktok" in texto_lower or "tik tok" in texto_lower:
        return "tiktok"
    elif "facebook" in texto_lower or "fb" in texto_lower:
        return "facebook"
    elif "whatsapp" in texto_lower or "wa" in texto_lower:
        return "whatsapp"
    elif "logo" in texto_lower or "branding" in texto_lower:
        return "logo" # Tratamiento especial para logos
    
    return "tiktok"  # Por defecto


# Instancias globales
quota_manager = QuotaManager()
log_manager = LogManager()
