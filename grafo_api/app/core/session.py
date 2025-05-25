"""
Middleware para gerenciamento de sessões no FastAPI.

Este módulo implementa o middleware de sessão para garantir isolamento
de dados entre usuários simultâneos sem necessidade de login.
"""

import time
import secrets
from typing import Dict, Any, Optional

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SessionManager:
    """
    Gerenciador de sessões para isolamento de dados entre usuários.
    """
    
    def __init__(self, expiration_time: int = 86400):  # 24 horas em segundos
        """
        Inicializa o gerenciador de sessões.
        
        Args:
            expiration_time: Tempo de expiração das sessões em segundos
        """
        self.expiration_time = expiration_time
        self.active_sessions = {}  # Mapa de sessões ativas: session_id -> dados da sessão
    
    def create_session(self) -> str:
        """
        Cria uma nova sessão e retorna o token.
        
        Returns:
            str: Token de sessão gerado
        """
        session_id = self._generate_secure_token()
        self.active_sessions[session_id] = {
            "created_at": time.time(),
            "last_activity": time.time(),
            "data": {}  # Dados específicos da sessão
        }
        return session_id
    
    def validate_session(self, session_id: str) -> bool:
        """
        Valida um token de sessão e atualiza o timestamp de atividade.
        
        Args:
            session_id: Token de sessão a ser validado
            
        Returns:
            bool: True se a sessão é válida, False caso contrário
        """
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
    
    def delete_session(self, session_id: str) -> None:
        """
        Remove uma sessão e seus dados associados.
        
        Args:
            session_id: Token de sessão a ser removido
        """
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
    
    def get_session_data(self, session_id: str, key: str, default: Any = None) -> Any:
        """
        Obtém um dado específico da sessão.
        
        Args:
            session_id: Token de sessão
            key: Chave do dado
            default: Valor padrão se a chave não existir
            
        Returns:
            Any: Valor associado à chave ou o valor padrão
        """
        if not self.validate_session(session_id):
            return default
            
        return self.active_sessions[session_id]["data"].get(key, default)
    
    def set_session_data(self, session_id: str, key: str, value: Any) -> bool:
        """
        Define um dado específico na sessão.
        
        Args:
            session_id: Token de sessão
            key: Chave do dado
            value: Valor a ser armazenado
            
        Returns:
            bool: True se o dado foi armazenado, False caso contrário
        """
        if not self.validate_session(session_id):
            return False
            
        self.active_sessions[session_id]["data"][key] = value
        return True
    
    def get_all_sessions(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtém todas as sessões ativas.
        
        Returns:
            Dict[str, Dict[str, Any]]: Mapa de sessões ativas
        """
        return self.active_sessions
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove sessões expiradas.
        
        Returns:
            int: Número de sessões removidas
        """
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if current_time - session["last_activity"] > self.expiration_time:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.delete_session(session_id)
        
        return len(expired_sessions)
    
    def _generate_secure_token(self) -> str:
        """
        Gera um token seguro e único.
        
        Returns:
            str: Token gerado
        """
        return secrets.token_urlsafe(32)  # 32 bytes = 256 bits


class SessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware para gerenciamento de sessões no FastAPI.
    """
    
    def __init__(self, app, session_manager: SessionManager):
        """
        Inicializa o middleware de sessão.
        
        Args:
            app: Aplicação FastAPI
            session_manager: Gerenciador de sessões
        """
        super().__init__(app)
        self.session_manager = session_manager
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Processa a requisição e gerencia a sessão.
        
        Args:
            request: Requisição HTTP
            call_next: Função para chamar o próximo middleware
            
        Returns:
            Response: Resposta HTTP
        """
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
                max_age=self.session_manager.expiration_time,
                samesite="lax"
            )
        
        return response


class SessionStorage:
    """
    Armazenamento de dados por sessão.
    """
    
    def __init__(self, cleanup_interval: int = 3600):  # Limpeza a cada hora
        """
        Inicializa o armazenamento de sessão.
        
        Args:
            cleanup_interval: Intervalo de limpeza em segundos
        """
        self.storage = {}  # session_id -> {tipo_dados -> {id -> dados}}
        self.cleanup_interval = cleanup_interval
        self.last_cleanup = time.time()
    
    def store_data(self, session_id: str, data_type: str, data_id: str, data: Any) -> bool:
        """
        Armazena dados associados a uma sessão.
        
        Args:
            session_id: ID da sessão
            data_type: Tipo de dados (ex: "grafos", "projetos")
            data_id: ID dos dados
            data: Dados a serem armazenados
            
        Returns:
            bool: True se os dados foram armazenados com sucesso
        """
        self._ensure_session_exists(session_id, data_type)
        self.storage[session_id][data_type][data_id] = data
        return True
    
    def get_data(self, session_id: str, data_type: str, data_id: str) -> Optional[Any]:
        """
        Recupera dados associados a uma sessão.
        
        Args:
            session_id: ID da sessão
            data_type: Tipo de dados
            data_id: ID dos dados
            
        Returns:
            Optional[Any]: Dados recuperados ou None se não encontrados
        """
        if not self._session_has_data(session_id, data_type, data_id):
            return None
        return self.storage[session_id][data_type][data_id]
    
    def list_data(self, session_id: str, data_type: str) -> Dict[str, Any]:
        """
        Lista todos os dados de um tipo associados a uma sessão.
        
        Args:
            session_id: ID da sessão
            data_type: Tipo de dados
            
        Returns:
            Dict[str, Any]: Mapa de IDs para dados
        """
        self._ensure_session_exists(session_id, data_type)
        return self.storage[session_id][data_type]
    
    def delete_data(self, session_id: str, data_type: str, data_id: str) -> bool:
        """
        Remove dados associados a uma sessão.
        
        Args:
            session_id: ID da sessão
            data_type: Tipo de dados
            data_id: ID dos dados
            
        Returns:
            bool: True se os dados foram removidos com sucesso
        """
        if not self._session_has_data(session_id, data_type, data_id):
            return False
        del self.storage[session_id][data_type][data_id]
        return True
    
    def clear_session_data(self, session_id: str) -> bool:
        """
        Remove todos os dados associados a uma sessão.
        
        Args:
            session_id: ID da sessão
            
        Returns:
            bool: True se os dados foram removidos com sucesso
        """
        if session_id in self.storage:
            del self.storage[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self, session_manager: SessionManager) -> int:
        """
        Remove dados de sessões expiradas.
        
        Args:
            session_manager: Gerenciador de sessões para verificar sessões ativas
            
        Returns:
            int: Número de sessões limpas
        """
        current_time = time.time()
        if current_time - self.last_cleanup < self.cleanup_interval:
            return 0
            
        self.last_cleanup = current_time
        active_sessions = set(session_manager.active_sessions.keys())
        stored_sessions = set(self.storage.keys())
        
        # Encontra sessões no armazenamento que não estão mais ativas
        expired_sessions = stored_sessions - active_sessions
        
        # Remove dados de sessões expiradas
        for session_id in expired_sessions:
            self.clear_session_data(session_id)
        
        return len(expired_sessions)
    
    def _ensure_session_exists(self, session_id: str, data_type: str) -> None:
        """
        Garante que a estrutura de armazenamento para a sessão existe.
        
        Args:
            session_id: ID da sessão
            data_type: Tipo de dados
        """
        if session_id not in self.storage:
            self.storage[session_id] = {}
        
        if data_type not in self.storage[session_id]:
            self.storage[session_id][data_type] = {}
    
    def _session_has_data(self, session_id: str, data_type: str, data_id: str) -> bool:
        """
        Verifica se dados específicos existem na sessão.
        
        Args:
            session_id: ID da sessão
            data_type: Tipo de dados
            data_id: ID dos dados
            
        Returns:
            bool: True se os dados existem
        """
        return (session_id in self.storage and 
                data_type in self.storage[session_id] and
                data_id in self.storage[session_id][data_type])
