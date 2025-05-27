
import { GrafoCreate, GrafoInfo, Grafo, VerticeCreate, ArestaCreate, DadosVisualizacao, ResultadoAlgoritmo, OperacaoGrafos, ComparacaoGrafos, ResultadoComparacao, ImportacaoGrafo, ExportacaoGrafo } from '@/types/graph';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://grafos-api.datasortingmachine.com';

class GraphService {
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const sessionId = localStorage.getItem('graph-session-id') || this.generateSessionId();
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'X-Session-ID': sessionId,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  private generateSessionId(): string {
    let sessionId: string;
    
    // Verifica se crypto.randomUUID está disponível (HTTPS ou localhost)
    if (typeof crypto !== 'undefined' && crypto.randomUUID) {
      sessionId = crypto.randomUUID();
    } else {
      // Fallback para ambientes onde crypto.randomUUID não está disponível
      sessionId = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }
    
    localStorage.setItem('graph-session-id', sessionId);
    return sessionId;
  }

  // ===== GRAFOS =====
  async criarGrafo(grafo: GrafoCreate): Promise<GrafoInfo> {
    return this.request<GrafoInfo>('/api/v1/grafos/', {
      method: 'POST',
      body: JSON.stringify(grafo),
    });
  }

  async listarGrafos(skip = 0, limit = 100): Promise<{ total: number; grafos: GrafoInfo[] }> {
    return this.request<{ total: number; grafos: GrafoInfo[] }>(`/api/v1/grafos/?skip=${skip}&limit=${limit}`);
  }

  async obterGrafo(grafoId: string): Promise<Grafo> {
    return this.request<Grafo>(`/api/v1/grafos/${grafoId}`);
  }

  async atualizarGrafo(grafoId: string, dados: { nome?: string; direcionado?: boolean; ponderado?: boolean; bipartido?: boolean }): Promise<GrafoInfo> {
    return this.request<GrafoInfo>(`/api/v1/grafos/${grafoId}`, {
      method: 'PUT',
      body: JSON.stringify(dados),
    });
  }

  async excluirGrafo(grafoId: string): Promise<void> {
    await this.request(`/api/v1/grafos/${grafoId}`, {
      method: 'DELETE',
    });
  }

  async adicionarVertice(grafoId: string, vertice: VerticeCreate): Promise<void> {
    return this.request(`/api/v1/grafos/${grafoId}/vertices`, {
      method: 'POST',
      body: JSON.stringify(vertice),
    });
  }

  async adicionarAresta(grafoId: string, aresta: ArestaCreate): Promise<void> {
    return this.request(`/api/v1/grafos/${grafoId}/arestas`, {
      method: 'POST',
      body: JSON.stringify(aresta),
    });
  }

  async removerVertice(grafoId: string, verticeId: string): Promise<void> {
    await this.request(`/api/v1/grafos/${grafoId}/vertices/${verticeId}`, {
      method: 'DELETE',
    });
  }

  async removerAresta(grafoId: string, origem: string, destino: string): Promise<void> {
    await this.request(`/api/v1/grafos/${grafoId}/arestas/${origem}/${destino}`, {
      method: 'DELETE',
    });
  }

  // ===== VISUALIZAÇÃO =====
  async listarLayouts(): Promise<string[]> {
    return this.request<string[]>('/api/v1/visualizacao/layouts');
  }

  async obterVisualizacao(grafoId: string, layout = 'spring', incluirAtributos = true): Promise<DadosVisualizacao> {
    return this.request<DadosVisualizacao>(`/api/v1/visualizacao/${grafoId}?layout=${layout}&incluir_atributos=${incluirAtributos}`);
  }

  // ===== ALGORITMOS =====
  async listarAlgoritmos(): Promise<any[]> {
    return this.request<any[]>('/api/v1/algoritmos/');
  }

  async listarAlgorimosPorCategoria(categoria: string): Promise<any[]> {
    return this.request<any[]>(`/api/v1/algoritmos/categoria/${categoria}`);
  }

  async obterAlgoritmo(algoritmoId: string): Promise<any> {
    return this.request<any>(`/api/v1/algoritmos/algoritmo/${algoritmoId}`);
  }

  async executarAlgoritmo(algoritmoId: string, grafoId: string, parametros = {}): Promise<ResultadoAlgoritmo> {
    return this.request<ResultadoAlgoritmo>(`/api/v1/algoritmos/executar/${algoritmoId}/${grafoId}`, {
      method: 'POST',
      body: JSON.stringify({ parametros }),
    });
  }

  // ===== OPERAÇÕES =====
  async unirGrafos(grafoId1: string, grafoId2: string, nomeResultado?: string): Promise<GrafoInfo> {
    return this.request<GrafoInfo>('/api/v1/operacoes/uniao', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2,
        nome_resultado: nomeResultado
      }),
    });
  }

  async intersecaoGrafos(grafoId1: string, grafoId2: string, nomeResultado?: string): Promise<GrafoInfo> {
    return this.request<GrafoInfo>('/api/v1/operacoes/intersecao', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2,
        nome_resultado: nomeResultado
      }),
    });
  }

  async diferencaGrafos(grafoId1: string, grafoId2: string, nomeResultado?: string): Promise<GrafoInfo> {
    return this.request<GrafoInfo>('/api/v1/operacoes/diferenca', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2,
        nome_resultado: nomeResultado
      }),
    });
  }

  async diferencaSimetricaGrafos(grafoId1: string, grafoId2: string, nomeResultado?: string): Promise<GrafoInfo> {
    return this.request<GrafoInfo>('/api/v1/operacoes/diferenca-simetrica', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2,
        nome_resultado: nomeResultado
      }),
    });
  }

  async composicaoGrafos(grafoId1: string, grafoId2: string, nomeResultado?: string): Promise<GrafoInfo> {
    return this.request<GrafoInfo>('/api/v1/operacoes/composicao', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2,
        nome_resultado: nomeResultado
      }),
    });
  }

  // ===== COMPARAÇÃO =====
  async verificarIsomorfismo(grafoId1: string, grafoId2: string): Promise<ResultadoComparacao> {
    return this.request<ResultadoComparacao>('/api/v1/comparacao/isomorfismo', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2
      }),
    });
  }

  async calcularSimilaridade(grafoId1: string, grafoId2: string): Promise<ResultadoComparacao> {
    return this.request<ResultadoComparacao>('/api/v1/comparacao/similaridade', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2
      }),
    });
  }

  async verificarSubgrafo(grafoId1: string, grafoId2: string): Promise<ResultadoComparacao> {
    return this.request<ResultadoComparacao>('/api/v1/comparacao/subgrafo', {
      method: 'POST',
      body: JSON.stringify({
        grafo_id1: grafoId1,
        grafo_id2: grafoId2
      }),
    });
  }

  // ===== PERSISTÊNCIA =====
  async exportarGrafo(grafoId: string, formato = 'json'): Promise<any> {
    return this.request<any>(`/api/v1/persistencia/${grafoId}/exportar?formato=${formato}`);
  }

  async exportarGrafoArquivo(grafoId: string, formato = 'json'): Promise<Blob> {
    const response = await fetch(`${API_BASE_URL}/api/v1/persistencia/${grafoId}/exportar/arquivo?formato=${formato}`, {
      headers: {
        'X-Session-ID': localStorage.getItem('graph-session-id') || this.generateSessionId(),
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.blob();
  }

  async importarGrafo(nome: string, formato: string, conteudo: string): Promise<GrafoInfo> {
    return this.request<GrafoInfo>('/api/v1/persistencia/importar', {
      method: 'POST',
      body: JSON.stringify({
        nome,
        formato,
        conteudo
      }),
    });
  }
}

export const graphService = new GraphService();
