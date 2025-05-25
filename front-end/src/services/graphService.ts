
import { GrafoCreate, GrafoInfo, Grafo, VerticeCreate, ArestaCreate, DadosVisualizacao, ResultadoAlgoritmo } from '@/types/graph';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://api-grafos:8010';

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

  async obterVisualizacao(grafoId: string, layout = 'spring'): Promise<DadosVisualizacao> {
    return this.request<DadosVisualizacao>(`/api/v1/visualizacao/${grafoId}?layout=${layout}`);
  }

  async listarAlgoritmos(): Promise<any[]> {
    return this.request<any[]>('/api/v1/algoritmos/');
  }

  async executarAlgoritmo(algoritmoId: string, grafoId: string, parametros = {}): Promise<ResultadoAlgoritmo> {
    return this.request<ResultadoAlgoritmo>(`/api/v1/algoritmos/${algoritmoId}/${grafoId}`, {
      method: 'POST',
      body: JSON.stringify({ parametros }),
    });
  }
}

export const graphService = new GraphService();
