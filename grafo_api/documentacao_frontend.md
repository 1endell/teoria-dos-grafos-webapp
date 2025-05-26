# Documentação para Desenvolvimento do Frontend da API de Grafos

## Introdução

Este documento fornece instruções detalhadas para o desenvolvimento do frontend da API de Grafos. A API foi completamente corrigida e testada, garantindo que todos os endpoints estejam funcionando corretamente. O frontend deverá fornecer uma interface amigável para interagir com a API, permitindo a criação, visualização, manipulação e análise de grafos.

## Arquitetura da API

A API de Grafos segue uma arquitetura RESTful organizada em módulos, cada um responsável por um conjunto específico de funcionalidades:

1. **Grafos**: Gerenciamento básico de grafos (CRUD)
2. **Algoritmos**: Execução de algoritmos em grafos
3. **Operações**: Operações entre grafos (união, interseção, etc.)
4. **Comparação**: Comparação entre grafos (isomorfismo, similaridade, etc.)
5. **Persistência**: Importação e exportação de grafos
6. **Visualização**: Geração de layouts para visualização de grafos

Todos os endpoints retornam respostas em formato JSON e seguem convenções RESTful para códigos de status HTTP.

## Endpoints Principais

### Módulo de Grafos

#### Listar Grafos
- **Método**: GET
- **URL**: `/api/v1/grafos/`
- **Descrição**: Retorna a lista de todos os grafos disponíveis
- **Parâmetros de Query**:
  - `skip` (opcional): Número de grafos a pular (padrão: 0)
  - `limit` (opcional): Número máximo de grafos a retornar (padrão: 100)
- **Resposta de Sucesso**: 200 OK
  ```json
  {
    "total": 5,
    "grafos": [
      {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "nome": "Grafo de Exemplo",
        "direcionado": true,
        "ponderado": true,
        "bipartido": false,
        "num_vertices": 10,
        "num_arestas": 15,
        "data_criacao": "2025-05-26T10:30:00",
        "data_atualizacao": "2025-05-26T11:45:00"
      },
      ...
    ]
  }
  ```

#### Criar Grafo
- **Método**: POST
- **URL**: `/api/v1/grafos/`
- **Descrição**: Cria um novo grafo
- **Corpo da Requisição**:
  ```json
  {
    "nome": "Novo Grafo",
    "direcionado": true,
    "ponderado": true,
    "bipartido": false,
    "vertices": [
      {"id": "A", "atributos": {"cor": "vermelho"}},
      {"id": "B", "atributos": {"cor": "azul"}}
    ],
    "arestas": [
      {"origem": "A", "destino": "B", "peso": 2.5, "atributos": {"tipo": "amizade"}}
    ]
  }
  ```
- **Resposta de Sucesso**: 201 Created
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "nome": "Novo Grafo",
    "direcionado": true,
    "ponderado": true,
    "bipartido": false,
    "num_vertices": 2,
    "num_arestas": 1,
    "data_criacao": "2025-05-26T13:00:00",
    "data_atualizacao": null
  }
  ```

#### Obter Grafo
- **Método**: GET
- **URL**: `/api/v1/grafos/{grafo_id}`
- **Descrição**: Retorna os detalhes de um grafo específico
- **Resposta de Sucesso**: 200 OK
  ```json
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "nome": "Grafo de Exemplo",
    "direcionado": true,
    "ponderado": true,
    "bipartido": false,
    "num_vertices": 2,
    "num_arestas": 1,
    "data_criacao": "2025-05-26T13:00:00",
    "data_atualizacao": null,
    "vertices": [
      {"id": "A", "atributos": {"cor": "vermelho"}, "grau": 1},
      {"id": "B", "atributos": {"cor": "azul"}, "grau": 1}
    ],
    "arestas": [
      {"origem": "A", "destino": "B", "peso": 2.5, "atributos": {"tipo": "amizade"}}
    ]
  }
  ```

#### Adicionar Vértice
- **Método**: POST
- **URL**: `/api/v1/grafos/{grafo_id}/vertices`
- **Descrição**: Adiciona um vértice ao grafo
- **Corpo da Requisição**:
  ```json
  {
    "id": "C",
    "atributos": {"cor": "verde"}
  }
  ```
- **Resposta de Sucesso**: 200 OK

#### Adicionar Aresta
- **Método**: POST
- **URL**: `/api/v1/grafos/{grafo_id}/arestas`
- **Descrição**: Adiciona uma aresta ao grafo
- **Corpo da Requisição**:
  ```json
  {
    "origem": "A",
    "destino": "C",
    "peso": 3.0,
    "atributos": {"tipo": "colaboração"}
  }
  ```
- **Resposta de Sucesso**: 200 OK

### Módulo de Algoritmos

#### Listar Algoritmos
- **Método**: GET
- **URL**: `/api/v1/algoritmos/`
- **Descrição**: Retorna a lista de todos os algoritmos disponíveis
- **Resposta de Sucesso**: 200 OK
  ```json
  [
    {
      "id": "dijkstra",
      "nome": "Algoritmo de Dijkstra",
      "categoria": "caminhos",
      "descricao": "Calcula o caminho mais curto de um vértice de origem para todos os outros vértices em um grafo ponderado.",
      "parametros_obrigatorios": ["origem"],
      "parametros_opcionais": []
    },
    ...
  ]
  ```

#### Listar Algoritmos por Categoria
- **Método**: GET
- **URL**: `/api/v1/algoritmos/categoria/{categoria}`
- **Descrição**: Retorna a lista de algoritmos de uma categoria específica
- **Categorias Disponíveis**: caminhos, arvores, fluxo, coloracao, emparelhamento, planaridade, espectral, centralidade
- **Resposta de Sucesso**: 200 OK
  ```json
  [
    {
      "id": "dijkstra",
      "nome": "Algoritmo de Dijkstra",
      "categoria": "caminhos",
      "descricao": "Calcula o caminho mais curto de um vértice de origem para todos os outros vértices em um grafo ponderado.",
      "parametros_obrigatorios": ["origem"],
      "parametros_opcionais": []
    },
    ...
  ]
  ```

#### Obter Algoritmo
- **Método**: GET
- **URL**: `/api/v1/algoritmos/algoritmo/{algoritmo_id}`
- **Descrição**: Retorna os detalhes de um algoritmo específico
- **Resposta de Sucesso**: 200 OK
  ```json
  {
    "id": "dijkstra",
    "nome": "Algoritmo de Dijkstra",
    "categoria": "caminhos",
    "descricao": "Calcula o caminho mais curto de um vértice de origem para todos os outros vértices em um grafo ponderado.",
    "parametros_obrigatorios": ["origem"],
    "parametros_opcionais": []
  }
  ```

#### Executar Algoritmo
- **Método**: POST
- **URL**: `/api/v1/algoritmos/executar/{algoritmo_id}/{grafo_id}`
- **Descrição**: Executa um algoritmo em um grafo
- **Corpo da Requisição**:
  ```json
  {
    "parametros": {
      "origem": "A"
    }
  }
  ```
- **Resposta de Sucesso**: 200 OK
  ```json
  {
    "algoritmo": "dijkstra",
    "grafo_id": "123e4567-e89b-12d3-a456-426614174000",
    "resultado": {
      "A": 0.0,
      "B": 1.0,
      "C": 3.0
    },
    "tempo_execucao": 0.0015
  }
  ```

### Módulo de Operações

#### Unir Grafos
- **Método**: POST
- **URL**: `/api/v1/operacoes/uniao`
- **Descrição**: Cria um novo grafo a partir da união de dois grafos
- **Corpo da Requisição**:
  ```json
  {
    "grafo_id1": "123e4567-e89b-12d3-a456-426614174000",
    "grafo_id2": "223e4567-e89b-12d3-a456-426614174001",
    "nome_resultado": "União dos Grafos"
  }
  ```
- **Resposta de Sucesso**: 201 Created
  ```json
  {
    "id": "323e4567-e89b-12d3-a456-426614174002",
    "nome": "União dos Grafos",
    "direcionado": true,
    "ponderado": true,
    "bipartido": false,
    "num_vertices": 5,
    "num_arestas": 8,
    "data_criacao": "2025-05-26T14:30:00",
    "data_atualizacao": null
  }
  ```

#### Interseção de Grafos
- **Método**: POST
- **URL**: `/api/v1/operacoes/intersecao`
- **Descrição**: Cria um novo grafo a partir da interseção de dois grafos
- **Corpo da Requisição**: Similar à união
- **Resposta de Sucesso**: 201 Created (similar à união)

#### Diferença de Grafos
- **Método**: POST
- **URL**: `/api/v1/operacoes/diferenca`
- **Descrição**: Cria um novo grafo a partir da diferença entre dois grafos
- **Corpo da Requisição**: Similar à união
- **Resposta de Sucesso**: 201 Created (similar à união)

### Módulo de Comparação

#### Verificar Isomorfismo
- **Método**: POST
- **URL**: `/api/v1/comparacao/isomorfismo`
- **Descrição**: Verifica se dois grafos são isomórficos
- **Corpo da Requisição**:
  ```json
  {
    "grafo_id1": "123e4567-e89b-12d3-a456-426614174000",
    "grafo_id2": "223e4567-e89b-12d3-a456-426614174001"
  }
  ```
- **Resposta de Sucesso**: 200 OK
  ```json
  {
    "grafo_id1": "123e4567-e89b-12d3-a456-426614174000",
    "grafo_id2": "223e4567-e89b-12d3-a456-426614174001",
    "metrica": "isomorfismo",
    "resultado": true,
    "tempo_execucao": 0.0025
  }
  ```

#### Calcular Similaridade
- **Método**: POST
- **URL**: `/api/v1/comparacao/similaridade`
- **Descrição**: Calcula a similaridade entre dois grafos
- **Corpo da Requisição**: Similar ao isomorfismo
- **Resposta de Sucesso**: 200 OK (similar ao isomorfismo, mas com resultado numérico entre 0 e 1)

#### Verificar Subgrafo
- **Método**: POST
- **URL**: `/api/v1/comparacao/subgrafo`
- **Descrição**: Verifica se um grafo é subgrafo de outro
- **Corpo da Requisição**: Similar ao isomorfismo
- **Resposta de Sucesso**: 200 OK (similar ao isomorfismo, com resultado booleano)

### Módulo de Persistência

#### Exportar Grafo
- **Método**: GET
- **URL**: `/api/v1/persistencia/{grafo_id}/exportar`
- **Descrição**: Exporta um grafo para um formato específico
- **Parâmetros de Query**:
  - `formato` (opcional): Formato de exportação (graphml, gml, gexf, json, csv) (padrão: graphml)
- **Resposta de Sucesso**: 200 OK
  ```json
  {
    "grafo_id": "123e4567-e89b-12d3-a456-426614174000",
    "formato": "json",
    "conteudo": "base64_encoded_content"
  }
  ```

#### Exportar Grafo como Arquivo
- **Método**: GET
- **URL**: `/api/v1/persistencia/{grafo_id}/exportar/arquivo`
- **Descrição**: Exporta um grafo como arquivo para download
- **Parâmetros de Query**:
  - `formato` (opcional): Formato de exportação (graphml, gml, gexf, json, csv) (padrão: graphml)
- **Resposta de Sucesso**: 200 OK com o arquivo para download

#### Importar Grafo
- **Método**: POST
- **URL**: `/api/v1/persistencia/importar`
- **Descrição**: Importa um grafo a partir de uma representação
- **Corpo da Requisição**:
  ```json
  {
    "nome": "Grafo Importado",
    "formato": "json",
    "conteudo": "base64_encoded_content"
  }
  ```
- **Resposta de Sucesso**: 201 Created
  ```json
  {
    "id": "423e4567-e89b-12d3-a456-426614174003",
    "nome": "Grafo Importado",
    "direcionado": true,
    "ponderado": true,
    "bipartido": false,
    "num_vertices": 3,
    "num_arestas": 2,
    "data_criacao": "2025-05-26T15:00:00",
    "data_atualizacao": null
  }
  ```

### Módulo de Visualização

#### Listar Layouts
- **Método**: GET
- **URL**: `/api/v1/visualizacao/layouts`
- **Descrição**: Lista os layouts disponíveis para visualização de grafos
- **Resposta de Sucesso**: 200 OK
  ```json
  [
    "spring",
    "circular",
    "random",
    "spectral",
    "kamada_kawai",
    "shell",
    "bipartite"
  ]
  ```

#### Gerar Visualização
- **Método**: POST
- **URL**: `/api/v1/visualizacao/{grafo_id}`
- **Descrição**: Gera dados para visualização de um grafo
- **Corpo da Requisição**:
  ```json
  {
    "layout": "spring",
    "incluir_atributos": true
  }
  ```
- **Resposta de Sucesso**: 200 OK
  ```json
  {
    "vertices": [
      {"id": "A", "x": 0.5, "y": 0.3, "atributos": {"cor": "vermelho"}},
      {"id": "B", "x": 0.8, "y": 0.7, "atributos": {"cor": "azul"}},
      {"id": "C", "x": 0.2, "y": 0.9, "atributos": {"cor": "verde"}}
    ],
    "arestas": [
      {"origem": "A", "destino": "B", "peso": 2.5, "atributos": {"tipo": "amizade"}},
      {"origem": "B", "destino": "C", "peso": 1.8, "atributos": {"tipo": "colaboração"}}
    ],
    "layout": "spring"
  }
  ```

## Recomendações para o Frontend

### Estrutura Recomendada

O frontend deve ser organizado em módulos que correspondam aos módulos da API:

1. **Página Inicial**: Dashboard com lista de grafos e estatísticas
2. **Gerenciamento de Grafos**: Interface para criar, visualizar, editar e excluir grafos
3. **Visualização de Grafos**: Componente para renderizar grafos visualmente
4. **Algoritmos**: Interface para selecionar e executar algoritmos em grafos
5. **Operações**: Interface para realizar operações entre grafos
6. **Comparação**: Interface para comparar grafos
7. **Importação/Exportação**: Interface para importar e exportar grafos

### Fluxos de Usuário Recomendados

#### Fluxo Principal
1. Usuário acessa a página inicial e vê a lista de grafos disponíveis
2. Usuário pode criar um novo grafo ou selecionar um existente
3. Ao selecionar um grafo, o usuário vê sua visualização e detalhes
4. A partir daí, o usuário pode:
   - Editar o grafo (adicionar/remover vértices e arestas)
   - Executar algoritmos no grafo
   - Realizar operações com outros grafos
   - Comparar com outros grafos
   - Exportar o grafo

#### Fluxo de Criação de Grafo
1. Usuário clica em "Criar Grafo"
2. Usuário preenche os detalhes básicos (nome, direcionado, ponderado, bipartido)
3. Usuário adiciona vértices e arestas através da interface visual ou formulário
4. Usuário salva o grafo

#### Fluxo de Execução de Algoritmo
1. Usuário seleciona um grafo
2. Usuário navega para a seção de algoritmos
3. Usuário seleciona um algoritmo da lista
4. Usuário preenche os parâmetros necessários
5. Usuário executa o algoritmo
6. Resultados são exibidos visualmente no grafo e/ou em formato tabular

### Componentes Recomendados

1. **Visualizador de Grafo**: Componente interativo para visualizar e editar grafos
   - Deve suportar diferentes layouts
   - Deve permitir adicionar/remover vértices e arestas
   - Deve destacar resultados de algoritmos (ex: caminhos, cores)

2. **Seletor de Algoritmos**: Componente para selecionar e configurar algoritmos
   - Deve agrupar algoritmos por categoria
   - Deve exibir descrição e parâmetros necessários
   - Deve validar parâmetros antes da execução

3. **Gerenciador de Grafos**: Componente para listar e gerenciar grafos
   - Deve exibir metadados básicos (nome, número de vértices/arestas)
   - Deve permitir ações rápidas (visualizar, editar, excluir)

4. **Importador/Exportador**: Componente para importar e exportar grafos
   - Deve suportar diferentes formatos
   - Deve permitir visualização prévia antes da importação

### Tecnologias Recomendadas

1. **Framework Frontend**: React, Vue.js ou Angular
2. **Biblioteca de Visualização de Grafos**: D3.js, Cytoscape.js ou Sigma.js
3. **Gerenciamento de Estado**: Redux, Vuex ou NgRx
4. **Requisições HTTP**: Axios ou Fetch API
5. **Estilização**: Tailwind CSS, Material UI ou Bootstrap

### Tratamento de Erros

O frontend deve tratar adequadamente os erros retornados pela API:

1. **Erro 400 (Bad Request)**: Exibir mensagem específica sobre o problema nos parâmetros
2. **Erro 404 (Not Found)**: Exibir mensagem indicando que o recurso não foi encontrado
3. **Erro 500 (Internal Server Error)**: Exibir mensagem genérica de erro interno

### Considerações de Desempenho

1. **Paginação**: Implementar paginação na listagem de grafos para lidar com grandes quantidades
2. **Carregamento Assíncrono**: Carregar dados sob demanda para melhorar a experiência do usuário
3. **Caching**: Armazenar em cache resultados de algoritmos e visualizações para reutilização

## Exemplos de Integração

### Exemplo 1: Listar e Visualizar Grafos

```javascript
// Listar grafos
async function listarGrafos() {
  try {
    const response = await fetch('/api/v1/grafos/');
    const data = await response.json();
    return data.grafos;
  } catch (error) {
    console.error('Erro ao listar grafos:', error);
    return [];
  }
}

// Visualizar grafo
async function visualizarGrafo(grafoId) {
  try {
    // Obter detalhes do grafo
    const grafoResponse = await fetch(`/api/v1/grafos/${grafoId}`);
    const grafo = await grafoResponse.json();
    
    // Obter dados de visualização
    const visualizacaoResponse = await fetch(`/api/v1/visualizacao/${grafoId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        layout: 'spring',
        incluir_atributos: true
      })
    });
    const visualizacao = await visualizacaoResponse.json();
    
    // Renderizar grafo com biblioteca de visualização
    renderizarGrafo(grafo, visualizacao);
  } catch (error) {
    console.error('Erro ao visualizar grafo:', error);
  }
}
```

### Exemplo 2: Executar Algoritmo

```javascript
async function executarAlgoritmo(grafoId, algoritmoId, parametros) {
  try {
    const response = await fetch(`/api/v1/algoritmos/executar/${algoritmoId}/${grafoId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        parametros: parametros
      })
    });
    
    if (!response.ok) {
      const erro = await response.json();
      throw new Error(erro.detail);
    }
    
    const resultado = await response.json();
    return resultado;
  } catch (error) {
    console.error(`Erro ao executar algoritmo ${algoritmoId}:`, error);
    throw error;
  }
}

// Exemplo de uso
try {
  const resultado = await executarAlgoritmo(
    '123e4567-e89b-12d3-a456-426614174000',
    'dijkstra',
    { origem: 'A' }
  );
  
  // Exibir resultado
  console.log('Distâncias:', resultado.resultado);
  console.log('Tempo de execução:', resultado.tempo_execucao, 'segundos');
  
  // Destacar caminho no grafo
  destacarCaminhoNoGrafo(resultado.resultado);
} catch (error) {
  // Exibir mensagem de erro para o usuário
  mostrarErro(error.message);
}
```

### Exemplo 3: Importar Grafo

```javascript
async function importarGrafo(nome, formato, conteudo) {
  try {
    // Codificar conteúdo em base64
    const conteudoBase64 = btoa(conteudo);
    
    const response = await fetch('/api/v1/persistencia/importar', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nome: nome,
        formato: formato,
        conteudo: conteudoBase64
      })
    });
    
    if (!response.ok) {
      const erro = await response.json();
      throw new Error(erro.detail);
    }
    
    const grafoImportado = await response.json();
    return grafoImportado;
  } catch (error) {
    console.error('Erro ao importar grafo:', error);
    throw error;
  }
}

// Exemplo de uso com arquivo
document.getElementById('importForm').addEventListener('submit', async (event) => {
  event.preventDefault();
  
  const fileInput = document.getElementById('fileInput');
  const file = fileInput.files[0];
  const nome = document.getElementById('nomeInput').value;
  
  if (!file) {
    alert('Selecione um arquivo para importar');
    return;
  }
  
  // Determinar formato pelo tipo ou extensão do arquivo
  let formato;
  if (file.name.endsWith('.json')) formato = 'json';
  else if (file.name.endsWith('.graphml')) formato = 'graphml';
  else if (file.name.endsWith('.gml')) formato = 'gml';
  else if (file.name.endsWith('.gexf')) formato = 'gexf';
  else if (file.name.endsWith('.csv')) formato = 'csv';
  else {
    alert('Formato de arquivo não suportado');
    return;
  }
  
  try {
    // Ler arquivo como texto
    const conteudo = await file.text();
    
    // Importar grafo
    const grafoImportado = await importarGrafo(nome, formato, conteudo);
    
    // Redirecionar para visualização do grafo importado
    window.location.href = `/grafos/${grafoImportado.id}`;
  } catch (error) {
    alert(`Erro ao importar grafo: ${error.message}`);
  }
});
```

## Conclusão

Esta documentação fornece as informações necessárias para desenvolver um frontend completo para a API de Grafos. Seguindo as recomendações e exemplos fornecidos, será possível criar uma interface intuitiva e funcional que aproveite todas as capacidades da API.

Lembre-se de que a API foi completamente testada e validada, garantindo que todos os endpoints funcionem conforme o esperado. Caso encontre algum problema durante o desenvolvimento do frontend, verifique se está seguindo corretamente as especificações dos endpoints e os formatos de requisição/resposta.

Para qualquer dúvida adicional, consulte a documentação completa da API ou entre em contato com a equipe de desenvolvimento do backend.
