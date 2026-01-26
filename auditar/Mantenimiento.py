import os
import subprocess

def check_memoria():
    # Chequea tamaño de la carpeta auditar
    cmd = "du -sh ~/proyectos/fractal-mind/auditar"
    res = subprocess.check_output(cmd, shell=True).decode()
    print(f"📦 Espacio en Auditoría: {res}")

def limpiar_links_rotos():
    # Busca y elimina links simbólicos que apuntan a la nada
    print("🧹 Limpiando links rotos...")
    os.system("find ~/proyectos -xtype l -delete")

def status_git():
    # Chequea si te olvidaste de subir algo importante
    print("🐙 Estado de Git:")
    os.system("git -C ~/proyectos/freqtrade-bestia status -s")

if __name__ == "__main__":
    print("--- INICIANDO MANTENIMIENTO TÉCNICO ---")
    check_memoria()
    limpiar_links_rotos()
    status_git()
    print("--- TODO EN ORDEN, TOMÁS ---")