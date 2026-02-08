
import os
import requests
import json
import sys
import datetime
import re

# Cargamos la llave desde el entorno
API_KEY = os.getenv("GOOGLE_API_KEY")
MEMORY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memory")
THREADS_DIR = os.path.join(MEMORY_DIR, "threads")

if not API_KEY:
    print("❌ Error: No se encontro GOOGLE_API_KEY.")
    sys.exit(1)

def chat_oraculo():
    print("--- 🦅 ORACULO PEGASO (VERSION LIGERA) ---")
    print("Escribe 'salir' para terminar y guardar memoria.")
    
    chat_history = []
    full_transcript = ""

    while True:
        user_input = input(">> Operador: ")
        if user_input.lower() in ['salir', 'exit', 'quit']:
            break
        
        # Modelo ultra-compatible
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
        headers = {'Content-Type': 'application/json'}
        
        # Estructura JSON estándar de Gemini
        payload = {
            "contents": [{
                "parts": [{"text": user_input}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            answer = data['candidates'][0]['content']['parts'][0]['text']
            
            print(f"\n>> Gemini: {answer}\n")
            full_transcript += f"Operador: {user_input}\nGemini: {answer}\n\n"
        except Exception as e:
            print(f"❌ Error en la API: {e}")
            break

    if full_transcript:
        print("💾 Guardando charla en la mente fractal...")
        # Guardado manual simplificado
        if not os.path.exists(THREADS_DIR): os.makedirs(THREADS_DIR)
        safe_date = datetime.date.today()
        filename = f"{safe_date}_Charla_Oraculo.md"
        filepath = os.path.join(THREADS_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# Charla con Oraculo\nFecha: {datetime.datetime.now()}\n\n## RESUMEN DE LA CHARLA\n{full_transcript}")
        
        # Sincronizamos con Git
        repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.system(f'git -C "{repo_dir}" add memory/*')
        os.system(f'git -C "{repo_dir}" commit -m "Pegaso: Charla del Oraculo guardada"')
        os.system(f'git -C "{repo_dir}" push origin main')
        print("✅ Sincronizado con la nube.")

if __name__ == "__main__":
    chat_oraculo()
