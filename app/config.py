"""
Configuración de la aplicación.
Lee las variables de entorno y las expone de forma segura.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Configuración centralizada de la aplicación.
    Pydantic valida automáticamente que las variables existan y tengan el tipo correcto.
    """
    
    # Google Cloud Platform
    gcp_project_id: str = "diagnovet-challenge"  # Cámbialo por tu PROJECT_ID real
    gcp_location: str = "us"
    gcp_processor_id: str = ""  # Lo configuraremos después
    gcs_bucket_name: str = "diagnovet-reports-images"  # Cámbialo por el nombre de tu bucket
    
    # Credenciales: usaremos Application Default Credentials (no necesita archivo JSON)
    google_application_credentials: str = ""  # Vacío = usa ADC automáticamente
    
    # Configuración de la aplicación
    environment: str = "development"
    
    class Config:
        # Busca estas variables en un archivo .env
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()  # Cachea la instancia para no leer el .env múltiples veces
def get_settings() -> Settings:
    """
    Retorna la configuración de la aplicación.
    El decorador @lru_cache hace que se ejecute solo una vez.
    """
    return Settings()
