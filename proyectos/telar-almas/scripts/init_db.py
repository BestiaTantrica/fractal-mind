from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    url = os.getenv("SUPABASE_URL")
    # Para DDL (crear tablas) necesitamos la SERVICE_ROLE_KEY
    key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("Faltan credenciales.")
        return

    supabase = create_client(url, key)
    
    # Intento de creación de tablas vía RPC o SQL directo si el SDK lo permite
    # Nota: El SDK de Python usualmente no permite SQL directo por seguridad, 
    # por lo que el SQL Editor es la vía recomendada.
    
    print(f"Conectado a {url}. Intentando verificar tablas...")
    # Aquí podríamos hacer un check de una tabla
    try:
        supabase.table("arcanos").select("*").limit(1).execute()
        print("✅ Acceso a tabla 'arcanos' verificado.")
    except Exception as e:
        print(f"❌ No se pudo acceder a las tablas: {e}")
        print("Acción sugerida: Ejecuta el SQL en el 'SQL Editor' de Supabase.")

if __name__ == "__main__":
    init_db()
