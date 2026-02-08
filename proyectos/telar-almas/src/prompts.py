class PromptGenerator:
    ARCANOS_BASE = {
        0: "The Fool, a traveler at the edge of a cliff, ethereal energy.",
        1: "The Magician, mastering the four elements, cosmic altar.",
        2: "The High Priestess, guardian of secrets, moonlight and pillars.",
        # ... se completarán los 22
    }

    @staticmethod
    def generate_image_prompt(arcano_num, natal_data, level=1):
        base = PromptGenerator.ARCANOS_BASE.get(arcano_num, "Mystical Entity")
        sun_sign = natal_data['sun']['sign']
        moon_sign = natal_data['moon']['sign']
        
        prompt = f"Digital art, high fantasy style. {base} "
        prompt += f"Influenced by the zodiac sign {sun_sign}. "
        prompt += f"Atmosphere of {moon_sign} energy. "
        
        if level > 1:
            prompt += f"Evolved state, level {level}, glowing aura, intricate details, mastery."
        else:
            prompt += "Level 1, nascent power, subtle mystical glow."
            
        prompt += " Cinematic lighting, 8k resolution, trending on ArtStation."
        return prompt

    @staticmethod
    def generate_description_prompt(arcano_num, natal_data):
        # Este será para que Gemini nos dé una descripción narrativa "esotérica"
        return f"Escribe una descripción corta y mística para un Arcano Mayor tipo {arcano_num} nacido con el Sol en {natal_data['sun']['sign']} y la Luna en {natal_data['moon']['sign']}. Habla de su destino y su poder."
