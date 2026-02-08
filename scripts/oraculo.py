
import os
import google.generativeai as genai
import sys
from pegaso_memory import PegasoMemory

# Configuración de la API (Debería estar en un .env)
# Para esta prueba, buscará la variable de entorno GOOGLE_API_KEY
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("❌ Error: No se encontró GOOGLE_API_KEY en las variables de entorno.")
    sys.exit(1)

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-pro')
pegaso = PegasoMemory()

def chat_oraculo():
    print("--- 🦅 ORACULO PEGASO ACTIVO ---")
    print("Escribe 'salir' para terminar y guardar memoria.")
    
    chat = model.start_chat(history=[])
    full_transcript = ""

    while True:
        user_input = input(">> Operador: ")
        if user_input.lower() in ['salir', 'exit', 'quit']:
            break
        
        response = chat.send_message(user_input)
        print(f"\n>> Gemini: {response.text}\n")
        
        full_transcript += f"Operador: {user_input}\nGemini: {response.text}\n\n"

    if full_transcript:
        print("💾 Guardando charla en la mente fractal...")
        pegaso.log_thread("Consulta al Oraculo", full_transcript, tags=["oraculo", "api"])
        print("✅ Sincronizado.")

if __name__ == "__main__":
    chat_oraculo()
