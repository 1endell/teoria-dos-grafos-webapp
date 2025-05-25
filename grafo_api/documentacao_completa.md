# Documentação da API de Teoria dos Grafos com Sessões e Projetos de Estudo

## Visão Geral

Esta API fornece uma interface RESTful para trabalhar com grafos e algoritmos de teoria dos grafos, com suporte a sessões isoladas, projetos de estudo e relatórios didáticos. A API permite criar, manipular, analisar e visualizar grafos, além de executar diversos algoritmos clássicos e avançados, tudo isso mantendo o isolamento entre diferentes usuários sem necessidade de login.

## Recursos Principais

- **Gerenciamento de Grafos**: Criar, editar, excluir e consultar grafos
- **Algoritmos Clássicos**: Dijkstra, Kruskal, Ford-Fulkerson e outros
- **Algoritmos Avançados**: Coloração, emparelhamento, planaridade, análise espectral
- **Operações entre Grafos**: União, interseção, diferença, composição
- **Persistência**: Importação e exportação em diversos formatos (GraphML, GML, GEXF, JSON, CSV)
- **Comparação**: Isomorfismo, similaridade, verificação de subgrafos
- **Visualização**: Geração de dados para visualização e imagens de grafos
- **Sessões Isoladas**: Isolamento de dados entre usuários simultâneos sem login
- **Projetos de Estudo**: Agrupamento de grafos, operações, algoritmos e anotações
- **Relatórios Didáticos**: Exportação de relatórios em PDF com explicações teóricas e passo a passo

## Instalação e Execução

### Requisitos

- Python 3.8+
- NetworkX
- FastAPI
- Uvicorn
- Matplotlib
- SciPy
- NumPy
- WeasyPrint (para geração de PDFs)

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

## Sistema de Sessões

A API utiliza um sistema de sessões para garantir o isolamento de dados entre usuários simultâneos, sem necessidade de login. Cada usuário recebe automaticamente um token de sessão armazenado em cookie, que é utilizado para associar todos os grafos, projetos e operações realizadas.

### Características do Sistema de Sessões

- **Isolamento Completo**: Usuários não podem ver ou acessar dados de outros usuários
- **Sem Login**: Não é necessário criar conta ou fazer login
- **Expiração Automática**: Sessões expiram após 24 horas de inatividade
- **Persistência**: Dados podem ser exportados e importados para continuar o estudo posteriormente

### Como Funciona

1. Na primeira requisição, o usuário recebe automaticamente um cookie de sessão
2. Todas as operações subsequentes são associadas a essa sessão
3. Apenas os dados criados na sessão atual são visíveis para o usuário
4. Para compartilhar ou continuar o estudo em outro momento, o usuário pode exportar projetos ou grafos

## Fluxos de Estudo

### Fluxo Básico de Estudo

1. **Criação de Grafo**: O usuário cria um grafo inicial com vértices e arestas
2. **Análise**: Aplica algoritmos para analisar propriedades do grafo
3. **Visualização**: Visualiza o grafo e os resultados dos algoritmos
4. **Exportação**: Exporta o grafo ou os resultados para uso posterior

### Fluxo de Estudo com Projetos

1. **Criação de Projeto**: O usuário cria um projeto de estudo com título e descrição
2. **Adição de Grafos**: Cria ou importa múltiplos grafos relacionados ao tema de estudo
3. **Aplicação de Algoritmos**: Aplica diferentes algoritmos aos grafos e registra os resultados
4. **Anotações**: Adiciona notas e observações sobre os grafos e algoritmos
5. **Organização**: Utiliza tags para categorizar o projeto
6. **Exportação**: Gera relatórios didáticos em PDF ou exporta o projeto completo

### Fluxo de Compartilhamento e Continuidade

1. **Exportação de Projeto**: O usuário exporta um projeto completo em formato JSON
2. **Compartilhamento**: Envia o arquivo para outros usuários ou salva para uso posterior
3. **Importação**: Outro usuário (ou o mesmo em outro momento) importa o projeto
4. **Continuação**: Continua o estudo a partir do ponto onde parou

## Exemplos de Uso

### Criação de Sessão e Grafo Básico

```python
import requests
import json

# URL base da API
base_url = "http://localhost:8000/api/v1"

# A primeira requisição criará automaticamente uma sessão
# O cookie de sessão será armazenado e enviado automaticamente nas próximas requisições
session = requests.Session()

# Dados para criar um grafo
grafo_data = {
    "nome": "Meu Grafo de Estudo",
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
response = session.post(f"{base_url}/grafos/", json=grafo_data)

# Obtém o ID do grafo criado
grafo_id = response.json()["id"]
print(f"Grafo criado com ID: {grafo_id}")
```

### Criação e Uso de Projetos de Estudo

```python
# Dados para criar um projeto
projeto_data = {
    "titulo": "Estudo de Caminhos Mínimos",
    "descricao": "Análise comparativa de algoritmos de caminho mínimo em diferentes tipos de grafos",
    "autor": "Estudante de Teoria dos Grafos"
}

# Cria o projeto
response = session.post(f"{base_url}/projetos/", json=projeto_data)
projeto_id = response.json()["id"]
print(f"Projeto criado com ID: {projeto_id}")

# Adiciona o grafo ao projeto
response = session.post(f"{base_url}/projetos/{projeto_id}/grafos/{grafo_id}")

# Adiciona uma nota ao projeto
nota_data = {
    "texto": "Este grafo representa uma rede social simples com 3 pessoas.",
    "grafo_id": grafo_id
}
session.post(f"{base_url}/projetos/{projeto_id}/notas", json=nota_data)

# Adiciona tags ao projeto
tags_data = {
    "adicionar": ["redes sociais", "caminhos mínimos", "estudo inicial"],
    "remover": []
}
session.put(f"{base_url}/projetos/{projeto_id}/tags", json=tags_data)
```

### Execução de Algoritmo e Registro no Projeto

```python
# Parâmetros para o algoritmo de Dijkstra
params = {
    "parametros": {
        "origem": "A"
    }
}

# Executa o algoritmo
response = session.post(f"{base_url}/algoritmos/dijkstra/{grafo_id}", json=params)
resultado_dijkstra = response.json()

# Registra o algoritmo no projeto
algoritmo_data = {
    "nome": "dijkstra",
    "descricao": "Cálculo de caminhos mínimos a partir do vértice A",
    "grafo_id": grafo_id,
    "parametros": params["parametros"],
    "resultado": resultado_dijkstra["resultado"]
}
session.post(f"{base_url}/projetos/{projeto_id}/algoritmos", json=algoritmo_data)
```

### Geração de Relatório Didático

```python
# Gera um relatório didático do projeto em PDF
response = session.post(
    f"{base_url}/projetos/{projeto_id}/relatorio",
    params={
        "formato": "pdf",
        "incluir_teoria": True,
        "incluir_passos": True,
        "incluir_referencias": True,
        "estilo": "padrao"
    },
    stream=True
)

# Salva o PDF localmente
with open("relatorio_projeto.pdf", "wb") as f:
    for chunk in response.iter_content(chunk_size=1024):
        f.write(chunk)

print("Relatório didático salvo em relatorio_projeto.pdf")
```

### Exportação e Importação de Projeto

```python
# Exporta o projeto para compartilhamento
response = session.post(f"{base_url}/projetos/{projeto_id}/exportar/arquivo", params={"formato": "json"})

# Salva o arquivo localmente
with open("projeto_exportado.json", "wb") as f:
    for chunk in response.iter_content(chunk_size=1024):
        f.write(chunk)

print("Projeto exportado para projeto_exportado.json")

# Em outra sessão ou momento, importa o projeto
with open("projeto_exportado.json", "rb") as f:
    files = {"arquivo": ("projeto_exportado.json", f, "application/json")}
    response = session.post(
        f"{base_url}/projetos/importar/arquivo",
        files=files,
        data={"formato": "json"}
    )

projeto_importado_id = response.json()["id"]
print(f"Projeto importado com ID: {projeto_importado_id}")
```

## Integração com Frontend

A API foi projetada para ser facilmente integrada com aplicações frontend. Aqui está um exemplo básico de como integrar com uma aplicação React:

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1';

// Configuração do axios para enviar cookies
axios.defaults.withCredentials = true;

function ProjetoEstudoApp() {
  const [projetos, setProjetos] = useState([]);
  const [projetoAtual, setProjetoAtual] = useState(null);
  const [grafos, setGrafos] = useState([]);
  const [notas, setNotas] = useState([]);
  const [historico, setHistorico] = useState([]);

  // Carrega a lista de projetos
  useEffect(() => {
    axios.get(`${API_URL}/projetos/`)
      .then(response => {
        setProjetos(response.data.projetos);
      })
      .catch(error => console.error('Erro ao carregar projetos:', error));
  }, []);

  // Carrega os detalhes do projeto selecionado
  const carregarProjeto = (projetoId) => {
    // Carrega o projeto
    axios.get(`${API_URL}/projetos/${projetoId}`)
      .then(response => {
        setProjetoAtual(response.data);
        
        // Carrega os grafos do projeto
        axios.get(`${API_URL}/projetos/${projetoId}/grafos`)
          .then(response => setGrafos(response.data))
          .catch(error => console.error('Erro ao carregar grafos:', error));
        
        // Carrega as notas do projeto
        axios.get(`${API_URL}/projetos/${projetoId}/notas`)
          .then(response => setNotas(response.data))
          .catch(error => console.error('Erro ao carregar notas:', error));
        
        // Carrega o histórico do projeto
        axios.get(`${API_URL}/projetos/${projetoId}/historico`)
          .then(response => setHistorico(response.data))
          .catch(error => console.error('Erro ao carregar histórico:', error));
      })
      .catch(error => console.error('Erro ao carregar projeto:', error));
  };

  // Cria um novo projeto
  const criarProjeto = () => {
    const novoProjeto = {
      titulo: "Novo Projeto de Estudo",
      descricao: "Descrição do projeto",
      autor: "Usuário"
    };
    
    axios.post(`${API_URL}/projetos/`, novoProjeto)
      .then(response => {
        setProjetos([...projetos, response.data]);
        setProjetoAtual(response.data);
      })
      .catch(error => console.error('Erro ao criar projeto:', error));
  };

  // Gera um relatório do projeto
  const gerarRelatorio = () => {
    if (!projetoAtual) return;
    
    // Abre o relatório em uma nova aba
    window.open(`${API_URL}/projetos/${projetoAtual.id}/relatorio?incluir_teoria=true&incluir_passos=true`, '_blank');
  };

  // Exporta o projeto
  const exportarProjeto = () => {
    if (!projetoAtual) return;
    
    // Inicia o download do arquivo
    window.location.href = `${API_URL}/projetos/${projetoAtual.id}/exportar/arquivo?formato=json`;
  };

  // Importa um projeto
  const importarProjeto = (event) => {
    const arquivo = event.target.files[0];
    if (!arquivo) return;
    
    const formData = new FormData();
    formData.append('arquivo', arquivo);
    formData.append('formato', 'json');
    
    axios.post(`${API_URL}/projetos/importar/arquivo`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    .then(response => {
      setProjetos([...projetos, response.data]);
      setProjetoAtual(response.data);
    })
    .catch(error => console.error('Erro ao importar projeto:', error));
  };

  return (
    <div className="app-container">
      <h1>Plataforma de Estudo de Teoria dos Grafos</h1>
      
      <div className="actions">
        <button onClick={criarProjeto}>Novo Projeto</button>
        <input 
          type="file" 
          id="importar" 
          style={{ display: 'none' }} 
          onChange={importarProjeto} 
        />
        <label htmlFor="importar" className="button">Importar Projeto</label>
      </div>
      
      <div className="content">
        <div className="sidebar">
          <h2>Meus Projetos</h2>
          <ul>
            {projetos.map(projeto => (
              <li key={projeto.id}>
                <button onClick={() => carregarProjeto(projeto.id)}>
                  {projeto.titulo}
                </button>
              </li>
            ))}
          </ul>
        </div>
        
        {projetoAtual && (
          <div className="main-content">
            <div className="projeto-header">
              <h2>{projetoAtual.titulo}</h2>
              <p>{projetoAtual.descricao}</p>
              <div className="tags">
                {projetoAtual.tags && projetoAtual.tags.map(tag => (
                  <span key={tag} className="tag">{tag}</span>
                ))}
              </div>
              <div className="projeto-actions">
                <button onClick={gerarRelatorio}>Gerar Relatório</button>
                <button onClick={exportarProjeto}>Exportar Projeto</button>
              </div>
            </div>
            
            <div className="grafos-section">
              <h3>Grafos ({grafos.length})</h3>
              <div className="grafos-list">
                {grafos.map(grafo => (
                  <div key={grafo.id} className="grafo-card">
                    <h4>{grafo.nome}</h4>
                    <p>Vértices: {grafo.num_vertices}</p>
                    <p>Arestas: {grafo.num_arestas}</p>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="notas-section">
              <h3>Notas ({notas.length})</h3>
              <ul className="notas-list">
                {notas.map(nota => (
                  <li key={nota.id} className="nota">
                    <p>{nota.texto}</p>
                    <small>
                      {nota.grafo_id ? `Relacionada ao grafo ${nota.grafo_id}` : 'Nota geral'}
                    </small>
                  </li>
                ))}
              </ul>
            </div>
            
            <div className="historico-section">
              <h3>Histórico de Atividades</h3>
              <ul className="historico-list">
                {historico.map((acao, index) => (
                  <li key={index} className="acao">
                    <span className="acao-tipo">{acao.tipo}</span>
                    <span className="acao-descricao">{acao.descricao}</span>
                    <span className="acao-timestamp">{new Date(acao.timestamp).toLocaleString()}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProjetoEstudoApp;
```

## Referência da API

### Endpoints de Sessão

- A API gerencia sessões automaticamente através de cookies
- Não há endpoints específicos para gerenciamento de sessões
- Todas as operações são automaticamente associadas à sessão atual

### Endpoints de Grafos

- `GET /api/v1/grafos/`: Lista todos os grafos da sessão atual
- `POST /api/v1/grafos/`: Cria um novo grafo na sessão atual
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

### Endpoints de Projetos

- `POST /api/v1/projetos/`: Cria um novo projeto de estudo
- `GET /api/v1/projetos/`: Lista todos os projetos da sessão atual
- `GET /api/v1/projetos/{projeto_id}`: Obtém os detalhes de um projeto específico
- `PUT /api/v1/projetos/{projeto_id}`: Atualiza os metadados de um projeto
- `DELETE /api/v1/projetos/{projeto_id}`: Exclui um projeto
- `POST /api/v1/projetos/{projeto_id}/grafos/{grafo_id}`: Adiciona um grafo ao projeto
- `DELETE /api/v1/projetos/{projeto_id}/grafos/{grafo_id}`: Remove um grafo do projeto
- `GET /api/v1/projetos/{projeto_id}/grafos`: Lista todos os grafos de um projeto
- `POST /api/v1/projetos/{projeto_id}/notas`: Adiciona uma nota ao projeto
- `GET /api/v1/projetos/{projeto_id}/notas`: Lista todas as notas de um projeto
- `PUT /api/v1/projetos/{projeto_id}/tags`: Atualiza as tags de um projeto
- `GET /api/v1/projetos/{projeto_id}/historico`: Obtém o histórico de ações de um projeto
- `POST /api/v1/projetos/{projeto_id}/exportar`: Exporta um projeto para um formato específico
- `POST /api/v1/projetos/{projeto_id}/exportar/arquivo`: Exporta um projeto para um arquivo
- `POST /api/v1/projetos/importar`: Importa um projeto a partir de uma representação
- `POST /api/v1/projetos/importar/arquivo`: Importa um projeto a partir de um arquivo
- `POST /api/v1/projetos/{projeto_id}/relatorio`: Gera um relatório didático de um projeto

## Considerações de Segurança

- **Isolamento de Sessões**: Cada usuário tem acesso apenas aos seus próprios dados
- **Proteção de Tokens**: Cookies com flag HttpOnly para prevenir acesso via JavaScript
- **Validação de Entradas**: Todas as entradas são validadas para prevenir injeções
- **Expiração de Sessões**: Sessões expiram automaticamente após período de inatividade

## Limitações Conhecidas

- **Armazenamento em Memória**: Os dados são armazenados em memória por padrão, podendo ser perdidos em caso de reinicialização do servidor
- **Escalabilidade**: Para ambientes de produção com muitos usuários simultâneos, recomenda-se substituir o armazenamento em memória por Redis ou similar
- **Desempenho**: O desempenho pode ser afetado ao trabalhar com grafos muito grandes ou muitos projetos por sessão

## Próximos Passos

- **Integração com Banco de Dados**: Implementar persistência de longo prazo para sessões e projetos
- **Autenticação Opcional**: Adicionar sistema de autenticação opcional para usuários que desejam manter seus dados permanentemente
- **Colaboração em Tempo Real**: Permitir que múltiplos usuários trabalhem no mesmo projeto simultaneamente
- **Mais Algoritmos Avançados**: Expandir a biblioteca de algoritmos disponíveis
- **Melhorias na Visualização**: Adicionar mais opções de visualização e interatividade

## Contribuição

Contribuições são bem-vindas! Por favor, sinta-se à vontade para enviar pull requests ou abrir issues para reportar bugs ou sugerir melhorias.

## Licença

Este projeto está licenciado sob a licença MIT.
