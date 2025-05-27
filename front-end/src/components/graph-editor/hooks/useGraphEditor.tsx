import { useState, useRef } from 'react';
import Graph from 'graphology';
import { Grafo, VerticeCreate, ArestaCreate, GrafoCreate } from '@/types/graph';
import { graphService } from '@/services/graphService';
import { useToast } from '@/hooks/use-toast';
import { EditorMode, GraphEditorState, NodeProperties, EdgeProperties } from '../types';
import { generateNodeName } from '../utils';
import { useCallback, useEffect, useState, useRef } from "react";
import { useSigma } from "react-sigma-v2";
import { useSigmaInstance } from './useSigmaInstance';

export function useGraphEditor(grafoId, onSave) {
  const [state, setState] = useState({
    isDirected: true,
    isWeighted: false,
    layoutType: 'circular',
    mode: 'select',
    selectedNode: null,
    sourceNode: null,
    nodeProperties: {},
    edgeProperties: {},
    isLoading: false,
    grafoNome: ''
  });
  
  const graphRef = useRef(new Graph());
  const grafoInfo = useRef(null);
  const { refresh } = useSigmaInstance();

  useEffect(() => {
    if (grafoId) loadGrafo(grafoId);
    else initEmptyGraph();
  }, [grafoId]);

  function updateState(updates) {
    setState(prev => ({ ...prev, ...updates }));
  }

  function loadGrafo(id) {
    updateState({ isLoading: true });
    return fetch(`/api/grafos/${id}`)
      .then(res => res.json())
      .then(data => {
        const graph = new Graph();
        data.nodes.forEach(node => graph.addNode(node.id, node));
        data.edges.forEach(edge => graph.addEdge(edge.source, edge.target, edge));
        graphRef.current = graph;
        grafoInfo.current = data.info;
        updateState({
          isDirected: data.isDirected,
          isWeighted: data.isWeighted,
          layoutType: data.layoutType,
          grafoNome: data.info?.nome || ''
        });
        return graph;
      })
      .finally(() => updateState({ isLoading: false }));
  }

  function initEmptyGraph() {
    const graph = new Graph();
    graphRef.current = graph;
    return graph;
  }

  function addNode({ x, y }) {
    const id = String(graphRef.current.order + 1);
    graphRef.current.addNode(id, { label: id, x, y, size: 10, color: '#1E88E5' });
    return true;
  }

  function addEdge(source, target) {
    if (!graphRef.current.hasEdge(source, target)) {
      graphRef.current.addEdge(source, target, { label: `${source}-${target}` });
      return true;
    }
    return false;
  }

  function removeSelectedNode() {
    if (state.selectedNode && graphRef.current.hasNode(state.selectedNode)) {
      graphRef.current.dropNode(state.selectedNode);
      updateState({ selectedNode: null });
      return true;
    }
    return false;
  }

  function saveGraph() {
    const data = {
      nodes: graphRef.current.nodes().map(id => ({
        id,
        ...graphRef.current.getNodeAttributes(id)
      })),
      edges: graphRef.current.edges().map(id => {
        const [source, target] = graphRef.current.extremities(id);
        return { id, source, target, ...graphRef.current.getEdgeAttributes(id) };
      }),
      info: grafoInfo.current
    };
    onSave?.(data);
  }

  function handleModeChange(newMode) {
    updateState({ mode: newMode });
  }

  return {
    state,
    updateState,
    grafoInfo,
    graphRef,
    loadGrafo,
    initEmptyGraph,
    addNode,
    addEdge,
    removeSelectedNode,
    saveGraph,
    handleModeChange
  };
}


export const useGraphEditor = (grafoId?: string, onSave?: (grafoId: string) => void) => {
  const graphRef = useRef<Graph>(new Graph({ multi: false, type: 'directed' }));
  const { toast } = useToast();

  const [state, setState] = useState<GraphEditorState>({
    mode: 'select',
    selectedNode: null,
    sourceNode: null,
    isDirected: true,
    isWeighted: true,
    nodeCounter: 0,
    nodeProperties: { label: '', color: '#1E88E5' },
    edgeProperties: { weight: 1.0, color: '#757575' },
    isLoading: false,
    layoutType: 'circular',
    grafoNome: ''
  });

  const [grafoInfo, setGrafoInfo] = useState<Grafo | null>(null);

  const updateState = (updates: Partial<GraphEditorState>) => {
    setState(prev => ({ ...prev, ...updates }));
  };

  const loadGrafo = async (id: string) => {
    try {
      updateState({ isLoading: true });
      const grafo = await graphService.obterGrafo(id);
      setGrafoInfo(grafo);
      updateState({ isDirected: grafo.direcionado, isWeighted: grafo.ponderado, grafoNome: grafo.nome });

      const visualizacao = await graphService.obterVisualizacao(id, 'spring', true);
      const graph = new Graph({ multi: false, type: grafo.direcionado ? 'directed' : 'undirected' });

      visualizacao.vertices.forEach(v => {
        graph.addNode(v.id, {
          x: v.x,
          y: v.y,
          size: 15,
          color: v.atributos?.cor || '#1E88E5',
          label: v.atributos?.label || v.id
        });
      });

      visualizacao.arestas.forEach(a => {
        if (graph.hasNode(a.origem) && graph.hasNode(a.destino)) {
          graph.addEdge(a.origem, a.destino, {
            size: 2,
            color: a.atributos?.cor || '#757575',
            label: grafo.ponderado && a.peso !== undefined ? a.peso.toString() : '',
            weight: a.peso || 1,
            type: grafo.direcionado ? 'arrow' : 'line'
          });
        }
      });

      graphRef.current = graph;
      return graph;
    } catch (error) {
      console.error('Error loading graph:', error);
      toast({ title: "Erro", description: "Não foi possível carregar o grafo.", variant: "destructive" });
      return initEmptyGraph();
    } finally {
      updateState({ isLoading: false });
    }
  };

  const initEmptyGraph = () => {
    const graph = new Graph({ multi: false, type: state.isDirected ? 'directed' : 'undirected' });
    graphRef.current = graph;
    return graph;
  };

  const generateNodePosition = () => {
    const graph = graphRef.current;
    const minDistance = 100;
    const maxAttempts = 50;

    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      const x = Math.random() * 800 - 400;
      const y = Math.random() * 600 - 300;

      let tooClose = false;
      graph.forEachNode((nodeId, attributes) => {
        const dx = attributes.x - x;
        const dy = attributes.y - y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        if (distance < minDistance) tooClose = true;
      });

      if (!tooClose) return { x, y };
    }

    const gridSize = Math.ceil(Math.sqrt(graph.order + 1));
    const nodeIndex = graph.order;
    const gridX = (nodeIndex % gridSize) * 80 - (gridSize * 40);
    const gridY = Math.floor(nodeIndex / gridSize) * 80 - (gridSize * 40);
    return { x: gridX, y: gridY };
  };

  const addNode = (coords?: { x: number, y: number }) => {
    const graph = graphRef.current;
    const nodeId = crypto.randomUUID();

    const usedNames = new Set<string>();
    graph.forEachNode((nodeId, attributes) => {
      if (attributes.label) usedNames.add(attributes.label);
    });

    const nodeName = state.nodeProperties.label || generateNodeName(usedNames);
    const position = coords || generateNodePosition();

    try {
      graph.addNode(nodeId, {
        x: position.x,
        y: position.y,
        size: 15,
        color: state.nodeProperties.color,
        label: nodeName
      });

      updateState({ nodeProperties: { ...state.nodeProperties, label: '' } });
      toast({ title: "Sucesso", description: `Vértice ${nodeName} adicionado.` });
      return true;
    } catch (error) {
      console.error('Error adding node:', error);
      toast({ title: "Erro", description: "Erro ao adicionar vértice.", variant: "destructive" });
      return false;
    }
  };

  const addEdge = (source: string, target: string) => {
    const graph = graphRef.current;

    if (graph.hasEdge(source, target)) {
      toast({ title: "Aviso", description: "Esta aresta já existe.", variant: "default" });
      return false;
    }

    try {
      graph.addEdge(source, target, {
        size: 2,
        color: state.edgeProperties.color,
        label: state.isWeighted ? state.edgeProperties.weight.toString() : '',
        weight: state.edgeProperties.weight,
        type: state.isDirected ? 'arrow' : 'line'
      });

      // 🔥 Refresh para atualizar visualização
      if (typeof window !== 'undefined' && window.sigmaInstance) {
        window.sigmaInstance.refresh();
      }

      const sourceLabel = graph.getNodeAttribute(source, 'label');
      const targetLabel = graph.getNodeAttribute(target, 'label');
      toast({ title: "Sucesso", description: `Aresta de ${sourceLabel} para ${targetLabel} adicionada.` });
      return true;
    } catch (error) {
      console.error('Error adding edge:', error);
      toast({ title: "Erro", description: "Erro ao adicionar aresta.", variant: "destructive" });
      return false;
    }
  };

  const removeSelectedNode = () => {
    if (!state.selectedNode) return false;
    const graph = graphRef.current;
    const nodeLabel = graph.getNodeAttribute(state.selectedNode, 'label');

    try {
      graph.dropNode(state.selectedNode);
      updateState({ selectedNode: null });
      toast({ title: "Sucesso", description: `Vértice ${nodeLabel} removido.` });
      return true;
    } catch (error) {
      console.error('Error removing node:', error);
      toast({ title: "Erro", description: "Erro ao remover vértice.", variant: "destructive" });
      return false;
    }
  };

  const saveGraph = async () => {
    try {
      updateState({ isLoading: true });
      const graph = graphRef.current;
      const vertices: VerticeCreate[] = [];
      const arestas: ArestaCreate[] = [];

      graph.forEachNode((nodeId, attributes) => {
        vertices.push({ id: nodeId, atributos: { cor: attributes.color, label: attributes.label } });
      });

      graph.forEachEdge((edgeId, attributes, source, target) => {
        arestas.push({ origem: source, destino: target, peso: attributes.weight || 1.0, atributos: { cor: attributes.color } });
      });

      let resultado;

      if (grafoInfo && grafoInfo.id) {
        await graphService.atualizarGrafo(grafoInfo.id, {
          nome: state.grafoNome || grafoInfo.nome,
          direcionado: state.isDirected,
          ponderado: state.isWeighted
        });

        const currentGraph = await graphService.obterGrafo(grafoInfo.id);
        for (const vertice of currentGraph.vertices) {
          try { await graphService.removerVertice(grafoInfo.id, vertice.id); }
          catch (error) { console.log('Vertex already removed or does not exist:', vertice.id); }
        }

        for (const vertice of vertices) {
          await graphService.adicionarVertice(grafoInfo.id, vertice);
        }

        for (const aresta of arestas) {
          await graphService.adicionarAresta(grafoInfo.id, aresta);
        }

        resultado = { id: grafoInfo.id };
      } else {
        resultado = await criarNovoGrafo(vertices, arestas);
        setGrafoInfo(await graphService.obterGrafo(resultado.id));
      }

      toast({ title: "Sucesso", description: "Grafo salvo com sucesso!" });
      if (onSave && resultado) onSave(resultado.id);

    } catch (error) {
      console.error('Error saving graph:', error);
      toast({ title: "Erro", description: "Não foi possível salvar o grafo.", variant: "destructive" });
    } finally {
      updateState({ isLoading: false });
    }
  };

  const criarNovoGrafo = async (vertices: VerticeCreate[], arestas: ArestaCreate[]) => {
    const grafoNome = state.grafoNome || `Grafo Visual ${new Date().toLocaleString()}`;
    const novoGrafo: GrafoCreate = { nome: grafoNome, direcionado: state.isDirected, ponderado: state.isWeighted, vertices, arestas };
    return await graphService.criarGrafo(novoGrafo);
  };

  const handleModeChange = (newMode: EditorMode) => {
    updateState({ mode: newMode, selectedNode: null, sourceNode: null });
  };

  return {
    state,
    updateState,
    grafoInfo,
    graphRef,
    loadGrafo,
    initEmptyGraph,
    addNode,
    addEdge,
    removeSelectedNode,
    saveGraph,
    handleModeChange
  };
};
