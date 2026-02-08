from .emotion_engine import EmotionEngine

class AbstractArtGenerator:
    """
    Generador de activos de producción usando Pollinations.ai (FREE).
    Usa Seeds fijas para garantizar que el estilo no cambie (sin sorpresas).
    """
    
    BASE_URLS = [
        "https://image.pollinations.ai/prompt/",
        "https://api.v0.pollinations.ai/prompt/" # Backup endpoint
    ]
    # El SEED asegura que el "estilo artistico" sea el mismo para todas las capas.
    STYLE_SEED = 42240412 

    @staticmethod
    def get_production_url(prompt, width=1024, height=1024, layer_seed_offset=0):
        """
        Genera un link directo a la imagen.
        """
        clean_prompt = prompt.replace(" ", "%20")
        seed = AbstractArtGenerator.STYLE_SEED + layer_seed_offset
        # Probamos el endpoint principal
        return f"{AbstractArtGenerator.BASE_URLS[0]}{clean_prompt}?width={width}&height={height}&seed={seed}&model=flux&nologo=true"

    @staticmethod
    def generate_layered_assets(natal_data):
        """
        Genera el paquete de 3 capas con links de producción REALES.
        """
        # 1. Capas (Fondo, Medio, Frente)
        # Usamos prompts que evocan la "Personalidad" (Aries/Saturno)
        
        # FONDO: Vacío cósmico y papel quemado
        prompt_back = "Abstract cosmic void, edges of burnt ancient paper, deep crimson and indigo tones, extreme detail, 8k, cinematic."
        
        # MEDIO: Los Cristales de Saturno (Transmutación)
        prompt_mid = "Floating sharp crystalline shards, frozen structures, dark glass, cosmic dust, deep shadow, on black background."
        
        # FRENTE: El Fuego de Aries (Impulso)
        prompt_front = "Electric plasma arcs, living fire filaments, bright energy core, rays of light, intense glow, on black background."

        return {
            "back": AbstractArtGenerator.get_production_url(prompt_back, layer_seed_offset=1),
            "mid": AbstractArtGenerator.get_production_url(prompt_mid, layer_seed_offset=2),
            "front": AbstractArtGenerator.get_production_url(prompt_front, layer_seed_offset=3)
        }
