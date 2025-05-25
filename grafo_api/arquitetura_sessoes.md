# Arquitetura do Sistema de Sessões e Armazenamento Temporário

## Visão Geral

A arquitetura proposta implementa um sistema de sessões sem login que permite isolamento de dados entre usuários simultâneos, mantendo a simplicidade de acesso e garantindo a privacidade dos estudos de cada usuário. O sistema utiliza tokens de sessão e um mecanismo de armazenamento temporário integrado ao backend FastAPI.

## Componentes Principais

### 1. Gerenciador de Sessões

**Responsabilidades:**
- Gerar identificadores únicos de sessão (tokens)
- Validar tokens de sessão existentes
- Gerenciar ciclo de vida das sessões (criação, expiração, renovação)
- Fornecer middleware para validação automática de sessões em requisições

**Implementação:**
```python
class SessionManager:
    def __init__(self, expiration_time=86400):  # 24 horas em segundos
        self.expiration_time = expiration_time
        self.active_sessions = {}  # Mapa de sessões ativas
    
    def create_session(self):
        """Cria uma nova sessão e retorna o token"""
        session_id = self._generate_secure_token()
        self.active_sessions[session_id] = {
            "created_at": time.time(),
            "last_activity": time.time(),
            "data": {}  # Dados específicos da sessão
        }
        return session_id
    
    def validate_session(self, session_id):
        """Valida um token de sessão e atualiza o timestamp de atividade"""
        if session_id not in self.active_sessions:
            return False
            
        session = self.active_sessions[session_id]
        current_time = time.time()
        
        # Verifica se a sessão expirou
        if current_time - session["last_activity"] > self.expiration_time:
            self.delete_session(session_id)
            return False
            
        # Atualiza o timestamp de última atividade
        session["last_activity"] = current_time
        return True
    
    def delete_session(self, session_id):
        """Remove uma sessão e seus dados associados"""
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            # Limpar dados associados à sessão no armazenamento
            self.storage_manager.clear_session_data(session_id)
    
    def _generate_secure_token(self):
        """Gera um token seguro e único"""
        return secrets.token_urlsafe(32)  # 32 bytes = 256 bits
```

### 2. Armazenamento de Dados por Sessão

**Responsabilidades:**
- Armazenar grafos, projetos e outros dados associados a cada sessão
- Garantir isolamento entre dados de diferentes sessões
- Gerenciar limpeza de dados de sessões expiradas

**Implementação:**
```python
class SessionStorageManager:
    def __init__(self, cleanup_interval=3600):  # Limpeza a cada hora
        self.storage = {}  # Armazenamento em memória por sessão
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
    
    def store_graph(self, session_id, graph_id, graph_data):
        """Armazena um grafo associado a uma sessão"""
        self._ensure_session_exists(session_id)
        self.storage[session_id]["graphs"][graph_id] = graph_data
        return True
    
    def get_graph(self, session_id, graph_id):
        """Recupera um grafo específico de uma sessão"""
        if not self._session_has_graph(session_id, graph_id):
            return None
        return self.storage[session_id]["graphs"][graph_id]
    
    def list_session_graphs(self, session_id):
        """Lista todos os grafos de uma sessão"""
        self._ensure_session_exists(session_id)
        return list(self.storage[session_id]["graphs"].keys())
    
    def store_project(self, session_id, project_id, project_data):
        """Armazena um projeto associado a uma sessão"""
        self._ensure_session_exists(session_id)
        self.storage[session_id]["projects"][project_id] = project_data
        return True
    
    def clear_session_data(self, session_id):
        """Remove todos os dados associados a uma sessão"""
        if session_id in self.storage:
            del self.storage[session_id]
    
    def cleanup_expired_sessions(self, session_manager):
        """Remove dados de sessões expiradas"""
        current_time = time.time()
        if current_time - self.last_cleanup < self.cleanup_interval:
            return
            
        self.last_cleanup = current_time
        active_sessions = set(session_manager.active_sessions.keys())
        stored_sessions = set(self.storage.keys())
        
        # Encontra sessões no armazenamento que não estão mais ativas
        expired_sessions = stored_sessions - active_sessions
        
        # Remove dados de sessões expiradas
        for session_id in expired_sessions:
            self.clear_session_data(session_id)
    
    def _ensure_session_exists(self, session_id):
        """Garante que a estrutura de armazenamento para a sessão existe"""
        if session_id not in self.storage:
            self.storage[session_id] = {
                "graphs": {},
                "projects": {},
                "history": []
            }
    
    def _session_has_graph(self, session_id, graph_id):
        """Verifica se um grafo específico existe na sessão"""
        return (session_id in self.storage and 
                "graphs" in self.storage[session_id] and
                graph_id in self.storage[session_id]["graphs"])
```

### 3. Middleware de Sessão para FastAPI

**Responsabilidades:**
- Interceptar requisições para validar tokens de sessão
- Criar novas sessões para usuários sem token
- Adicionar informações de sessão ao contexto da requisição

**Implementação:**
```python
class SessionMiddleware:
    def __init__(self, session_manager):
        self.session_manager = session_manager
    
    async def __call__(self, request: Request, call_next):
        # Tenta obter o token de sessão do cookie
        session_id = request.cookies.get("session_id")
        
        # Se não existir ou for inválido, cria uma nova sessão
        is_new_session = False
        if not session_id or not self.session_manager.validate_session(session_id):
            session_id = self.session_manager.create_session()
            is_new_session = True
        
        # Adiciona o ID da sessão ao estado da requisição
        request.state.session_id = session_id
        request.state.is_new_session = is_new_session
        
        # Processa a requisição
        response = await call_next(request)
        
        # Se for uma nova sessão, define o cookie
        if is_new_session:
            response.set_cookie(
                key="session_id",
                value=session_id,
                httponly=True,
                max_age=86400,  # 24 horas
                samesite="lax"
            )
        
        return response
```

### 4. Adaptador de Serviços

**Responsabilidades:**
- Adaptar os serviços existentes para trabalhar com o contexto de sessão
- Filtrar operações por ID de sessão
- Garantir isolamento de dados entre sessões

**Implementação:**
```python
class SessionAwareGrafoService:
    def __init__(self, storage_manager):
        self.storage_manager = storage_manager
    
    def criar_grafo(self, session_id, nome, direcionado=False, ponderado=False, bipartido=False):
        """Cria um grafo associado a uma sessão específica"""
        # Cria o grafo usando a implementação existente
        grafo = Grafo(nome=nome, direcionado=direcionado, ponderado=ponderado, bipartido=bipartido)
        
        # Gera um ID único para o grafo
        grafo_id = str(uuid.uuid4())
        
        # Armazena o grafo associado à sessão
        self.storage_manager.store_graph(session_id, grafo_id, grafo)
        
        return grafo_id
    
    def listar_grafos(self, session_id, skip=0, limit=100):
        """Lista grafos associados a uma sessão específica"""
        # Obtém apenas os grafos da sessão atual
        grafos_ids = self.storage_manager.list_session_graphs(session_id)
        
        # Aplica paginação
        total = len(grafos_ids)
        grafos_ids = grafos_ids[skip:skip+limit]
        
        # Obtém os metadados de cada grafo
        grafos = []
        for grafo_id in grafos_ids:
            grafo = self.storage_manager.get_graph(session_id, grafo_id)
            if grafo:
                metadados = self._extrair_metadados(grafo_id, grafo)
                grafos.append(metadados)
        
        return total, grafos
    
    def obter_grafo(self, session_id, grafo_id):
        """Obtém um grafo específico de uma sessão"""
        grafo = self.storage_manager.get_graph(session_id, grafo_id)
        if not grafo:
            raise ValueError(f"Grafo com ID {grafo_id} não encontrado na sessão atual")
        return grafo
    
    def _extrair_metadados(self, grafo_id, grafo):
        """Extrai metadados básicos de um grafo"""
        return {
            "id": grafo_id,
            "nome": grafo.nome,
            "direcionado": grafo.eh_direcionado() if hasattr(grafo, 'eh_direcionado') else False,
            "ponderado": grafo.eh_ponderado() if hasattr(grafo, 'eh_ponderado') else False,
            "bipartido": grafo.eh_bipartido() if hasattr(grafo, 'eh_bipartido') else False,
            "num_vertices": grafo.numero_vertices(),
            "num_arestas": grafo.numero_arestas()
        }
```

## Integração com a API Existente

### 1. Configuração da Aplicação

```python
def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )
    
    # Inicializa o gerenciador de sessões
    session_manager = SessionManager()
    storage_manager = SessionStorageManager()
    
    # Configura o middleware de sessão
    app.add_middleware(SessionMiddleware, session_manager=session_manager)
    
    # Configura os serviços com suporte a sessão
    app.state.session_manager = session_manager
    app.state.storage_manager = storage_manager
    app.state.grafo_service = SessionAwareGrafoService(storage_manager)
    
    # Adiciona os roteadores
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app
```

### 2. Adaptação dos Endpoints

```python
@router.post("/", response_model=GrafoInfo, status_code=201)
def criar_grafo(
    grafo: GrafoCreate,
    request: Request
):
    """Cria um novo grafo na sessão atual."""
    session_id = request.state.session_id
    grafo_service = request.app.state.grafo_service
    
    grafo_id = grafo_service.criar_grafo(
        session_id=session_id,
        nome=grafo.nome,
        direcionado=grafo.direcionado,
        ponderado=grafo.ponderado,
        bipartido=grafo.bipartido
    )
    
    # Resto da implementação...
    return metadados
```

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                        Cliente (Browser)                        │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Cookie de Sessão                           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Application                         │
│  ┌─────────────────────────┐      ┌─────────────────────────┐  │
│  │   Session Middleware    │◄────►│    Session Manager      │  │
│  └─────────────┬───────────┘      └─────────────┬───────────┘  │
│                │                                │              │
│                ▼                                ▼              │
│  ┌─────────────────────────┐      ┌─────────────────────────┐  │
│  │      API Endpoints      │◄────►│  Storage Manager        │  │
│  └─────────────┬───────────┘      └─────────────┬───────────┘  │
│                │                                │              │
│                ▼                                ▼              │
│  ┌─────────────────────────┐      ┌─────────────────────────┐  │
│  │ Session-Aware Services  │◄────►│  Session Data Storage   │  │
│  └─────────────────────────┘      └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Considerações de Segurança

1. **Proteção de Tokens**
   - Cookies com flag HttpOnly para prevenir acesso via JavaScript
   - Implementação de SameSite para mitigar ataques CSRF
   - Tokens suficientemente longos e aleatórios (256 bits)

2. **Isolamento de Dados**
   - Validação rigorosa de IDs de sessão em todas as operações
   - Verificação de propriedade antes de qualquer acesso a dados
   - Sanitização de entradas para prevenir injeções

3. **Expiração e Limpeza**
   - Expiração automática de sessões inativas
   - Limpeza periódica de dados de sessões expiradas
   - Limite de recursos por sessão para prevenir DoS

## Considerações de Escalabilidade

1. **Armazenamento Distribuído**
   - Para ambientes de produção, substituir o armazenamento em memória por Redis ou similar
   - Implementar particionamento de dados por sessão

2. **Balanceamento de Carga**
   - Garantir que sessões sejam mantidas no mesmo servidor ou usar armazenamento compartilhado
   - Implementar sticky sessions se necessário

3. **Monitoramento**
   - Rastrear número de sessões ativas
   - Monitorar uso de recursos por sessão
   - Implementar limites de uso para prevenir abuso
