"""
Configurações compartilhadas para testes.
"""

import pytest
import logging
from fastapi.testclient import TestClient

from app.main import create_app
from app.core.session import get_grafo_service, reset_services_state, debug_services_state

# Configuração de logging para testes
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Cria uma única instância da aplicação para todos os testes
@pytest.fixture(scope="session")
def app():
    """
    Cria uma única instância da aplicação FastAPI para todos os testes.
    """
    logger.debug("Criando instância única da aplicação para testes")
    app_instance = create_app()
    return app_instance

# Cria um cliente de teste para a aplicação
@pytest.fixture(scope="session")
def client(app):
    """
    Cria um cliente de teste para a aplicação.
    """
    logger.debug("Criando cliente de teste para a aplicação")
    with TestClient(app) as test_client:
        yield test_client

# Fixture para limpar o estado dos serviços antes de cada teste
@pytest.fixture(autouse=True)
def clean_services_state():
    """
    Limpa o estado dos serviços antes de cada teste.
    """
    logger.debug("Limpando estado dos serviços antes do teste")
    reset_services_state()
    
    # Executa o teste
    yield
    
    # Registra o estado dos serviços após o teste para diagnóstico
    logger.debug("Estado dos serviços após o teste:")
    debug_services_state()

# Fixture para criar um grafo de teste
@pytest.fixture
def grafo_teste(client):
    """
    Cria um grafo de teste e retorna seu ID.
    """
    # Dados para criar um grafo
    grafo_data = {
        "nome": "Grafo de Teste",
        "direcionado": False,
        "ponderado": True,
        "bipartido": False
    }
    
    # Cria o grafo
    response = client.post("/api/v1/grafos/", json=grafo_data)
    assert response.status_code == 201
    grafo_id = response.json()["id"]
    
    # Adiciona alguns vértices e arestas
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "A"})
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "B"})
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "C"})
    
    client.post(f"/api/v1/grafos/{grafo_id}/arestas/", json={"origem": "A", "destino": "B", "peso": 1.5})
    client.post(f"/api/v1/grafos/{grafo_id}/arestas/", json={"origem": "B", "destino": "C", "peso": 2.0})
    
    logger.debug(f"Grafo de teste criado com ID: {grafo_id}")
    
    # Verifica se o grafo foi persistido corretamente
    grafo_service = get_grafo_service()
    grafo = grafo_service.obter_grafo(grafo_id)
    assert grafo is not None
    logger.debug(f"Grafo persistido com {grafo.numero_vertices()} vértices e {grafo.numero_arestas()} arestas")
    
    return grafo_id

# Fixture para criar dois grafos de teste para operações
@pytest.fixture
def grafos_operacoes(client):
    """
    Cria dois grafos de teste para operações e retorna seus IDs.
    """
    # Dados para criar o primeiro grafo
    grafo1_data = {
        "nome": "Grafo 1 para Operações",
        "direcionado": False,
        "ponderado": True,
        "bipartido": False
    }
    
    # Cria o primeiro grafo
    response = client.post("/api/v1/grafos/", json=grafo1_data)
    assert response.status_code == 201
    grafo_id1 = response.json()["id"]
    
    # Adiciona vértices e arestas ao primeiro grafo
    client.post(f"/api/v1/grafos/{grafo_id1}/vertices/", json={"id": "A"})
    client.post(f"/api/v1/grafos/{grafo_id1}/vertices/", json={"id": "B"})
    client.post(f"/api/v1/grafos/{grafo_id1}/vertices/", json={"id": "C"})
    
    client.post(f"/api/v1/grafos/{grafo_id1}/arestas/", json={"origem": "A", "destino": "B", "peso": 1.5})
    client.post(f"/api/v1/grafos/{grafo_id1}/arestas/", json={"origem": "B", "destino": "C", "peso": 2.0})
    
    # Dados para criar o segundo grafo
    grafo2_data = {
        "nome": "Grafo 2 para Operações",
        "direcionado": False,
        "ponderado": True,
        "bipartido": False
    }
    
    # Cria o segundo grafo
    response = client.post("/api/v1/grafos/", json=grafo2_data)
    assert response.status_code == 201
    grafo_id2 = response.json()["id"]
    
    # Adiciona vértices e arestas ao segundo grafo
    client.post(f"/api/v1/grafos/{grafo_id2}/vertices/", json={"id": "B"})
    client.post(f"/api/v1/grafos/{grafo_id2}/vertices/", json={"id": "C"})
    client.post(f"/api/v1/grafos/{grafo_id2}/vertices/", json={"id": "D"})
    
    client.post(f"/api/v1/grafos/{grafo_id2}/arestas/", json={"origem": "B", "destino": "C", "peso": 1.0})
    client.post(f"/api/v1/grafos/{grafo_id2}/arestas/", json={"origem": "C", "destino": "D", "peso": 3.0})
    
    logger.debug(f"Grafos para operações criados com IDs: {grafo_id1}, {grafo_id2}")
    
    # Verifica se os grafos foram persistidos corretamente
    grafo_service = get_grafo_service()
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    grafo2 = grafo_service.obter_grafo(grafo_id2)
    assert grafo1 is not None
    assert grafo2 is not None
    
    logger.debug(f"Grafo 1 persistido com {grafo1.numero_vertices()} vértices e {grafo1.numero_arestas()} arestas")
    logger.debug(f"Grafo 2 persistido com {grafo2.numero_vertices()} vértices e {grafo2.numero_arestas()} arestas")
    
    return {"grafo_id1": grafo_id1, "grafo_id2": grafo_id2}
