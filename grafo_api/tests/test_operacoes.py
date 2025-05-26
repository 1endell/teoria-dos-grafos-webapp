"""
Arquivo de testes para os endpoints de operações entre grafos.
"""

import pytest
from app.core.session import get_grafo_service

# Armazena os IDs dos grafos criados para reutilização entre testes
grafos_criados = {}


def criar_segundo_grafo(client):
    """Cria um segundo grafo para testes de operações."""
    # Verifica se já existe um grafo criado para reutilização
    if 'segundo_grafo' in grafos_criados:
        grafo_id = grafos_criados['segundo_grafo']
        
        # Verifica se o grafo existe no serviço
        grafo_service = get_grafo_service()
        grafo = grafo_service.obter_grafo(grafo_id)
        if grafo:
            return grafo_id
    
    # Dados para criar um grafo
    grafo_data = {
        "nome": "Grafo de Teste 2",
        "direcionado": False,
        "ponderado": True,
        "bipartido": False
    }
    
    # Faz a requisição para criar o grafo
    response = client.post("/api/v1/grafos/", json=grafo_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 201
    
    # Armazena o ID do grafo criado para reutilização
    grafo_id = response.json()["id"]
    grafos_criados['segundo_grafo'] = grafo_id
    
    # Adiciona vértices e arestas ao grafo
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "C", "atributos": {"cor": "verde"}})
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "D", "atributos": {"cor": "amarelo"}})
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "E", "atributos": {"cor": "roxo"}})
    
    client.post(f"/api/v1/grafos/{grafo_id}/arestas/", json={"origem": "C", "destino": "D", "peso": 1.5, "atributos": {"tipo": "amizade"}})
    client.post(f"/api/v1/grafos/{grafo_id}/arestas/", json={"origem": "D", "destino": "E", "peso": 2.0, "atributos": {"tipo": "trabalho"}})
    
    return grafo_id


def criar_primeiro_grafo(client):
    """Cria um primeiro grafo para testes de operações."""
    # Dados para criar um grafo
    grafo_data = {
        "nome": "Grafo de Teste 1",
        "direcionado": False,
        "ponderado": True,
        "bipartido": False
    }
    
    # Faz a requisição para criar o grafo
    response = client.post("/api/v1/grafos/", json=grafo_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 201
    
    # Armazena o ID do grafo criado para reutilização
    grafo_id = response.json()["id"]
    grafos_criados['primeiro_grafo'] = grafo_id
    
    # Adiciona vértices e arestas ao grafo
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "A", "atributos": {"cor": "azul"}})
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "B", "atributos": {"cor": "vermelho"}})
    client.post(f"/api/v1/grafos/{grafo_id}/vertices/", json={"id": "C", "atributos": {"cor": "verde"}})
    
    client.post(f"/api/v1/grafos/{grafo_id}/arestas/", json={"origem": "A", "destino": "B", "peso": 1.5, "atributos": {"tipo": "amizade"}})
    client.post(f"/api/v1/grafos/{grafo_id}/arestas/", json={"origem": "B", "destino": "C", "peso": 2.0, "atributos": {"tipo": "trabalho"}})
    
    return grafo_id


def test_uniao_grafos(client):
    """Testa a união de dois grafos."""
    # Cria dois grafos para teste
    if 'primeiro_grafo' not in grafos_criados:
        grafo_id1 = criar_primeiro_grafo(client)
    else:
        grafo_id1 = grafos_criados['primeiro_grafo']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    if not grafo1:
        # Se o grafo não existir, cria um novo
        grafo_id1 = criar_primeiro_grafo(client)
    
    grafo_id2 = criar_segundo_grafo(client)
    
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
    
    # Armazena o ID do grafo resultante para reutilização
    grafos_criados['uniao'] = data["id"]


def test_intersecao_grafos(client):
    """Testa a interseção de dois grafos."""
    # Cria dois grafos para teste
    if 'primeiro_grafo' not in grafos_criados:
        grafo_id1 = criar_primeiro_grafo(client)
    else:
        grafo_id1 = grafos_criados['primeiro_grafo']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    if not grafo1:
        # Se o grafo não existir, cria um novo
        grafo_id1 = criar_primeiro_grafo(client)
    
    grafo_id2 = criar_segundo_grafo(client)
    
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
    
    # Armazena o ID do grafo resultante para reutilização
    grafos_criados['intersecao'] = data["id"]


def test_diferenca_grafos(client):
    """Testa a diferença entre dois grafos."""
    # Cria dois grafos para teste
    if 'primeiro_grafo' not in grafos_criados:
        grafo_id1 = criar_primeiro_grafo(client)
    else:
        grafo_id1 = grafos_criados['primeiro_grafo']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    if not grafo1:
        # Se o grafo não existir, cria um novo
        grafo_id1 = criar_primeiro_grafo(client)
    
    grafo_id2 = criar_segundo_grafo(client)
    
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
    
    # Armazena o ID do grafo resultante para reutilização
    grafos_criados['diferenca'] = data["id"]


def test_diferenca_simetrica_grafos(client):
    """Testa a diferença simétrica entre dois grafos."""
    # Cria dois grafos para teste
    if 'primeiro_grafo' not in grafos_criados:
        grafo_id1 = criar_primeiro_grafo(client)
    else:
        grafo_id1 = grafos_criados['primeiro_grafo']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    if not grafo1:
        # Se o grafo não existir, cria um novo
        grafo_id1 = criar_primeiro_grafo(client)
    
    grafo_id2 = criar_segundo_grafo(client)
    
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
    
    # Armazena o ID do grafo resultante para reutilização
    grafos_criados['diferenca_simetrica'] = data["id"]


def test_composicao_grafos(client):
    """Testa a composição de dois grafos."""
    # Cria dois grafos para teste
    if 'primeiro_grafo' not in grafos_criados:
        grafo_id1 = criar_primeiro_grafo(client)
    else:
        grafo_id1 = grafos_criados['primeiro_grafo']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    if not grafo1:
        # Se o grafo não existir, cria um novo
        grafo_id1 = criar_primeiro_grafo(client)
    
    grafo_id2 = criar_segundo_grafo(client)
    
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
    
    # Armazena o ID do grafo resultante para reutilização
    grafos_criados['composicao'] = data["id"]


def test_operacao_com_grafo_inexistente(client):
    """Testa uma operação com um grafo inexistente."""
    # Cria um grafo para teste
    if 'primeiro_grafo' not in grafos_criados:
        grafo_id1 = criar_primeiro_grafo(client)
    else:
        grafo_id1 = grafos_criados['primeiro_grafo']
    
    # Verifica se o grafo existe no serviço
    grafo_service = get_grafo_service()
    grafo1 = grafo_service.obter_grafo(grafo_id1)
    if not grafo1:
        # Se o grafo não existir, cria um novo
        grafo_id1 = criar_primeiro_grafo(client)
    
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
