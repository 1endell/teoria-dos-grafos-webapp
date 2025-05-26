"""
Inicialização do backend de grafos.

Este arquivo garante que o diretório raiz do projeto esteja sempre disponível
para importações absolutas em todos os módulos do backend.
"""

import sys
import os

# Adiciona o diretório raiz ao path para permitir importações absolutas
# independente de onde o módulo é importado
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
