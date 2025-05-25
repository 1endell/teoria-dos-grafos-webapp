"""
Configurações da aplicação.
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configurações da aplicação."""
    
    # Informações do projeto
    PROJECT_NAME: str = "API de Teoria dos Grafos"
    PROJECT_DESCRIPTION: str = "API para estudo e aplicação de teoria dos grafos com algoritmos avançados"
    PROJECT_VERSION: str = "0.1.0"
    
    # Configurações da API
    API_V1_STR: str = "/api/v1"
    
    # Configurações de CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # Configurações de segurança
    SECRET_KEY: str = "chave_secreta_para_desenvolvimento"
    
    # Configurações de ambiente
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância das configurações
settings = Settings()
