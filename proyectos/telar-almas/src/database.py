from supabase import create_client, Client
from .config import Config

class Database:
    _instance: Client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._instance is None:
            if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
                raise ValueError("No se puede inicializar Supabase sin URL y KEY")
            cls._instance = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        return cls._instance

# Singleton para usar en todo el proyecto
db = Database
