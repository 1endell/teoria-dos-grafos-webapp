"""
Arquivo de testes para os endpoints de persistência de grafos.
"""

import pytest
import base64
from app.core.session import get_grafo_service


def test_exportar_grafo_graphml(client, grafo_teste):
    """Testa a exportação de um grafo em formato GraphML."""
    # Usa o grafo criado pela fixture
    grafo_id = grafo_teste
    
    # Faz a requisição para exportar o grafo
    response = client.get(f"/api/v1/persistencia/{grafo_id}/exportar?formato=graphml")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o conteúdo do grafo
    data = response.json()
    assert data["grafo_id"] == grafo_id
    assert data["formato"] == "graphml"
    assert "conteudo" in data
    
    # Verifica se o conteúdo é uma string base64 válida
    try:
        conteudo_bytes = base64.b64decode(data["conteudo"])
        conteudo_str = conteudo_bytes.decode('utf-8')
        assert "<?xml" in conteudo_str
        assert "graphml" in conteudo_str
    except Exception as e:
        assert False, f"Conteúdo base64 inválido: {e}"


def test_exportar_grafo_json(client, grafo_teste):
    """Testa a exportação de um grafo em formato JSON."""
    # Usa o grafo criado pela fixture
    grafo_id = grafo_teste
    
    # Faz a requisição para exportar o grafo
    response = client.get(f"/api/v1/persistencia/{grafo_id}/exportar?formato=json")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o conteúdo do grafo
    data = response.json()
    assert data["grafo_id"] == grafo_id
    assert data["formato"] == "json"
    assert "conteudo" in data
    
    # Verifica se o conteúdo é uma string base64 válida
    try:
        conteudo_bytes = base64.b64decode(data["conteudo"])
        conteudo_str = conteudo_bytes.decode('utf-8')
        assert "{" in conteudo_str
        assert "}" in conteudo_str
    except Exception as e:
        assert False, f"Conteúdo base64 inválido: {e}"


def test_exportar_grafo_arquivo(client, grafo_teste):
    """Testa a exportação de um grafo para arquivo."""
    # Usa o grafo criado pela fixture
    grafo_id = grafo_teste
    
    # Faz a requisição para exportar o grafo
    response = client.get(f"/api/v1/persistencia/{grafo_id}/exportar/arquivo?formato=graphml")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém o arquivo
    assert response.headers["Content-Type"] == "application/octet-stream"
    assert "Content-Disposition" in response.headers
    assert f"grafo_{grafo_id}" in response.headers["Content-Disposition"]
    assert ".graphml" in response.headers["Content-Disposition"]
    assert len(response.content) > 0


def test_importar_grafo(client):
    """Testa a importação de um grafo."""
    # Cria um grafo para teste
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
    
    # Converte para JSON e codifica em base64
    import json
    conteudo_json = json.dumps(grafo_data)
    conteudo_base64 = base64.b64encode(conteudo_json.encode('utf-8')).decode('utf-8')
    
    # Dados para a importação
    importacao_data = {
        "nome": "Grafo Importado",
        "formato": "json",
        "conteudo": conteudo_base64
    }
    
    # Faz a requisição para importar o grafo
    response = client.post("/api/v1/persistencia/importar", json=importacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 201
    
    # Verifica se a resposta contém o ID do grafo importado
    data = response.json()
    assert "id" in data
    assert data["nome"] == "Grafo Importado"
    assert data["num_vertices"] == 3
    assert data["num_arestas"] == 2


def test_importar_grafo_formato_invalido(client):
    """Testa a importação de um grafo com formato inválido."""
    # Dados para a importação com formato inválido
    importacao_data = {
        "nome": "Grafo Inválido",
        "formato": "formato_invalido",
        "conteudo": "conteudo_invalido"
    }
    
    # Faz a requisição para importar o grafo
    response = client.post("/api/v1/persistencia/importar", json=importacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 400
