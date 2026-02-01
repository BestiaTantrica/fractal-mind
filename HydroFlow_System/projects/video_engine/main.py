import os
import sys
from moviepy import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

def assemble_video(image_path, audio_path, output_path, caption_text):
    print(f"Video Engine: Ensamblando video con {image_path} y {audio_path}")
    
    # 1. Cargar Audio para saber la duración
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # 2. Cargar Imagen y ajustar duración
    img_clip = ImageClip(image_path).set_duration(duration)
    
    # 3. Crear Subtítulos (Opcional pero recomendado para redes)
    try:
        txt_clip = TextClip(caption_text, font='Arial', font_size=70, color='white', 
                            method='caption', size=(img_clip.size[0]*0.8, None))
        txt_clip = txt_clip.set_position(('center', 'center')).set_duration(duration)
        video = CompositeVideoClip([img_clip, txt_clip])
    except Exception as e:
        print(f"Advertencia: No se pudo crear subtítulos: {e}")
        video = img_clip

    # 4. Unir Audio y Video
    final_video = video.with_audio(audio)
    
    # 5. Exportar
    final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac")
    print(f"Video final exportado a {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python main.py <img_p> <audio_p> <out_p> [caption]")
        sys.exit(1)
        
    img_p = sys.argv[1]
    aud_p = sys.argv[2]
    out_p = sys.argv[3]
    cap_t = sys.argv[4] if len(sys.argv) > 4 else ""
    
    try:
        assemble_video(img_p, aud_p, out_p, cap_t)
        sys.exit(0)
    except Exception as e:
        print(f"Error en ensamblado: {e}")
        sys.exit(1)
