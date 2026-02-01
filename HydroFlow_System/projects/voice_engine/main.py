import asyncio
import sys
import os
from gtts import gTTS

async def text_to_speech(text, output_path):
    print(f"Voice Engine: Generando audio para '{text[:30]}...'")
    
    try:
        # Intentamos primero con Edge-TTS (Calidad Premium)
        import edge_tts
        voice = "es-AR-ElenaNeural"
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)
        print(f"Audio premium guardado en {output_path}")
    except Exception as e:
        print(f"Advertencia: Edge-TTS falló ({e}). Usando gTTS (Google) como respaldo...")
        # Fallback a gTTS (Más robusto ante DNS caprichosos)
        tts = gTTS(text=text, lang='es')
        tts.save(output_path)
        print(f"Audio de respaldo guardado en {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
        
    text_arg = sys.argv[1]
    out_arg = sys.argv[2]
    
    asyncio.run(text_to_speech(text_arg, out_arg))
    sys.exit(0)
