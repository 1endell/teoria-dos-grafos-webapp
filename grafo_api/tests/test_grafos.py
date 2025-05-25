"""
Arquivo de testes para os endpoints de grafos.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app

# Cria o cliente de teste
app = create_app()
client = TestClient(app)


def test_criar_grafo():
    """Testa a criação de um grafo."""
    # Dados para criar um grafo
    grafo_data = {
        "nome": "Grafo de Teste",
        "direcionado": False,
        "ponderado": True,
        "bipartido": False,
        "vertices": [
            {"id": "A", "atributos": {"cor": "vermelho"}},
            {"id": "B", "atributos": {"cor": "azul"}},
            {"id": "C", "atributos": {"cor": "verde"}}
        ],
        "arestas": [
            {"origem": "A", "destino": "B", "peso": 2.5, "atributos": {"tipo": "amizade"}},
            {"origem": "B", "destino": "C", "peso": 1.8, "atributos": {"tipo": "trabalho"}}
        ]
    }
    
    # Faz a requisição para criar o grafo
    response = client.post("/api/v1/grafos/", json=grafo_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 201
    
    # Verifica se o grafo foi criado corretamente
    data = response.json()
    assert data["nome"] == "Grafo de Teste"
    assert data["direcionado"] == False
    assert data["ponderado"] == True
    assert data["bipartido"] == False
    assert data["num_vertices"] == 3
    assert data["num_arestas"] == 2
    
    # Retorna o ID do grafo criado para uso em outros testes
    return data["id"]


def test_listar_grafos():
    """Testa a listagem de grafos."""
    # Faz a requisição para listar os grafos
    response = client.get("/api/v1/grafos/")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém a lista de grafos
    data = response.json()
    assert "total" in data
    assert "grafos" in data
    assert isinstance(data["grafos"], list)


def test_obter_grafo():
    """Testa a obtenção de um grafo específico."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para obter o grafo
    response = client.get(f"/api/v1/grafos/{grafo_id}")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se o grafo foi obtido corretamente
    data = response.json()
    assert data["id"] == grafo_id
    assert data["nome"] == "Grafo de Teste"
    assert data["direcionado"] == False
    assert data["ponderado"] == True
    assert data["bipartido"] == False
    assert len(data["vertices"]) == 3
    assert len(data["arestas"]) == 2


def test_atualizar_grafo():
    """Testa a atualização de um grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Dados para atualizar o grafo
    grafo_data = {
        "nome": "Grafo Atualizado"
    }
    
    # Faz a requisição para atualizar o grafo
    response = client.put(f"/api/v1/grafos/{grafo_id}", json=grafo_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se o grafo foi atualizado corretamente
    data = response.json()
    assert data["id"] == grafo_id
    assert data["nome"] == "Grafo Atualizado"


def test_adicionar_vertice():
    """Testa a adição de um vértice a um grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Dados para adicionar um vértice
    vertice_data = {
        "id": "D",
        "atributos": {"cor": "amarelo"}
    }
    
    # Faz a requisição para adicionar o vértice
    response = client.post(f"/api/v1/grafos/{grafo_id}/vertices", json=vertice_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se o vértice foi adicionado corretamente
    data = response.json()
    assert data["id"] == "D"
    assert data["atributos"]["cor"] == "amarelo"
    
    # Verifica se o vértice foi adicionado ao grafo
    response = client.get(f"/api/v1/grafos/{grafo_id}")
    data = response.json()
    assert len(data["vertices"]) == 4


def test_adicionar_aresta():
    """Testa a adição de uma aresta a um grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Adiciona um vértice D para teste
    vertice_data = {"id": "D", "atributos": {"cor": "amarelo"}}
    client.post(f"/api/v1/grafos/{grafo_id}/vertices", json=vertice_data)
    
    # Dados para adicionar uma aresta
    aresta_data = {
        "origem": "A",
        "destino": "D",
        "peso": 3.2,
        "atributos": {"tipo": "familiar"}
    }
    
    # Faz a requisição para adicionar a aresta
    response = client.post(f"/api/v1/grafos/{grafo_id}/arestas", json=aresta_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a aresta foi adicionada corretamente
    data = response.json()
    assert data["origem"] == "A"
    assert data["destino"] == "D"
    assert data["peso"] == 3.2
    assert data["atributos"]["tipo"] == "familiar"
    
    # Verifica se a aresta foi adicionada ao grafo
    response = client.get(f"/api/v1/grafos/{grafo_id}")
    data = response.json()
    assert len(data["arestas"]) == 3


def test_remover_vertice():
    """Testa a remoção de um vértice de um grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para remover o vértice
    response = client.delete(f"/api/v1/grafos/{grafo_id}/vertices/C")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 204
    
    # Verifica se o vértice foi removido do grafo
    response = client.get(f"/api/v1/grafos/{grafo_id}")
    data = response.json()
    assert len(data["vertices"]) == 2
    assert all(v["id"] != "C" for v in data["vertices"])
    assert len(data["arestas"]) == 1  # A aresta B-C também deve ter sido removida


def test_remover_aresta():
    """Testa a remoção de uma aresta de um grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para remover a aresta
    response = client.delete(f"/api/v1/grafos/{grafo_id}/arestas/A/B")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 204
    
    # Verifica se a aresta foi removida do grafo
    response = client.get(f"/api/v1/grafos/{grafo_id}")
    data = response.json()
    assert len(data["arestas"]) == 1
    assert all(not (a["origem"] == "A" and a["destino"] == "B") for a in data["arestas"])


def test_excluir_grafo():
    """Testa a exclusão de um grafo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para excluir o grafo
    response = client.delete(f"/api/v1/grafos/{grafo_id}")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 204
    
    # Verifica se o grafo foi excluído
    response = client.get(f"/api/v1/grafos/{grafo_id}")
    assert response.status_code == 404
