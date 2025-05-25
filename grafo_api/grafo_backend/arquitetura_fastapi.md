# Arquitetura da Aplicação Web de Teoria dos Grafos com FastAPI

## Visão Geral da Arquitetura

A arquitetura da aplicação web de teoria dos grafos será baseada em uma API RESTful implementada com FastAPI, mantendo a modularidade do backend existente e expandindo-o com novos algoritmos avançados. A estrutura seguirá os princípios de design limpo, separação de responsabilidades e será otimizada para desempenho e escalabilidade.

```
grafo_api/
├── app/                      # Código principal da aplicação FastAPI
│   ├── api/                  # Endpoints da API
│   │   ├── v1/               # Versão 1 da API
│   │   │   ├── endpoints/    # Endpoints organizados por funcionalidade
│   │   │   │   ├── grafos.py         # CRUD de grafos
│   │   │   │   ├── vertices.py       # Operações com vértices
│   │   │   │   ├── arestas.py        # Operações com arestas
│   │   │   │   ├── algoritmos.py     # Execução de algoritmos
│   │   │   │   ├── operacoes.py      # Operações entre grafos
│   │   │   │   ├── persistencia.py   # Import/export de grafos
│   │   │   │   ├── comparacao.py     # Comparação e isomorfismo
│   │   │   │   └── visualizacao.py   # Dados para visualização
│   │   │   ├── router.py     # Configuração de rotas da v1
│   │   │   └── models.py     # Modelos Pydantic para a API
│   │   └── api.py            # Configuração geral da API
│   ├── core/                 # Configurações e utilitários do núcleo
│   │   ├── config.py         # Configurações da aplicação
│   │   ├── security.py       # Configurações de segurança (opcional)
│   │   └── errors.py         # Tratamento de erros personalizado
│   ├── services/             # Serviços de negócio
│   │   ├── grafo_service.py  # Serviço para operações com grafos
│   │   └── algoritmo_service.py # Serviço para execução de algoritmos
│   ├── schemas/              # Esquemas Pydantic para validação e serialização
│   │   ├── grafo.py          # Esquemas para grafos
│   │   ├── vertice.py        # Esquemas para vértices
│   │   ├── aresta.py         # Esquemas para arestas
│   │   └── resultado.py      # Esquemas para resultados de algoritmos
│   ├── db/                   # Camada de persistência (opcional)
│   │   ├── session.py        # Configuração de sessão
│   │   └── models.py         # Modelos de dados
│   ├── middleware/           # Middleware personalizado
│   │   ├── logging.py        # Middleware de logging
│   │   └── rate_limiter.py   # Limitador de taxa
│   └── main.py               # Ponto de entrada da aplicação
├── grafo_backend/            # Backend existente de teoria dos grafos
│   ├── core/                 # Classes base para representação de grafos
│   ├── tipos/                # Implementações de tipos específicos de grafos
│   ├── algoritmos/           # Algoritmos clássicos e avançados
│   │   ├── caminhos/         # Algoritmos de caminhos mínimos
│   │   ├── arvores/          # Algoritmos de árvores geradoras
│   │   ├── fluxo/            # Algoritmos de fluxo em redes
│   │   ├── coloracao/        # Algoritmos de coloração (novo)
│   │   ├── emparelhamento/   # Algoritmos de emparelhamento (novo)
│   │   ├── planaridade/      # Algoritmos de planaridade (novo)
│   │   ├── espectral/        # Algoritmos de teoria espectral (novo)
│   │   ├── dinamicos/        # Algoritmos para grafos dinâmicos (novo)
│   │   └── centralidade/     # Algoritmos de centralidade (novo)
│   ├── operacoes/            # Operações entre grafos
│   ├── persistencia/         # Importação e exportação de grafos
│   ├── comparacao/           # Funções para comparação e isomorfismo
│   ├── visualizacao/         # Funções para visualização de grafos
│   └── utils/                # Funções utilitárias
├── tests/                    # Testes automatizados
│   ├── api/                  # Testes da API
│   ├── algoritmos/           # Testes dos algoritmos
│   └── conftest.py           # Configurações para testes
├── docs/                     # Documentação adicional
├── static/                   # Arquivos estáticos (opcional)
├── .env                      # Variáveis de ambiente
├── requirements.txt          # Dependências do projeto
├── Dockerfile                # Configuração para Docker (opcional)
└── main.py                   # Script de inicialização
```

## Endpoints da API

A API será organizada em endpoints RESTful que seguem as melhores práticas de design de API. Abaixo está uma visão geral dos principais endpoints:

### Grafos

```
GET     /api/v1/grafos                # Listar todos os grafos
POST    /api/v1/grafos                # Criar um novo grafo
GET     /api/v1/grafos/{id}           # Obter um grafo específico
PUT     /api/v1/grafos/{id}           # Atualizar um grafo
DELETE  /api/v1/grafos/{id}           # Excluir um grafo
```

### Vértices

```
GET     /api/v1/grafos/{id}/vertices          # Listar todos os vértices
POST    /api/v1/grafos/{id}/vertices          # Adicionar um vértice
GET     /api/v1/grafos/{id}/vertices/{v_id}   # Obter um vértice específico
PUT     /api/v1/grafos/{id}/vertices/{v_id}   # Atualizar um vértice
DELETE  /api/v1/grafos/{id}/vertices/{v_id}   # Remover um vértice
```

### Arestas

```
GET     /api/v1/grafos/{id}/arestas                   # Listar todas as arestas
POST    /api/v1/grafos/{id}/arestas                   # Adicionar uma aresta
GET     /api/v1/grafos/{id}/arestas/{origem}/{destino} # Obter uma aresta específica
PUT     /api/v1/grafos/{id}/arestas/{origem}/{destino} # Atualizar uma aresta
DELETE  /api/v1/grafos/{id}/arestas/{origem}/{destino} # Remover uma aresta
```

### Algoritmos

```
GET     /api/v1/algoritmos                            # Listar algoritmos disponíveis
POST    /api/v1/algoritmos/{algoritmo}/grafos/{id}    # Executar algoritmo em um grafo
```

#### Algoritmos Específicos

```
POST    /api/v1/algoritmos/caminhos/dijkstra/grafos/{id}      # Executar Dijkstra
POST    /api/v1/algoritmos/arvores/kruskal/grafos/{id}        # Executar Kruskal
POST    /api/v1/algoritmos/fluxo/ford-fulkerson/grafos/{id}   # Executar Ford-Fulkerson
POST    /api/v1/algoritmos/coloracao/grafos/{id}              # Executar coloração
POST    /api/v1/algoritmos/emparelhamento/grafos/{id}         # Executar emparelhamento
POST    /api/v1/algoritmos/planaridade/grafos/{id}            # Verificar planaridade
POST    /api/v1/algoritmos/espectral/grafos/{id}              # Análise espectral
POST    /api/v1/algoritmos/centralidade/grafos/{id}           # Calcular centralidades
```

### Operações entre Grafos

```
POST    /api/v1/operacoes/uniao                # União de grafos
POST    /api/v1/operacoes/intersecao           # Interseção de grafos
POST    /api/v1/operacoes/diferenca            # Diferença de grafos
POST    /api/v1/operacoes/diferenca-simetrica  # Diferença simétrica
POST    /api/v1/operacoes/composicao           # Composição de grafos
```

### Comparação e Isomorfismo

```
POST    /api/v1/comparacao/isomorfismo         # Verificar isomorfismo
POST    /api/v1/comparacao/similaridade        # Calcular similaridade
POST    /api/v1/comparacao/subgrafo            # Verificar subgrafo
```

### Persistência

```
POST    /api/v1/persistencia/importar          # Importar grafo de arquivo
GET     /api/v1/persistencia/exportar/{id}     # Exportar grafo para arquivo
```

### Visualização

```
GET     /api/v1/visualizacao/grafos/{id}       # Obter dados para visualização
```

## Modelos de Dados

### Grafo

```python
class GrafoBase(BaseModel):
    nome: str
    direcionado: bool = False
    ponderado: bool = False
    bipartido: bool = False

class GrafoCreate(GrafoBase):
    pass

class GrafoUpdate(GrafoBase):
    nome: Optional[str] = None
    direcionado: Optional[bool] = None
    ponderado: Optional[bool] = None
    bipartido: Optional[bool] = None

class Grafo(GrafoBase):
    id: str
    num_vertices: int
    num_arestas: int
    data_criacao: datetime
    data_atualizacao: Optional[datetime] = None

    class Config:
        orm_mode = True
```

### Vértice

```python
class VerticeBase(BaseModel):
    id: Any
    atributos: Dict[str, Any] = {}

class VerticeCreate(VerticeBase):
    pass

class VerticeUpdate(BaseModel):
    atributos: Dict[str, Any]

class Vertice(VerticeBase):
    grau: int
    
    class Config:
        orm_mode = True
```

### Aresta

```python
class ArestaBase(BaseModel):
    origem: Any
    destino: Any
    peso: float = 1.0
    atributos: Dict[str, Any] = {}

class ArestaCreate(ArestaBase):
    pass

class ArestaUpdate(BaseModel):
    peso: Optional[float] = None
    atributos: Optional[Dict[str, Any]] = None

class Aresta(ArestaBase):
    class Config:
        orm_mode = True
```

## Integração com o Backend Existente

A aplicação FastAPI será integrada com o backend existente de teoria dos grafos através de uma camada de serviço que fará a ponte entre os endpoints da API e as funcionalidades do backend. Isso permitirá reutilizar todo o código existente enquanto expõe suas funcionalidades através de uma API web.

```python
# Exemplo de serviço para integração
class GrafoService:
    def __init__(self):
        self.grafos = {}  # Armazenamento em memória (pode ser substituído por banco de dados)
    
    def criar_grafo(self, nome: str, direcionado: bool = False, 
                   ponderado: bool = False, bipartido: bool = False) -> str:
        """Cria um novo grafo e retorna seu ID."""
        from grafo_backend.core import Grafo
        from grafo_backend.tipos import GrafoDirecionado, GrafoPonderado, GrafoBipartido
        
        # Criar o tipo apropriado de grafo
        if bipartido:
            grafo = GrafoBipartido(nome)
        elif ponderado and direcionado:
            grafo = GrafoPonderado(nome, direcionado=True)
        elif ponderado:
            grafo = GrafoPonderado(nome)
        elif direcionado:
            grafo = GrafoDirecionado(nome)
        else:
            grafo = Grafo(nome)
        
        # Gerar ID único
        import uuid
        grafo_id = str(uuid.uuid4())
        
        # Armazenar grafo
        self.grafos[grafo_id] = grafo
        
        return grafo_id
    
    # Outros métodos para manipulação de grafos...
```

## Serialização e Desserialização

Para permitir a transmissão de grafos pela API, serão implementados métodos de serialização e desserialização que convertem entre objetos Grafo do backend e representações JSON compatíveis com a API.

```python
def serializar_grafo(grafo):
    """Converte um objeto Grafo em um dicionário serializável."""
    return {
        "nome": grafo.nome,
        "direcionado": isinstance(grafo, GrafoDirecionado),
        "ponderado": isinstance(grafo, GrafoPonderado),
        "bipartido": isinstance(grafo, GrafoBipartido),
        "vertices": [
            {
                "id": v,
                "atributos": grafo.obter_atributos_vertice(v)
            }
            for v in grafo.obter_vertices()
        ],
        "arestas": [
            {
                "origem": u,
                "destino": v,
                "peso": grafo.obter_peso_aresta(u, v) if hasattr(grafo, "obter_peso_aresta") else 1.0,
                "atributos": grafo.obter_atributos_aresta(u, v)
            }
            for u, v in grafo.obter_arestas()
        ]
    }

def desserializar_grafo(dados):
    """Converte um dicionário em um objeto Grafo."""
    # Implementação da desserialização...
```

## Processamento Assíncrono

Para algoritmos que podem levar muito tempo para executar, será implementado processamento assíncrono usando tarefas em background do FastAPI.

```python
from fastapi import BackgroundTasks

@router.post("/algoritmos/{algoritmo}/grafos/{id}")
async def executar_algoritmo(
    algoritmo: str,
    id: str,
    parametros: Dict[str, Any],
    background_tasks: BackgroundTasks
):
    # Verificar se o algoritmo existe
    if algoritmo not in algoritmos_disponiveis:
        raise HTTPException(status_code=404, detail="Algoritmo não encontrado")
    
    # Verificar se o grafo existe
    if id not in grafo_service.grafos:
        raise HTTPException(status_code=404, detail="Grafo não encontrado")
    
    # Para algoritmos rápidos, executar imediatamente
    if algoritmo in algoritmos_rapidos:
        resultado = executar_algoritmo_sincrono(algoritmo, id, parametros)
        return {"status": "concluído", "resultado": resultado}
    
    # Para algoritmos lentos, executar em background
    task_id = str(uuid.uuid4())
    background_tasks.add_task(
        executar_algoritmo_assincrono,
        algoritmo,
        id,
        parametros,
        task_id
    )
    return {"status": "em_processamento", "task_id": task_id}
```

## Documentação Interativa

A documentação interativa será gerada automaticamente pelo Swagger/OpenAPI do FastAPI, com exemplos e descrições detalhadas para cada endpoint.

```python
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="API de Teoria dos Grafos",
    description="API para estudo e aplicação da teoria dos grafos",
    version="1.0.0",
    docs_url=None,  # Desabilita a documentação padrão
)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Documentação",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )
```

## Segurança e Desempenho

Para garantir a segurança e o desempenho da API, serão implementados:

1. **Limitação de taxa**: Para evitar sobrecarga do servidor
2. **Validação de entrada**: Para prevenir injeções e outros ataques
3. **Cache**: Para melhorar o desempenho de operações frequentes
4. **Compressão**: Para reduzir o tamanho das respostas

```python
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.get("/api/v1/grafos")
@limiter.limit("100/minute")
async def listar_grafos(request: Request):
    # Implementação...
```

## Considerações de Implantação

A aplicação será projetada para ser facilmente implantada em diferentes ambientes:

1. **Desenvolvimento local**: Usando uvicorn diretamente
2. **Produção**: Usando Gunicorn com workers uvicorn
3. **Containerização**: Usando Docker para facilitar a implantação

```python
# main.py
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

```dockerfile
# Dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "--workers", "4"]
```

## Próximos Passos

1. Implementar os algoritmos avançados de teoria dos grafos
2. Criar a estrutura básica da aplicação FastAPI
3. Implementar os endpoints da API
4. Integrar o backend existente com a API
5. Implementar serialização e desserialização de grafos
6. Adicionar documentação interativa
7. Implementar testes automatizados
8. Otimizar desempenho e segurança
9. Preparar para implantação
