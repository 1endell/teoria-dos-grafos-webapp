"""
Arquivo de testes para os endpoints de comparação entre grafos.
"""

import pytest
from app.core.session import get_grafo_service

def test_comparar_grafos_isomorfismo(client, grafos_operacoes):
    """Testa a comparação de isomorfismo entre dois grafos."""
    # Usa os grafos criados pela fixture
    grafo_id1 = grafos_operacoes["grafo_id1"]
    grafo_id2 = grafos_operacoes["grafo_id2"]
    
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


def test_verificar_isomorfismo_direto(client, grafos_operacoes):
    """Testa a verificação direta de isomorfismo entre dois grafos."""
    # Usa os grafos criados pela fixture
    grafo_id1 = grafos_operacoes["grafo_id1"]
    grafo_id2 = grafos_operacoes["grafo_id2"]
    
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


def test_calcular_similaridade(client, grafos_operacoes):
    """Testa o cálculo de similaridade entre dois grafos."""
    # Usa os grafos criados pela fixture
    grafo_id1 = grafos_operacoes["grafo_id1"]
    grafo_id2 = grafos_operacoes["grafo_id2"]
    
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


def test_verificar_subgrafo(client, grafos_operacoes):
    """Testa a verificação de subgrafo entre dois grafos."""
    # Usa os grafos criados pela fixture
    grafo_id1 = grafos_operacoes["grafo_id1"]
    grafo_id2 = grafos_operacoes["grafo_id2"]
    
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


def test_comparar_grafos_com_grafo_inexistente(client, grafo_teste):
    """Testa a comparação com um grafo inexistente."""
    # Usa o grafo criado pela fixture
    grafo_id1 = grafo_teste
    
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


def test_comparar_grafos_metrica_invalida(client, grafos_operacoes):
    """Testa a comparação com uma métrica inválida."""
    # Usa os grafos criados pela fixture
    grafo_id1 = grafos_operacoes["grafo_id1"]
    grafo_id2 = grafos_operacoes["grafo_id2"]
    
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
