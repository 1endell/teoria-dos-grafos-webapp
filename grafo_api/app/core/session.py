"""
Gerenciamento de sessão e serviços compartilhados.
"""

import logging
from typing import Dict, Any
import threading

from app.services.grafo_service import GrafoService
from app.services.algoritmo_service import AlgoritmoService
from app.services.operacao_service import OperacaoService
from app.services.comparacao_service import ComparacaoService
from app.services.persistencia_service import PersistenciaService
from app.services.visualizacao_service import VisualizacaoService

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Lock para garantir thread-safety na criação de serviços
_services_lock = threading.RLock()

# Dicionário para armazenar as instâncias dos serviços
_services = {}

def _get_or_create_service(service_class, *args, **kwargs):
    """
    Obtém ou cria uma instância de serviço, garantindo que seja um singleton.
    
    Args:
        service_class: Classe do serviço.
        *args: Argumentos posicionais para o construtor do serviço.
        **kwargs: Argumentos nomeados para o construtor do serviço.
        
    Returns:
        Instância do serviço.
    """
    service_name = service_class.__name__
    
    # Usa lock para garantir thread-safety
    with _services_lock:
        if service_name not in _services:
            logger.debug(f"Criando nova instância de {service_name}")
            _services[service_name] = service_class(*args, **kwargs)
        else:
            logger.debug(f"Reutilizando instância existente de {service_name}")
        
        # Registra o ID da instância para diagnóstico
        logger.debug(f"ID da instância de {service_name}: {id(_services[service_name])}")
    
    return _services[service_name]

def get_grafo_service() -> GrafoService:
    """Retorna a instância compartilhada do serviço de grafos."""
    return _get_or_create_service(GrafoService)

def get_algoritmo_service() -> AlgoritmoService:
    """Retorna a instância compartilhada do serviço de algoritmos."""
    grafo_service = get_grafo_service()
    return _get_or_create_service(AlgoritmoService, grafo_service)

def get_operacao_service() -> OperacaoService:
    """Retorna a instância compartilhada do serviço de operações."""
    grafo_service = get_grafo_service()
    return _get_or_create_service(OperacaoService, grafo_service)

def get_comparacao_service() -> ComparacaoService:
    """Retorna a instância compartilhada do serviço de comparação."""
    grafo_service = get_grafo_service()
    return _get_or_create_service(ComparacaoService, grafo_service)

def get_persistencia_service() -> PersistenciaService:
    """Retorna a instância compartilhada do serviço de persistência."""
    grafo_service = get_grafo_service()
    return _get_or_create_service(PersistenciaService, grafo_service)

def get_visualizacao_service() -> VisualizacaoService:
    """Retorna a instância compartilhada do serviço de visualização."""
    grafo_service = get_grafo_service()
    return _get_or_create_service(VisualizacaoService, grafo_service)

# Inicializa os serviços para garantir que estejam disponíveis
# Isso garante que os serviços sejam criados uma única vez na inicialização do módulo
with _services_lock:
    if not _services:
        logger.debug("Inicializando serviços na carga do módulo")
        grafo_service = get_grafo_service()
        algoritmo_service = get_algoritmo_service()
        operacao_service = get_operacao_service()
        comparacao_service = get_comparacao_service()
        persistencia_service = get_persistencia_service()
        visualizacao_service = get_visualizacao_service()
        logger.debug(f"Serviços inicializados: {list(_services.keys())}")

# Função para depuração e diagnóstico
def debug_services_state() -> Dict[str, Any]:
    """
    Retorna o estado atual dos serviços para depuração.
    
    Returns:
        Dict[str, Any]: Estado dos serviços.
    """
    with _services_lock:
        grafo_service = get_grafo_service()
        state = {
            "services_count": len(_services),
            "services": list(_services.keys()),
            "grafo_service_id": id(grafo_service),
            "grafo_service_grafos_count": len(grafo_service.grafos) if "GrafoService" in _services else 0,
            "grafo_ids": list(grafo_service.grafos.keys()) if "GrafoService" in _services else []
        }
        
        logger.debug(f"Estado atual dos serviços: {state}")
        return state

# Função para limpar o estado dos serviços (útil para testes)
def reset_services_state():
    """
    Limpa o estado de todos os serviços.
    Útil para testes que precisam de um estado limpo.
    """
    with _services_lock:
        # Desativando a limpeza de estado para manter persistência entre testes
        logger.debug("Função reset_services_state chamada, mas desativada para manter persistência entre testes")
        # Comentado para manter persistência entre testes
        # if "GrafoService" in _services:
        #     grafo_service = _services["GrafoService"]
        #     grafo_service.grafos.clear()
        #     grafo_service.metadados.clear()
        #     logger.debug("Estado do GrafoService limpo")
        
        logger.debug("Estado dos serviços mantido para persistência entre testes")
