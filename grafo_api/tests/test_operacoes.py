"""
Arquivo de testes para os endpoints de operações entre grafos.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from tests.test_grafos import test_criar_grafo

# Cria o cliente de teste
app = create_app()
client = TestClient(app)


def criar_segundo_grafo():
    """Cria um segundo grafo para testes de operações."""
    # Dados para criar um grafo
    grafo_data = {
        "nome": "Grafo de Teste 2",
        "direcionado": False,
        "ponderado": True,
        "bipartido": False,
        "vertices": [
            {"id": "C", "atributos": {"cor": "verde"}},
            {"id": "D", "atributos": {"cor": "amarelo"}},
            {"id": "E", "atributos": {"cor": "roxo"}}
        ],
        "arestas": [
            {"origem": "C", "destino": "D", "peso": 1.5, "atributos": {"tipo": "amizade"}},
            {"origem": "D", "destino": "E", "peso": 2.0, "atributos": {"tipo": "trabalho"}}
        ]
    }
    
    # Faz a requisição para criar o grafo
    response = client.post("/api/v1/grafos/", json=grafo_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 201
    
    # Retorna o ID do grafo criado
    return response.json()["id"]


def test_uniao_grafos():
    """Testa a união de dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Dados para a operação
    operacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "nome_resultado": "União de Teste"
    }
    
    # Faz a requisição para realizar a união
    response = client.post("/api/v1/operacoes/uniao", json=operacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da operação
    data = response.json()
    assert data["nome"] == "União de Teste"
    assert data["num_vertices"] >= 5  # A + B + C + D + E (C está em ambos)
    assert data["num_arestas"] >= 4  # A-B + B-C + C-D + D-E
    
    # Retorna o ID do grafo resultante
    return data["id"]


def test_intersecao_grafos():
    """Testa a interseção de dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Dados para a operação
    operacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "nome_resultado": "Interseção de Teste"
    }
    
    # Faz a requisição para realizar a interseção
    response = client.post("/api/v1/operacoes/intersecao", json=operacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da operação
    data = response.json()
    assert data["nome"] == "Interseção de Teste"
    
    # Retorna o ID do grafo resultante
    return data["id"]


def test_diferenca_grafos():
    """Testa a diferença entre dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Dados para a operação
    operacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "nome_resultado": "Diferença de Teste"
    }
    
    # Faz a requisição para realizar a diferença
    response = client.post("/api/v1/operacoes/diferenca", json=operacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da operação
    data = response.json()
    assert data["nome"] == "Diferença de Teste"
    
    # Retorna o ID do grafo resultante
    return data["id"]


def test_diferenca_simetrica_grafos():
    """Testa a diferença simétrica entre dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Dados para a operação
    operacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "nome_resultado": "Diferença Simétrica de Teste"
    }
    
    # Faz a requisição para realizar a diferença simétrica
    response = client.post("/api/v1/operacoes/diferenca-simetrica", json=operacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da operação
    data = response.json()
    assert data["nome"] == "Diferença Simétrica de Teste"
    
    # Retorna o ID do grafo resultante
    return data["id"]


def test_composicao_grafos():
    """Testa a composição de dois grafos."""
    # Cria dois grafos para teste
    grafo_id1 = test_criar_grafo()
    grafo_id2 = criar_segundo_grafo()
    
    # Dados para a operação
    operacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "nome_resultado": "Composição de Teste"
    }
    
    # Faz a requisição para realizar a composição
    response = client.post("/api/v1/operacoes/composicao", json=operacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado da operação
    data = response.json()
    assert data["nome"] == "Composição de Teste"
    
    # Retorna o ID do grafo resultante
    return data["id"]


def test_operacao_com_grafo_inexistente():
    """Testa uma operação com um grafo inexistente."""
    # Cria um grafo para teste
    grafo_id1 = test_criar_grafo()
    
    # ID de um grafo inexistente
    grafo_id2 = "grafo_inexistente"
    
    # Dados para a operação
    operacao_data = {
        "grafo_id1": grafo_id1,
        "grafo_id2": grafo_id2,
        "nome_resultado": "Operação Inválida"
    }
    
    # Faz a requisição para realizar a união
    response = client.post("/api/v1/operacoes/uniao", json=operacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404
