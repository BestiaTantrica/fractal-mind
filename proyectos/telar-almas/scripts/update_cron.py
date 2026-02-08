import sys
import os
import time

# Añadir el path para poder importar desde src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import db
from src.prompts import PromptGenerator

def update_all_arcanos():
    """
    Función que revisa todos los Arcanos y los actualiza.
    """
    print("🌅 Iniciando ciclo diario de actualización de almas...")
    try:
        supabase = db.get_client()
        # 1. Obtener todos los arcanos
        arcanos = supabase.table("arcanos").select("*").execute()
        
        for arcano in arcanos.data:
            print(f"Refinando Arcano {arcano['id']}...")
            
            # TODO: Lógica de IA para decidir si gana XP o cambia de sombra
            # Por ahora, simulamos una ganancia pasiva de XP
            new_xp = arcano['xp'] + 10
            new_level = arcano['level']
            
            # Verificar Level Up
            if new_xp >= new_level * 100:
                new_level += 1
                print(f"🌟 ¡LEVEL UP! {arcano['id']} subió a nivel {new_level}")
            
            # Actualizar en DB
            supabase.table("arcanos").update({
                "xp": new_xp,
                "level": new_level
            }).eq("id", arcano['id']).execute()

        print("✅ Ciclo completado.")
    except Exception as e:
        print(f"❌ Error en el cron: {e}")

if __name__ == "__main__":
    while True:
        update_all_arcanos()
        # En una versión real, esto correría cada 24hs o disparado por un scheduler
        print("Zzz... Durmiendo hasta el próximo ciclo.")
        time.sleep(3600 * 24) # 24 horas
