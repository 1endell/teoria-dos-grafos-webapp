"""
Arquivo de testes para os endpoints de comparação entre grafos.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from tests.test_grafos import test_criar_grafo
from tests.test_operacoes import criar_segundo_grafo

# Cria o cliente de teste
app = create_app()
client = TestClient(app)


def test_comparar_grafos_isomorfismo():
    """Testa a comparação de isomorfismo entre dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Dados para a comparação
    comparacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "metrica": "isomorfismo"
    }
    
    # Faz a requisição para comparar os grafos
    response = client.post("/api/v1/comparacao/", json=comparacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da comparação
    data = response.json()
    assert data["grafo_id1"] == grafo_id1
    assert data["grafo_id2"] == grafo_id2
    assert data["metrica"] == "isomorfismo"
    assert "resultado" in data
    assert "tempo_execucao" in data
    assert "eh_isomorfo" in data["resultado"]


def test_verificar_isomorfismo_direto():
    """Testa a verificação direta de isomorfismo entre dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Faz a requisição para verificar isomorfismo
    response = client.get(f"/api/v1/comparacao/isomorfismo/{grafo_id1}/{grafo_id2}")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da verificação
    data = response.json()
    assert data["grafo_id1"] == grafo_id1
    assert data["grafo_id2"] == grafo_id2
    assert data["metrica"] == "isomorfismo"
    assert "resultado" in data
    assert "tempo_execucao" in data
    assert "eh_isomorfo" in data["resultado"]


def test_calcular_similaridade():
    """Testa o cálculo de similaridade entre dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Faz a requisição para calcular similaridade
    response = client.get(f"/api/v1/comparacao/similaridade/{grafo_id1}/{grafo_id2}?metrica=espectral")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado do cálculo
    data = response.json()
    assert data["grafo_id1"] == grafo_id1
    assert data["grafo_id2"] == grafo_id2
    assert data["metrica"] == "similaridade_espectral"
    assert "resultado" in data
    assert "tempo_execucao" in data
    assert "similaridade" in data["resultado"]


def test_verificar_subgrafo():
    """Testa a verificação de subgrafo entre dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Faz a requisição para verificar subgrafo
    response = client.get(f"/api/v1/comparacao/subgrafo/{grafo_id1}/{grafo_id2}")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da verificação
    data = response.json()
    assert data["grafo_id1"] == grafo_id1
    assert data["grafo_id2"] == grafo_id2
    assert data["metrica"] == "subgrafo"
    assert "resultado" in data
    assert "tempo_execucao" in data
    assert "eh_subgrafo" in data["resultado"]


def test_comparar_grafos_com_grafo_inexistente():
    """Testa a comparação com um grafo inexistente."""
    # Cria um grafo para teste
    grafo_id1 = test_criar_grafo()
    
    # ID de um grafo inexistente
    grafo_id2 = "grafo_inexistente"
    
    # Dados para a comparação
    comparacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "metrica": "isomorfismo"
    }
    
    # Faz a requisição para comparar os grafos
    response = client.post("/api/v1/comparacao/", json=comparacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404


def test_comparar_grafos_metrica_invalida():
    """Testa a comparação com uma métrica inválida."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Dados para a comparação com métrica inválida
    comparacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "metrica": "metrica_invalida"
    }
    
    # Faz a requisição para comparar os grafos
    response = client.post("/api/v1/comparacao/", json=comparacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404 or response.status_code == 500
