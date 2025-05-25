"""
Arquivo de testes para os endpoints de algoritmos.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from tests.test_grafos import test_criar_grafo

# Cria o cliente de teste
app = create_app()
client = TestClient(app)


def test_listar_algoritmos():
    """Testa a listagem de algoritmos disponíveis."""
    # Faz a requisição para listar os algoritmos
    response = client.get("/api/v1/algoritmos/")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém a lista de algoritmos
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    
    # Verifica se cada algoritmo tem os campos necessários
    for algoritmo in data:
        assert "id" in algoritmo
        assert "nome" in algoritmo
        assert "categoria" in algoritmo
        assert "descricao" in algoritmo
        assert "parametros_obrigatorios" in algoritmo
        assert "parametros_opcionais" in algoritmo


def test_listar_algoritmos_por_categoria():
    """Testa a listagem de algoritmos por categoria."""
    # Categorias a testar
    categorias = ["caminhos", "arvores", "fluxo", "coloracao", "emparelhamento", 
                 "planaridade", "espectral", "centralidade"]
    
    for categoria in categorias:
        # Faz a requisição para listar os algoritmos da categoria
        response = client.get(f"/api/v1/algoritmos/{categoria}")
        
        # Verifica se a resposta foi bem-sucedida
        assert response.status_code == 200
        
        # Verifica se a resposta contém a lista de algoritmos
        data = response.json()
        assert isinstance(data, list)
        
        # Verifica se todos os algoritmos são da categoria correta
        for algoritmo in data:
            assert algoritmo["categoria"] == categoria


def test_executar_algoritmo_dijkstra():
    """Testa a execução do algoritmo de Dijkstra."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Parâmetros para o algoritmo
    params = {
        "parametros": {
            "origem": "A"
        }
    }
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/dijkstra/{grafo_id}", json=params)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado do algoritmo
    data = response.json()
    assert data["algoritmo"] == "dijkstra"
    assert data["grafo_id"] == grafo_id
    assert "resultado" in data
    assert "tempo_execucao" in data
    
    # Verifica se o resultado contém as distâncias
    assert "A" in data["resultado"]
    assert "B" in data["resultado"]
    assert "C" in data["resultado"]


def test_executar_algoritmo_coloracao():
    """Testa a execução do algoritmo de coloração."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/coloracao_welsh_powell/{grafo_id}", json={})
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado do algoritmo
    data = response.json()
    assert data["algoritmo"] == "coloracao_welsh_powell"
    assert data["grafo_id"] == grafo_id
    assert "resultado" in data
    assert "tempo_execucao" in data
    
    # Verifica se o resultado contém as cores dos vértices
    assert "A" in data["resultado"]
    assert "B" in data["resultado"]
    assert "C" in data["resultado"]


def test_executar_algoritmo_centralidade():
    """Testa a execução do algoritmo de centralidade."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/centralidade_grau/{grafo_id}", json={})
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado do algoritmo
    data = response.json()
    assert data["algoritmo"] == "centralidade_grau"
    assert data["grafo_id"] == grafo_id
    assert "resultado" in data
    assert "tempo_execucao" in data
    
    # Verifica se o resultado contém as centralidades dos vértices
    assert "A" in data["resultado"]
    assert "B" in data["resultado"]
    assert "C" in data["resultado"]


def test_executar_algoritmo_com_parametros_invalidos():
    """Testa a execução de um algoritmo com parâmetros inválidos."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Parâmetros inválidos para o algoritmo (falta a origem)
    params = {
        "parametros": {}
    }
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/dijkstra/{grafo_id}", json=params)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404 or response.status_code == 500


def test_executar_algoritmo_grafo_inexistente():
    """Testa a execução de um algoritmo em um grafo inexistente."""
    # ID de um grafo inexistente
    grafo_id = "grafo_inexistente"
    
    # Parâmetros para o algoritmo
    params = {
        "parametros": {
            "origem": "A"
        }
    }
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/dijkstra/{grafo_id}", json=params)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404
