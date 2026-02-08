from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const

class AstrologyEngine:
    @staticmethod
    def calculate_chart(date_str, time_str, lat, lon):
        """
        Calcula la carta natal básica.
        date_str: 'YYYY/MM/DD'
        time_str: 'HH:MM'
        """
        date = Datetime(date_str, time_str, '+00:00') # Usamos UTC por defecto para normalizar
        pos = GeoPos(lat, lon)
        chart = Chart(date, pos)
        
        # Extraer puntos clave
        data = {
            "sun": AstrologyEngine._get_obj_data(chart.get(const.SUN)),
            "moon": AstrologyEngine._get_obj_data(chart.get(const.MOON)),
            "ascendant": AstrologyEngine._get_obj_data(chart.get(const.ASC)),
            "mars": AstrologyEngine._get_obj_data(chart.get(const.MARS)),
            "jupiter": AstrologyEngine._get_obj_data(chart.get(const.JUPITER)),
            "saturn": AstrologyEngine._get_obj_data(chart.get(const.SATURN)),
        }
        return data

    @staticmethod
    def _get_obj_data(obj):
        if not obj: return None
        return {
            "id": obj.id,
            "sign": obj.sign,
            "sign_lon": round(obj.signlon, 2),
            "house": obj.house if hasattr(obj, 'house') else None
        }

# Prueba simple si se ejecuta directo
if __name__ == "__main__":
    engine = AstrologyEngine()
    # Una prueba rápida: 1 de enero de 2000, 12:00, Buenos Aires
    test_chart = engine.calculate_chart('2000/01/01', '12:00', -34.60, -58.38)
    print(test_chart)
