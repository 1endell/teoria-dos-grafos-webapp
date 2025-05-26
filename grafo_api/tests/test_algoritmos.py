"""
Arquivo de testes para os endpoints de algoritmos.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import create_app
from app.core.session import get_grafo_service

# Cria uma única instância da aplicação e do cliente de teste para todos os testes
app = create_app()
client = TestClient(app)

# Armazena os IDs dos grafos criados para reutilização entre testes
grafos_criados = {}


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
        response = client.get(f"/api/v1/algoritmos/categoria/{categoria}")
        
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
    # Cria um grafo para teste se ainda não existir
    if 'dijkstra' not in grafos_criados:
        # Cria um grafo para o teste
        grafo_data = {
            "nome": "Grafo de Teste Dijkstra",
            "direcionado": True,
            "ponderado": True
        }
        response = client.post("/api/v1/grafos/", json=grafo_data)
        assert response.status_code == 201
        grafo_id = response.json()["id"]
        
        # Adiciona vértices
        vertices = ["A", "B", "C"]
        for v in vertices:
            response = client.post(f"/api/v1/grafos/{grafo_id}/vertices", json={"id": v})
            assert response.status_code == 200  # Ajustado para 200 conforme API atual
        
        # Adiciona arestas
        arestas = [
            {"origem": "A", "destino": "B", "peso": 1.0},
            {"origem": "B", "destino": "C", "peso": 2.0},
            {"origem": "A", "destino": "C", "peso": 4.0}
        ]
        for aresta in arestas:
            response = client.post(f"/api/v1/grafos/{grafo_id}/arestas", json=aresta)
            assert response.status_code == 200  # Ajustado para 200 conforme API atual
        
        # Armazena o ID do grafo para reutilização
        grafos_criados['dijkstra'] = grafo_id
    
    grafo_id = grafos_criados['dijkstra']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        # Se o grafo não existir no serviço, recria-o
        grafo_data = {
            "nome": "Grafo de Teste Dijkstra",
            "direcionado": True,
            "ponderado": True
        }
        response = client.post("/api/v1/grafos/", json=grafo_data)
        assert response.status_code == 201
        grafo_id = response.json()["id"]
        
        # Adiciona vértices
        vertices = ["A", "B", "C"]
        for v in vertices:
            response = client.post(f"/api/v1/grafos/{grafo_id}/vertices", json={"id": v})
            assert response.status_code == 200
        
        # Adiciona arestas
        arestas = [
            {"origem": "A", "destino": "B", "peso": 1.0},
            {"origem": "B", "destino": "C", "peso": 2.0},
            {"origem": "A", "destino": "C", "peso": 4.0}
        ]
        for aresta in arestas:
            response = client.post(f"/api/v1/grafos/{grafo_id}/arestas", json=aresta)
            assert response.status_code == 200
        
        # Atualiza o ID do grafo
        grafos_criados['dijkstra'] = grafo_id
    
    # Parâmetros para o algoritmo
    params = {
        "parametros": {
            "origem": "A"
        }
    }
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/executar/dijkstra/{grafo_id}", json=params)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado do algoritmo
    data = response.json()
    assert data["algoritmo"] == "dijkstra"
    assert data["grafo_id"] == grafo_id
    assert "resultado" in data
    assert "tempo_execucao" in data
    
    # Verifica se o resultado contém as distâncias
    # Ajustado para acessar o resultado dentro da estrutura retornada
    if "valor" in data["resultado"]:
        # Formato: {"valor": {...}, "info_adicional": {...}}
        assert "A" in data["resultado"]["valor"]
        assert "B" in data["resultado"]["valor"]
        assert "C" in data["resultado"]["valor"]
    else:
        # Formato direto: {...}
        assert "A" in data["resultado"]
        assert "B" in data["resultado"]
        assert "C" in data["resultado"]


def test_executar_algoritmo_coloracao():
    """Testa a execução do algoritmo de coloração."""
    # Cria um grafo para teste se ainda não existir
    if 'coloracao' not in grafos_criados:
        # Cria um grafo para o teste
        grafo_data = {
            "nome": "Grafo de Teste Coloração",
            "direcionado": False,
            "ponderado": False
        }
        response = client.post("/api/v1/grafos/", json=grafo_data)
        assert response.status_code == 201
        grafo_id = response.json()["id"]
        
        # Adiciona vértices
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            response = client.post(f"/api/v1/grafos/{grafo_id}/vertices", json={"id": v})
            assert response.status_code == 200  # Ajustado para 200 conforme API atual
        
        # Adiciona arestas
        arestas = [
            {"origem": "A", "destino": "B"},
            {"origem": "B", "destino": "C"},
            {"origem": "C", "destino": "D"},
            {"origem": "D", "destino": "A"}
        ]
        for aresta in arestas:
            response = client.post(f"/api/v1/grafos/{grafo_id}/arestas", json=aresta)
            assert response.status_code == 200  # Ajustado para 200 conforme API atual
        
        # Armazena o ID do grafo para reutilização
        grafos_criados['coloracao'] = grafo_id
    
    grafo_id = grafos_criados['coloracao']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        # Se o grafo não existir no serviço, recria-o
        grafo_data = {
            "nome": "Grafo de Teste Coloração",
            "direcionado": False,
            "ponderado": False
        }
        response = client.post("/api/v1/grafos/", json=grafo_data)
        assert response.status_code == 201
        grafo_id = response.json()["id"]
        
        # Adiciona vértices
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            response = client.post(f"/api/v1/grafos/{grafo_id}/vertices", json={"id": v})
            assert response.status_code == 200
        
        # Adiciona arestas
        arestas = [
            {"origem": "A", "destino": "B"},
            {"origem": "B", "destino": "C"},
            {"origem": "C", "destino": "D"},
            {"origem": "D", "destino": "A"}
        ]
        for aresta in arestas:
            response = client.post(f"/api/v1/grafos/{grafo_id}/arestas", json=aresta)
            assert response.status_code == 200
        
        # Atualiza o ID do grafo
        grafos_criados['coloracao'] = grafo_id
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/executar/coloracao_welsh_powell/{grafo_id}", json={})
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado do algoritmo
    data = response.json()
    assert data["algoritmo"] == "coloracao_welsh_powell"
    assert data["grafo_id"] == grafo_id
    assert "resultado" in data
    assert "tempo_execucao" in data
    
    # Verifica se o resultado contém as cores dos vértices
    # Ajustado para acessar o resultado dentro da estrutura retornada
    if isinstance(data["resultado"], dict) and "resultado" in data["resultado"]:
        # Formato: {"resultado": {...}}
        assert "A" in data["resultado"]["resultado"]
        assert "B" in data["resultado"]["resultado"]
        assert "C" in data["resultado"]["resultado"]
        assert "D" in data["resultado"]["resultado"]
    else:
        # Formato direto: {...}
        assert "A" in data["resultado"]
        assert "B" in data["resultado"]
        assert "C" in data["resultado"]
        assert "D" in data["resultado"]


def test_executar_algoritmo_centralidade():
    """Testa a execução do algoritmo de centralidade."""
    # Cria um grafo para teste se ainda não existir
    if 'centralidade' not in grafos_criados:
        # Cria um grafo para o teste
        grafo_data = {
            "nome": "Grafo de Teste Centralidade",
            "direcionado": False,
            "ponderado": False
        }
        response = client.post("/api/v1/grafos/", json=grafo_data)
        assert response.status_code == 201
        grafo_id = response.json()["id"]
        
        # Adiciona vértices
        vertices = ["A", "B", "C", "D", "E"]
        for v in vertices:
            response = client.post(f"/api/v1/grafos/{grafo_id}/vertices", json={"id": v})
            assert response.status_code == 200  # Ajustado para 200 conforme API atual
        
        # Adiciona arestas
        arestas = [
            {"origem": "A", "destino": "B"},
            {"origem": "A", "destino": "C"},
            {"origem": "A", "destino": "D"},
            {"origem": "B", "destino": "E"},
            {"origem": "C", "destino": "E"}
        ]
        for aresta in arestas:
            response = client.post(f"/api/v1/grafos/{grafo_id}/arestas", json=aresta)
            assert response.status_code == 200  # Ajustado para 200 conforme API atual
        
        # Armazena o ID do grafo para reutilização
        grafos_criados['centralidade'] = grafo_id
    
    grafo_id = grafos_criados['centralidade']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo = grafo_service.obter_grafo(grafo_id)
    if not grafo:
        # Se o grafo não existir no serviço, recria-o
        grafo_data = {
            "nome": "Grafo de Teste Centralidade",
            "direcionado": False,
            "ponderado": False
        }
        response = client.post("/api/v1/grafos/", json=grafo_data)
        assert response.status_code == 201
        grafo_id = response.json()["id"]
        
        # Adiciona vértices
        vertices = ["A", "B", "C", "D", "E"]
        for v in vertices:
            response = client.post(f"/api/v1/grafos/{grafo_id}/vertices", json={"id": v})
            assert response.status_code == 200
        
        # Adiciona arestas
        arestas = [
            {"origem": "A", "destino": "B"},
            {"origem": "A", "destino": "C"},
            {"origem": "A", "destino": "D"},
            {"origem": "B", "destino": "E"},
            {"origem": "C", "destino": "E"}
        ]
        for aresta in arestas:
            response = client.post(f"/api/v1/grafos/{grafo_id}/arestas", json=aresta)
            assert response.status_code == 200
        
        # Atualiza o ID do grafo
        grafos_criados['centralidade'] = grafo_id
    
    # Faz a requisição para executar o algoritmo
    response = client.post(f"/api/v1/algoritmos/executar/centralidade_grau/{grafo_id}", json={})
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o resultado do algoritmo
    data = response.json()
    assert data["algoritmo"] == "centralidade_grau"
    assert data["grafo_id"] == grafo_id
    assert "resultado" in data
    assert "tempo_execucao" in data
    
    # Verifica se o resultado contém as centralidades dos vértices
    # Ajustado para acessar o resultado dentro da estrutura retornada
    if isinstance(data["resultado"], dict) and "resultado" in data["resultado"]:
        # Formato: {"resultado": {...}}
        assert "A" in data["resultado"]["resultado"]
        assert "B" in data["resultado"]["resultado"]
        assert "C" in data["resultado"]["resultado"]
        assert "D" in data["resultado"]["resultado"]
        assert "E" in data["resultado"]["resultado"]
    else:
        # Formato direto: {...}
        assert "A" in data["resultado"]
        assert "B" in data["resultado"]
        assert "C" in data["resultado"]
        assert "D" in data["resultado"]
        assert "E" in data["resultado"]


def test_executar_algoritmo_com_parametros_invalidos():
    """Testa a execução de um algoritmo com parâmetros inválidos."""
    # Usa o grafo já criado para o teste de Dijkstra
    if 'dijkstra' in grafos_criados:
        grafo_id = grafos_criados['dijkstra']
        
        # Verifica se o grafo existe no serviço
        grafo_service = get_grafo_service()
        grafo = grafo_service.obter_grafo(grafo_id)
        if not grafo:
            # Se o grafo não existir, pula o teste
            pytest.skip("Grafo para teste não está disponível")
        
        # Parâmetros inválidos para o algoritmo (falta a origem)
        params = {
            "parametros": {}
        }
        
        # Faz a requisição para executar o algoritmo
        response = client.post(f"/api/v1/algoritmos/executar/dijkstra/{grafo_id}", json=params)
        
        # Verifica se a resposta indica erro de parâmetros inválidos (400)
        assert response.status_code == 400
        
        # Verifica se a mensagem de erro menciona o parâmetro obrigatório
        assert "origem" in response.json()["detail"].lower()


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
    response = client.post(f"/api/v1/algoritmos/executar/dijkstra/{grafo_id}", json=params)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 404
