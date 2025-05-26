"""
Implementação de persistência temporária para grafos.
"""

import json
import os
import logging
from typing import Dict, Any, List, Optional
import tempfile

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Diretório temporário para armazenamento de grafos
TEMP_DIR = tempfile.mkdtemp(prefix="grafo_api_")
logger.debug(f"Diretório temporário para persistência: {TEMP_DIR}")

def salvar_grafo(grafo_id: str, dados: Dict[str, Any]) -> None:
    """
    Salva os dados de um grafo em um arquivo temporário.
    
    Args:
        grafo_id: ID do grafo.
        dados: Dados do grafo a serem salvos.
    """
    arquivo = os.path.join(TEMP_DIR, f"{grafo_id}.json")
    logger.debug(f"Salvando grafo {grafo_id} em {arquivo}")
    
    try:
        with open(arquivo, 'w') as f:
            json.dump(dados, f, indent=2)
        logger.debug(f"Grafo {grafo_id} salvo com sucesso")
    except Exception as e:
        logger.error(f"Erro ao salvar grafo {grafo_id}: {str(e)}")
        raise

def carregar_grafo(grafo_id: str) -> Optional[Dict[str, Any]]:
    """
    Carrega os dados de um grafo a partir de um arquivo temporário.
    
    Args:
        grafo_id: ID do grafo.
        
    Returns:
        Dados do grafo ou None se o grafo não existir.
    """
    arquivo = os.path.join(TEMP_DIR, f"{grafo_id}.json")
    logger.debug(f"Carregando grafo {grafo_id} de {arquivo}")
    
    if not os.path.exists(arquivo):
        logger.warning(f"Grafo {grafo_id} não encontrado em {arquivo}")
        return None
    
    try:
        with open(arquivo, 'r') as f:
            dados = json.load(f)
        logger.debug(f"Grafo {grafo_id} carregado com sucesso")
        return dados
    except Exception as e:
        logger.error(f"Erro ao carregar grafo {grafo_id}: {str(e)}")
        return None

def excluir_grafo(grafo_id: str) -> bool:
    """
    Exclui os dados de um grafo.
    
    Args:
        grafo_id: ID do grafo.
        
    Returns:
        True se o grafo foi excluído com sucesso, False caso contrário.
    """
    arquivo = os.path.join(TEMP_DIR, f"{grafo_id}.json")
    logger.debug(f"Excluindo grafo {grafo_id} de {arquivo}")
    
    if not os.path.exists(arquivo):
        logger.warning(f"Grafo {grafo_id} não encontrado em {arquivo}")
        return False
    
    try:
        os.remove(arquivo)
        logger.debug(f"Grafo {grafo_id} excluído com sucesso")
        return True
    except Exception as e:
        logger.error(f"Erro ao excluir grafo {grafo_id}: {str(e)}")
        return False

def listar_grafos() -> List[str]:
    """
    Lista os IDs de todos os grafos armazenados.
    
    Returns:
        Lista de IDs de grafos.
    """
    logger.debug(f"Listando grafos em {TEMP_DIR}")
    
    try:
        arquivos = [f for f in os.listdir(TEMP_DIR) if f.endswith('.json')]
        ids = [os.path.splitext(f)[0] for f in arquivos]
        logger.debug(f"Grafos encontrados: {ids}")
        return ids
    except Exception as e:
        logger.error(f"Erro ao listar grafos: {str(e)}")
        return []

def limpar_todos_grafos() -> None:
    """
    Remove todos os grafos armazenados.
    """
    logger.debug(f"Limpando todos os grafos em {TEMP_DIR}")
    
    try:
        for arquivo in os.listdir(TEMP_DIR):
            if arquivo.endswith('.json'):
                os.remove(os.path.join(TEMP_DIR, arquivo))
        logger.debug("Todos os grafos foram removidos")
    except Exception as e:
        logger.error(f"Erro ao limpar grafos: {str(e)}")
