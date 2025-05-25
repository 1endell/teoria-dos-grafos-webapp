"""
Arquivo de testes para os endpoints de persistência de grafos.
"""

import pytest
import base64
from fastapi.testclient import TestClient
from app.main import create_app
from tests.test_grafos import test_criar_grafo

# Cria o cliente de teste
app = create_app()
client = TestClient(app)


def test_exportar_grafo_graphml():
    """Testa a exportação de um grafo para o formato GraphML."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
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
        assert "<graphml" in conteudo_str
    except:
        pytest.fail("O conteúdo não é uma string base64 válida ou não contém XML GraphML")
    
    # Retorna o conteúdo para uso em outros testes
    return data["conteudo"]


def test_exportar_grafo_json():
    """Testa a exportação de um grafo para o formato JSON."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
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
        assert "{" in conteudo_str and "}" in conteudo_str
    except:
        pytest.fail("O conteúdo não é uma string base64 válida ou não contém JSON")
    
    # Retorna o conteúdo para uso em outros testes
    return data["conteudo"]


def test_exportar_grafo_arquivo():
    """Testa a exportação de um grafo para um arquivo."""
    # Cria um grafo para teste
    grafo_id = test_criar_grafo()
    
    # Faz a requisição para exportar o grafo como arquivo
    response = client.get(f"/api/v1/persistencia/{grafo_id}/exportar/arquivo?formato=graphml")
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se o cabeçalho Content-Disposition está presente
    assert "Content-Disposition" in response.headers
    assert "attachment" in response.headers["Content-Disposition"]
    
    # Verifica se o conteúdo é XML GraphML
    conteudo = response.content.decode('utf-8')
    assert "<graphml" in conteudo


def test_importar_grafo():
    """Testa a importação de um grafo a partir de uma representação."""
    # Exporta um grafo para obter uma representação válida
    conteudo_base64 = test_exportar_grafo_graphml()
    
    # Dados para importar o grafo
    importacao_data = {
        "nome": "Grafo Importado",
        "formato": "graphml",
        "conteudo": conteudo_base64
    }
    
    # Faz a requisição para importar o grafo
    response = client.post("/api/v1/persistencia/importar", json=importacao_data)
    
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    
    # Verifica se a resposta contém os metadados do grafo importado
    data = response.json()
    assert data["nome"] == "Grafo Importado"
    assert "id" in data
    assert "num_vertices" in data
    assert "num_arestas" in data
    
    # Verifica se o grafo foi importado corretamente
    grafo_id = data["id"]
    response = client.get(f"/api/v1/grafos/{grafo_id}")
    assert response.status_code == 200
    
    # Retorna o ID do grafo importado
    return grafo_id


def test_importar_grafo_formato_invalido():
    """Testa a importação de um grafo com formato inválido."""
    # Exporta um grafo para obter uma representação válida
    conteudo_base64 = test_exportar_grafo_graphml()
    
    # Dados para importar o grafo com formato inválido
    importacao_data = {
        "nome": "Grafo Importado Inválido",
        "formato": "formato_invalido",
        "conteudo": conteudo_base64
    }
    
    # Faz a requisição para importar o grafo
    response = client.post("/api/v1/persistencia/importar", json=importacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 400


def test_importar_grafo_conteudo_invalido():
    """Testa a importação de um grafo com conteúdo inválido."""
    # Dados para importar o grafo com conteúdo inválido
    importacao_data = {
        "nome": "Grafo Importado Inválido",
        "formato": "graphml",
        "conteudo": "conteudo_invalido"
    }
    
    # Faz a requisição para importar o grafo
    response = client.post("/api/v1/persistencia/importar", json=importacao_data)
    
    # Verifica se a resposta indica erro
    assert response.status_code == 400 or response.status_code == 500
