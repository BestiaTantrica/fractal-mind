import sys
import os

# Asegurar que el directorio raíz está en el path para importar 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.abstract_art import AbstractArtGenerator
import webbrowser

def preview_production_assets():
    """
    Genera y abre los links de producción (GRATIS) para ver la calidad real.
    """
    assets = AbstractArtGenerator.generate_layered_assets({})
    
    print("--- GENERANDO ACTIVOS DE PRODUCCIÓN (FLUX) ---")
    for layer, url in assets.items():
        print(f"[{layer.upper()}]: {url}")
        # Abrimos en el navegador para que el usuario vea la calidad real
        webbrowser.open(url)

if __name__ == "__main__":
    preview_production_assets()
