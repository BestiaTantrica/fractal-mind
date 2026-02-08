import sys
import os

# Añadir el path para poder importar desde src si se ejecuta como script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.emotion_engine import EmotionEngine
except ImportError:
    from emotion_engine import EmotionEngine # Fallback si se corre desde src

import json

class VisualLayers:
    @staticmethod
    def generate_asset_bundle(natal_data):
        """
        Genera prompts para 3 capas + configuración de animación.
        """
        features = EmotionEngine.analyze_aspects(natal_data)
        palette = EmotionEngine.get_core_palette("Aries", "Aquarius") 
        
        # 1. LAYER BACK (Atmósfera)
        prompt_back = (
            f"Background texture only. Infinite cosmic void, burnt edges of ancient paper style. "
            f"Color palette: {palette['base']}. Minimalist, deep depth of field. Soft nebula clouds."
        )

        # 2. LAYER MID (La Tensión Flotante)
        tensions = ". ".join([f.get('visual_effect') for f in features])
        prompt_mid = (
            f"Floating abstract elements on transparent background. "
            f"Crystalline shards, broken glass structures, geometric debris. "
            f"Visual metaphor: {tensions}. Sharp focus, high contrast. "
            f"No background, isolated elements."
        )

        # 3. LAYER FRONT (El Núcleo/Luz)
        prompt_front = (
            f"Pure light effects on transparent background. "
            f"Electric arcs in {palette['accent']}. Glowing runes, plasma filaments. "
            f"Intense brightness, lens flares, mystical energy core. "
            f"No heavy structures, just light and energy."
        )
        
        # 4. CONFIG DE ANIMACIÓN (Json)
        # Determinamos movimiento basado en la "Modalidad" (Cardinal = Rápido, Fijo = Lento)
        # Por ahora hardcoded para Aries (Cardinal)
        anim_config = {
            "pulse_speed": "FAST" if "Aries" in str(natal_data) else "SLOW", # Simplificado
            "float_amplitude": 15, # Parallax
            "glow_color": palette['accent'].split(' ')[-1], # "Blue" o "Red"
            "shake_on_impact": True # Si hay aspectos tensos
        }

        return {
            "prompts": {
                "back": prompt_back,
                "mid": prompt_mid,
                "front": prompt_front
            },
            "animation_config": anim_config
        }

if __name__ == "__main__":
    # Test rápido
    bundle = VisualLayers.generate_asset_bundle({})
    print(json.dumps(bundle, indent=2))
