# Documentação da API de Teoria dos Grafos

## Visão Geral

Esta API fornece uma interface RESTful para trabalhar com grafos e algoritmos de teoria dos grafos. A API permite criar, manipular, analisar e visualizar grafos, além de executar diversos algoritmos clássicos e avançados.

## Recursos Principais

- **Gerenciamento de Grafos**: Criar, editar, excluir e consultar grafos
- **Algoritmos Clássicos**: Dijkstra, Kruskal, Ford-Fulkerson e outros
- **Algoritmos Avançados**: Coloração, emparelhamento, planaridade, análise espectral
- **Operações entre Grafos**: União, interseção, diferença, composição
- **Persistência**: Importação e exportação em diversos formatos (GraphML, GML, GEXF, JSON, CSV)
- **Comparação**: Isomorfismo, similaridade, verificação de subgrafos
- **Visualização**: Geração de dados para visualização e imagens de grafos

## Instalação e Execução

### Requisitos

- Python 3.8+
- NetworkX
- FastAPI
- Uvicorn
- Matplotlib
- SciPy
- NumPy

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/grafo-api.git
cd grafo-api
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Execução

Execute o servidor com:

```bash
python run.py
```

O servidor estará disponível em `http://localhost:8000`.

## Documentação Interativa

A documentação interativa da API está disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Exemplos de Uso

### Criar um Grafo

```python
import requests
import json

# URL base da API
base_url = "http://localhost:8000/api/v1"

# Dados para criar um grafo
grafo_data = {
    "nome": "Meu Grafo",
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
response = requests.post(f"{base_url}/grafos/", json=grafo_data)

# Obtém o ID do grafo criado
grafo_id = response.json()["id"]
print(f"Grafo criado com ID: {grafo_id}")
```

### Executar um Algoritmo

```python
# Parâmetros para o algoritmo de Dijkstra
params = {
    "parametros": {
        "origem": "A"
    }
}

# Faz a requisição para executar o algoritmo
response = requests.post(f"{base_url}/algoritmos/dijkstra/{grafo_id}", json=params)

# Obtém o resultado
resultado = response.json()
print("Distâncias mais curtas:")
print(json.dumps(resultado["resultado"], indent=2))
```

### Exportar um Grafo

```python
# Faz a requisição para exportar o grafo em formato GraphML
response = requests.get(f"{base_url}/persistencia/{grafo_id}/exportar?formato=graphml")

# Obtém o conteúdo do grafo em base64
conteudo_base64 = response.json()["conteudo"]

# Decodifica o conteúdo
import base64
conteudo_bytes = base64.b64decode(conteudo_base64)
conteudo_str = conteudo_bytes.decode('utf-8')

# Salva o conteúdo em um arquivo
with open("meu_grafo.graphml", "w") as f:
    f.write(conteudo_str)

print("Grafo exportado para meu_grafo.graphml")
```

### Visualizar um Grafo

```python
# Faz a requisição para obter dados de visualização
response = requests.get(f"{base_url}/visualizacao/{grafo_id}?layout=spring&incluir_atributos=true")

# Obtém os dados de visualização
dados_visualizacao = response.json()

# Exemplo de como usar os dados com uma biblioteca de visualização JavaScript
print("Vértices:", len(dados_visualizacao["vertices"]))
print("Arestas:", len(dados_visualizacao["arestas"]))

# Para obter uma imagem do grafo
response = requests.get(f"{base_url}/visualizacao/{grafo_id}/imagem?formato=png", stream=True)
with open("meu_grafo.png", "wb") as f:
    for chunk in response.iter_content(chunk_size=1024):
        f.write(chunk)

print("Imagem do grafo salva em meu_grafo.png")
```

## Integração com Frontend

A API foi projetada para ser facilmente integrada com aplicações frontend. Aqui está um exemplo básico de como integrar com uma aplicação React:

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

function GrafoApp() {
  const [grafos, setGrafos] = useState([]);
  const [grafoSelecionado, setGrafoSelecionado] = useState(null);
  const [dadosVisualizacao, setDadosVisualizacao] = useState(null);

  // Carrega a lista de grafos
  useEffect(() => {
    axios.get(`${API_URL}/grafos/`)
      .then(response => {
        setGrafos(response.data.grafos);
      })
      .catch(error => console.error('Erro ao carregar grafos:', error));
  }, []);

  // Carrega os dados de visualização quando um grafo é selecionado
  useEffect(() => {
    if (grafoSelecionado) {
      axios.get(`${API_URL}/visualizacao/${grafoSelecionado.id}?layout=spring`)
        .then(response => {
          setDadosVisualizacao(response.data);
        })
        .catch(error => console.error('Erro ao carregar visualização:', error));
    }
  }, [grafoSelecionado]);

  // Renderiza o grafo (exemplo simplificado)
  const renderizarGrafo = () => {
    if (!dadosVisualizacao) return null;
    
    return (
      <svg width="800" height="600">
        {/* Renderiza as arestas */}
        {dadosVisualizacao.arestas.map((aresta, index) => {
          const origem = dadosVisualizacao.vertices.find(v => v.id === aresta.origem);
          const destino = dadosVisualizacao.vertices.find(v => v.id === aresta.destino);
          
          return (
            <line
              key={`aresta-${index}`}
              x1={origem.x * 400 + 400}
              y1={origem.y * 300 + 300}
              x2={destino.x * 400 + 400}
              y2={destino.y * 300 + 300}
              stroke="gray"
              strokeWidth="2"
            />
          );
        })}
        
        {/* Renderiza os vértices */}
        {dadosVisualizacao.vertices.map(vertice => (
          <g key={`vertice-${vertice.id}`}>
            <circle
              cx={vertice.x * 400 + 400}
              cy={vertice.y * 300 + 300}
              r="20"
              fill="skyblue"
              stroke="navy"
              strokeWidth="2"
            />
            <text
              x={vertice.x * 400 + 400}
              y={vertice.y * 300 + 300}
              textAnchor="middle"
              dominantBaseline="middle"
              fill="black"
              fontWeight="bold"
            >
              {vertice.id}
            </text>
          </g>
        ))}
      </svg>
    );
  };

  return (
    <div>
      <h1>Aplicação de Teoria dos Grafos</h1>
      
      <div>
        <h2>Grafos Disponíveis</h2>
        <ul>
          {grafos.map(grafo => (
            <li key={grafo.id}>
              <button onClick={() => setGrafoSelecionado(grafo)}>
                {grafo.nome} ({grafo.num_vertices} vértices, {grafo.num_arestas} arestas)
              </button>
            </li>
          ))}
        </ul>
      </div>
      
      {grafoSelecionado && (
        <div>
          <h2>Grafo: {grafoSelecionado.nome}</h2>
          {renderizarGrafo()}
        </div>
      )}
    </div>
  );
}

export default GrafoApp;
```

## Referência da API

### Endpoints de Grafos

- `GET /api/v1/grafos/`: Lista todos os grafos
- `POST /api/v1/grafos/`: Cria um novo grafo
- `GET /api/v1/grafos/{grafo_id}`: Obtém um grafo específico
- `PUT /api/v1/grafos/{grafo_id}`: Atualiza um grafo
- `DELETE /api/v1/grafos/{grafo_id}`: Exclui um grafo
- `POST /api/v1/grafos/{grafo_id}/vertices`: Adiciona um vértice
- `GET /api/v1/grafos/{grafo_id}/vertices/{vertice_id}`: Obtém um vértice
- `PUT /api/v1/grafos/{grafo_id}/vertices/{vertice_id}`: Atualiza um vértice
- `DELETE /api/v1/grafos/{grafo_id}/vertices/{vertice_id}`: Remove um vértice
- `POST /api/v1/grafos/{grafo_id}/arestas`: Adiciona uma aresta
- `GET /api/v1/grafos/{grafo_id}/arestas/{origem}/{destino}`: Obtém uma aresta
- `PUT /api/v1/grafos/{grafo_id}/arestas/{origem}/{destino}`: Atualiza uma aresta
- `DELETE /api/v1/grafos/{grafo_id}/arestas/{origem}/{destino}`: Remove uma aresta

### Endpoints de Algoritmos

- `GET /api/v1/algoritmos/`: Lista todos os algoritmos disponíveis
- `GET /api/v1/algoritmos/{categoria}`: Lista algoritmos de uma categoria
- `POST /api/v1/algoritmos/{algoritmo_id}/{grafo_id}`: Executa um algoritmo em um grafo

### Endpoints de Operações

- `POST /api/v1/operacoes/uniao`: Realiza a união de dois grafos
- `POST /api/v1/operacoes/intersecao`: Realiza a interseção de dois grafos
- `POST /api/v1/operacoes/diferenca`: Realiza a diferença entre dois grafos
- `POST /api/v1/operacoes/diferenca-simetrica`: Realiza a diferença simétrica entre dois grafos
- `POST /api/v1/operacoes/composicao`: Realiza a composição de dois grafos

### Endpoints de Persistência

- `POST /api/v1/persistencia/importar`: Importa um grafo a partir de uma representação
- `POST /api/v1/persistencia/importar/arquivo`: Importa um grafo a partir de um arquivo
- `GET /api/v1/persistencia/{grafo_id}/exportar`: Exporta um grafo para um formato específico
- `GET /api/v1/persistencia/{grafo_id}/exportar/arquivo`: Exporta um grafo para um arquivo

### Endpoints de Comparação

- `POST /api/v1/comparacao/`: Compara dois grafos usando uma métrica específica
- `GET /api/v1/comparacao/isomorfismo/{grafo_id1}/{grafo_id2}`: Verifica se dois grafos são isomorfos
- `GET /api/v1/comparacao/similaridade/{grafo_id1}/{grafo_id2}`: Calcula a similaridade entre dois grafos
- `GET /api/v1/comparacao/subgrafo/{grafo_id1}/{grafo_id2}`: Verifica se o primeiro grafo é subgrafo do segundo

### Endpoints de Visualização

- `POST /api/v1/visualizacao/`: Gera dados para visualização de um grafo
- `GET /api/v1/visualizacao/{grafo_id}`: Gera dados para visualização de um grafo pelo ID
- `GET /api/v1/visualizacao/layouts`: Lista os layouts de visualização disponíveis
- `GET /api/v1/visualizacao/{grafo_id}/imagem`: Gera uma imagem de visualização do grafo

## Considerações de Segurança

- A API não implementa autenticação ou autorização. Em um ambiente de produção, recomenda-se adicionar um sistema de autenticação.
- Para uso em produção, considere adicionar rate limiting para evitar sobrecarga do servidor.
- Os grafos são armazenados em memória. Para persistência de longo prazo, considere implementar um sistema de armazenamento em banco de dados.

## Limitações Conhecidas

- O desempenho pode ser afetado ao trabalhar com grafos muito grandes.
- Alguns algoritmos avançados podem ter tempo de execução exponencial para certos tipos de grafos.
- A visualização de grafos muito grandes pode ser lenta ou difícil de interpretar.

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests ou abrir issues para reportar bugs ou sugerir melhorias.

## Licença

Este projeto está licenciado sob a licença MIT.
