"""
Arquivo de testes para os endpoints de visualização de grafos.
"""

import pytest
from app.core.session import get_grafo_service


def test_visualizar_grafo(client, grafo_teste):
    """Testa a visualização de um grafo."""
    # Usa o grafo criado pela fixture
    grafo_id = grafo_teste
    
    # Faz a requisição para visualizar o grafo
    response = client.get(f"/api/v1/visualizacao/{grafo_id}?layout=spring&incluir_atributos=true")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém os dados de visualização
    data = response.json()
    assert "vertices" in data
    assert "arestas" in data
    assert "layout" in data
    assert data["layout"] == "spring"
    
    # Verifica se os vértices e arestas estão corretos
    assert len(data["vertices"]) == 3  # A, B, C
    assert len(data["arestas"]) == 2  # A-B, B-C


def test_visualizar_grafo_por_id(client, grafo_teste):
    """Testa a visualização de um grafo pelo ID."""
    # Usa o grafo criado pela fixture
    grafo_id = grafo_teste
    
    # Faz a requisição para visualizar o grafo
    response = client.get(f"/api/v1/visualizacao/{grafo_id}")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém os dados de visualização
    data = response.json()
    assert "vertices" in data
    assert "arestas" in data
    assert "layout" in data
    
    # Verifica se os vértices e arestas estão corretos
    assert len(data["vertices"]) == 3  # A, B, C
    assert len(data["arestas"]) == 2  # A-B, B-C


def test_listar_layouts(client):
    """Testa a listagem de layouts de visualização."""
    # Faz a requisição para listar os layouts
    response = client.get("/api/v1/visualizacao/layouts")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém a lista de layouts
    data = response.json()
    assert isinstance(data, list)
    assert "spring" in data
    assert "circular" in data


def test_gerar_imagem_grafo(client, grafo_teste):
    """Testa a geração de uma imagem de um grafo."""
    # Usa o grafo criado pela fixture
    grafo_id = grafo_teste
    
    # Faz a requisição para gerar a imagem
    response = client.get(f"/api/v1/visualizacao/{grafo_id}/imagem?formato=png&layout=spring")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém os dados da imagem
    data = response.json()
    assert data["grafo_id"] == grafo_id
    assert data["formato"] == "png"
    assert data["layout"] == "spring"
    assert "conteudo" in data


def test_visualizar_grafo_layout_invalido(client, grafo_teste):
    """Testa a visualização de um grafo com layout inválido."""
    # Usa o grafo criado pela fixture
    grafo_id = grafo_teste
    
    # Faz a requisição com layout inválido
    response = client.get(f"/api/v1/visualizacao/{grafo_id}?layout=layout_invalido")
    
    # Verifica se a resposta indica erro
    assert response.status_code == 400
