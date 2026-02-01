import os
import sys
import requests
import random

def generate_image(prompt, output_path):
    print(f"AIR Pro Engine: Esculpiendo imagen para '{prompt}'")
    
    # PRESETS PROFESIONALES
    presets = {
        "cinematic": "cinematic lighting, hyper-realistic, 8k, highly detailed, professional photography, anamorphic lens flares",
        "cyberpunk": "neon lights, synthwave aesthetic, futuristic city, rainy night, high contrast, vibrant colors",
        "studio": "minimalist studio background, soft box lighting, high fashion, professional portrait, clean aesthetic",
        "urban": "street photography, gritty texture, natural lighting, candid, urban style"
    }
    
    # Detectar preset en el prompt
    selected_preset = ""
    for p_name, p_val in presets.items():
        if p_name in prompt.lower():
            selected_preset = p_val
            break
            
    full_prompt = f"{prompt}, {selected_preset}" if selected_preset else f"{prompt}, professional high quality digital art"
    
    # Dimensiones para Reel/TikTok (9:16)
    width = 1080
    height = 1920 
    seed = random.randint(0, 999999)
    
    url = f"https://pollinations.ai/p/{full_prompt.replace(' ', '%20')}?width={width}&height={height}&seed={seed}&model=flux"
    
    try:
        response = requests.get(url, timeout=35) # Más timeout para calidad Flux
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"✨ Obra maestra guardada en: {output_path}")
            return True
        else:
            print(f"❌ Error en API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error de red: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
        
    prompt_arg = sys.argv[1]
    out_arg = sys.argv[2]
    
    if generate_image(prompt_arg, out_arg):
        sys.exit(0)
    else:
        sys.exit(1)
