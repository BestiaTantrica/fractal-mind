import sys
import os
from datetime import datetime

# Añadir el path para poder importar desde src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.astrology_engine import AstrologyEngine
from src.database import db

def get_arcano_from_sign(sign):
    """Mapeo básico de Signo Solar a Arcano Mayor."""
    mapping = {
        'Aries': 4,       # El Emperador
        'Taurus': 5,      # El Hierofante
        'Gemini': 6,      # Los Enamorados
        'Cancer': 7,      # El Carro
        'Leo': 8,         # La Fuerza
        'Virgo': 9,       # El Ermitaño
        'Libra': 11,      # La Justicia
        'Scorpio': 13,     # La Muerte
        'Sagittarius': 14, # La Templanza
        'Capricorn': 15,   # El Diablo
        'Aquarius': 17,    # La Estrella
        'Pisces': 18      # La Luna
    }
    return mapping.get(sign, 0) # El Loco por defecto

def mint_arcano(wallet, dob, tob, lat, lon, arcano_num=None):
    """
    Crea un nuevo Arcano en la DB.
    dob: 'YYYY/MM/DD'
    tob: 'HH:MM'
    """
    print(f"🔮 Iniciando rito de Génesis para {wallet}...")
    
    # 1. Calcular Carta Natal
    engine = AstrologyEngine()
    try:
        natal_data = engine.calculate_chart(dob, tob, lat, lon)
    except Exception as e:
        print(f"❌ Error en el motor astrológico: {e}")
        return

    # 2. Determinar Arcano
    sun_sign = natal_data['sun']['sign']
    if arcano_num is None:
        arcano_num = get_arcano_from_sign(sun_sign)
        print(f"✨ Arcano seleccionado por destino ({sun_sign}): {arcano_num}")
    
    # 3. Generar Atributos Iniciales basados en la carta
    # Ejemplo: Si Marte está en signo de fuego, más fuerza.
    sun_sign = natal_data['sun']['sign']
    mars_sign = natal_data['mars']['sign']
    
    attributes = {
        "fuerza": 10 + (5 if mars_sign in ['Aries', 'Leo', 'Sagittarius'] else 0),
        "sabiduria": 10 + (5 if sun_sign in ['Aquarius', 'Gemini', 'Libra'] else 0),
        "esencia": sun_sign,
        "sombra_inicial": "Ninguna"
    }

    # 4. Guardar en Supabase
    try:
        supabase = db.get_client()
        data = {
            "owner_wallet": wallet,
            "arcano_type": arcano_num,
            "natal_data": natal_data,
            "current_attributes": attributes,
            "xp": 0,
            "level": 1
        }
        result = supabase.table("arcanos").insert(data).execute()
        print(f"✅ Arcano creado con éxito. ID: {result.data[0]['id']}")
        return result.data[0]
    except Exception as e:
        print(f"❌ Error al guardar en Supabase: {e}")

if __name__ == "__main__":
    # PRUEBA DE CALIBRACIÓN: Datos del Usuario
    # 12/04/1982, Almagro (BS AS), Argentina, 02:30hs. GMT-3
    mint_arcano(
        wallet="0xUserCalibration", 
        dob="1982/04/12", 
        tob="05:30", # UTC (02:30 local + 3hs)
        lat=-34.61, 
        lon=-58.42, 
        arcano_num=None # Que lo seleccione automáticamente
    )

