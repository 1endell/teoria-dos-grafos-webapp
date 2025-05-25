"""
Arquivo de testes para os endpoints de visualização de grafos.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from tests.test_grafos import test_criar_grafo

# Cria o cliente de teste
app = create_app()
client = TestClient(app)


def test_visualizar_grafo():
    """Testa a geração de dados para visualização de um grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Dados para a visualização
    visualizacao_data = {
        "grafo_id": grafo_id,
        "layout": "spring",
        "incluir_atributos": True
    }
    
    # Faz a requisição para visualizar o grafo
    response = client.post("/api/v1/visualizacao/", json=visualizacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém os dados de visualização
    data = response.json()
    assert "vertices" in data
    assert "arestas" in data
    assert "layout" in data
    assert data["layout"] == "spring"
    
    # Verifica se os vértices e arestas estão presentes
    assert len(data["vertices"]) >= 3  # A, B, C
    assert len(data["arestas"]) >= 2  # A-B, B-C
    
    # Verifica se os vértices têm as propriedades necessárias
    for vertice in data["vertices"]:
        assert "id" in vertice
        assert "x" in vertice
        assert "y" in vertice
        assert "grau" in vertice
        if visualizacao_data["incluir_atributos"]:
            assert "atributos" in vertice
    
    # Verifica se as arestas têm as propriedades necessárias
    for aresta in data["arestas"]:
        assert "origem" in aresta
        assert "destino" in aresta
        if visualizacao_data["incluir_atributos"]:
            assert "atributos" in aresta


def test_visualizar_grafo_por_id():
    """Testa a geração de dados para visualização de um grafo pelo ID."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para visualizar o grafo
    response = client.get(f"/api/v1/visualizacao/{grafo_id}?layout=circular&incluir_atributos=true")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém os dados de visualização
    data = response.json()
    assert "vertices" in data
    assert "arestas" in data
    assert "layout" in data
    assert data["layout"] == "circular"
    
    # Verifica se os vértices e arestas estão presentes
    assert len(data["vertices"]) >= 3  # A, B, C
    assert len(data["arestas"]) >= 2  # A-B, B-C


def test_listar_layouts():
    """Testa a listagem de layouts de visualização disponíveis."""
    # Faz a requisição para listar os layouts
    response = client.get("/api/v1/visualizacao/layouts")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém a lista de layouts
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    
    # Verifica se os layouts comuns estão presentes
    assert "spring" in data
    assert "circular" in data
    assert "spectral" in data


def test_gerar_imagem_grafo():
    """Testa a geração de uma imagem de visualização do grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para gerar a imagem
    response = client.get(f"/api/v1/visualizacao/{grafo_id}/imagem?layout=spring&formato=png&tamanho=800x600")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se o cabeçalho Content-Disposition está presente
    assert "Content-Disposition" in response.headers
    assert "attachment" in response.headers["Content-Disposition"]
    
    # Verifica se o tipo de conteúdo é correto
    assert response.headers["content-type"] == "image/png"
    
    # Verifica se o conteúdo não está vazio
    assert len(response.content) > 0


def test_visualizar_grafo_inexistente():
    """Testa a visualização de um grafo inexistente."""
    # ID de um grafo inexistente
    grafo_id = "grafo_inexistente"
    
    # Dados para a visualização
    visualizacao_data = {
        "grafo_id": grafo_id,
        "layout": "spring",
        "incluir_atributos": True
    }
    
    # Faz a requisição para visualizar o grafo
    response = client.post("/api/v1/visualizacao/", json=visualizacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404


def test_visualizar_grafo_layout_invalido():
    """Testa a visualização de um grafo com layout inválido."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Dados para a visualização com layout inválido
    visualizacao_data = {
        "grafo_id": grafo_id,
        "layout": "layout_invalido",
        "incluir_atributos": True
    }
    
    # Faz a requisição para visualizar o grafo
    response = client.post("/api/v1/visualizacao/", json=visualizacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404 or response.status_code == 500
