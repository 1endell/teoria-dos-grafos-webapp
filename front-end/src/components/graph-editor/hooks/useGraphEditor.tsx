
import { useState, useRef } from 'react';
import Graph from 'graphology';
import { Grafo, VerticeCreate, ArestaCreate, GrafoCreate } from '@/types/graph';
import { graphService } from '@/services/graphService';
import { useToast } from '@/hooks/use-toast';
import { EditorMode, GraphEditorState, NodeProperties, EdgeProperties } from '../types';
import { generateNodeName } from '../utils';

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
    layoutType: 'circular'
  });

  const [grafoInfo, setGrafoInfo] = useState<Grafo | null>(null);

  const updateState = (updates: Partial<GraphEditorState>) => {
    console.log('Updating state:', updates);
    setState(prev => {
      const newState = { ...prev, ...updates };
      console.log('New state:', newState);
      return newState;
    });
  };

  // Carregar grafo existente
  const loadGrafo = async (id: string) => {
    try {
      updateState({ isLoading: true });
      console.log('Loading graph data for ID:', id);
      const grafo = await graphService.obterGrafo(id);
      setGrafoInfo(grafo);
      updateState({ 
        isDirected: grafo.direcionado,
        isWeighted: grafo.ponderado 
      });
      
      // Obter visualização para posições dos nós
      const visualizacao = await graphService.obterVisualizacao(id, 'spring', true);
      
      // Criar novo grafo
      const graph = new Graph({ multi: false, type: grafo.direcionado ? 'directed' : 'undirected' });
      
      // Adicionar vértices
      visualizacao.vertices.forEach(v => {
        graph.addNode(v.id, {
          x: v.x,
          y: v.y,
          size: 10,
          color: v.atributos?.cor || '#1E88E5',
          label: v.id
        });
      });
      
      // Adicionar arestas
      visualizacao.arestas.forEach(a => {
        if (graph.hasNode(a.origem) && graph.hasNode(a.destino)) {
          graph.addEdge(a.origem, a.destino, {
            size: 2,
            color: '#757575',
            label: a.peso !== undefined ? a.peso.toString() : '',
            weight: a.peso || 1,
            type: grafo.direcionado ? 'arrow' : 'line'
          });
        }
      });
      
      // Atualizar contador de nós
      const nodeIds = graph.nodes();
      if (nodeIds.length > 0) {
        const numericIds = nodeIds
          .filter(id => /^\d+$/.test(id))
          .map(id => parseInt(id, 10));
        
        if (numericIds.length > 0) {
          updateState({ nodeCounter: Math.max(...numericIds) + 1 });
        }
      }
      
      graphRef.current = graph;
      return graph;
      
    } catch (error) {
      console.error('Error loading graph:', error);
      toast({
        title: "Erro",
        description: "Não foi possível carregar o grafo.",
        variant: "destructive",
      });
      return initEmptyGraph();
    } finally {
      updateState({ isLoading: false });
    }
  };

  // Inicializar grafo vazio
  const initEmptyGraph = () => {
    console.log('Initializing empty graph');
    const graph = new Graph({ multi: false, type: state.isDirected ? 'directed' : 'undirected' });
    graphRef.current = graph;
    return graph;
  };

  // Adicionar nó
  const addNode = (coords: {x: number, y: number}) => {
    console.log('Adding node called with coords:', coords, 'current mode:', state.mode);
    
    const graph = graphRef.current;
    const nodeId = state.nodeCounter.toString();
    
    // Coletar nomes já utilizados
    const usedNames = new Set<string>();
    graph.forEachNode((nodeId, attributes) => {
      if (attributes.label) {
        usedNames.add(attributes.label);
      }
    });
    
    const nodeName = state.nodeProperties.label || generateNodeName(usedNames);
    
    console.log('Adding node:', { nodeId, nodeName, coords });
    
    try {
      // Verificar se o nó já existe
      if (graph.hasNode(nodeId)) {
        console.log('Node already exists, incrementing counter');
        const newNodeId = (state.nodeCounter + 1).toString();
        
        graph.addNode(newNodeId, {
          x: coords.x,
          y: coords.y,
          size: 15,
          color: state.nodeProperties.color,
          label: nodeName
        });
        
        updateState({ nodeCounter: state.nodeCounter + 2 });
      } else {
        graph.addNode(nodeId, {
          x: coords.x,
          y: coords.y,
          size: 15,
          color: state.nodeProperties.color,
          label: nodeName
        });
        
        updateState({ nodeCounter: state.nodeCounter + 1 });
      }
      
      // Limpar o rótulo após adicionar
      updateState({ 
        nodeProperties: { ...state.nodeProperties, label: '' }
      });
      
      toast({
        title: "Sucesso",
        description: `Vértice ${nodeName} adicionado.`,
      });
      
      console.log('Node added successfully');
      return true;
    } catch (error) {
      console.error('Error adding node:', error);
      toast({
        title: "Erro",
        description: "Erro ao adicionar vértice.",
        variant: "destructive",
      });
      return false;
    }
  };

  // Adicionar aresta
  const addEdge = (source: string, target: string) => {
    const graph = graphRef.current;
    
    if (graph.hasEdge(source, target)) {
      toast({
        title: "Aviso",
        description: "Esta aresta já existe.",
        variant: "default",
      });
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
      
      const sourceLabel = graph.getNodeAttribute(source, 'label');
      const targetLabel = graph.getNodeAttribute(target, 'label');
      
      toast({
        title: "Sucesso",
        description: `Aresta de ${sourceLabel} para ${targetLabel} adicionada.`,
      });
      
      return true;
    } catch (error) {
      console.error('Error adding edge:', error);
      toast({
        title: "Erro",
        description: "Erro ao adicionar aresta.",
        variant: "destructive",
      });
      return false;
    }
  };

  // Remover nó selecionado
  const removeSelectedNode = () => {
    if (!state.selectedNode) return;
    
    const graph = graphRef.current;
    const nodeLabel = graph.getNodeAttribute(state.selectedNode, 'label');
    
    try {
      graph.dropNode(state.selectedNode);
      updateState({ selectedNode: null });
      
      toast({
        title: "Sucesso",
        description: `Vértice ${nodeLabel} removido.`,
      });
      
      return true;
    } catch (error) {
      console.error('Error removing node:', error);
      toast({
        title: "Erro",
        description: "Erro ao remover vértice.",
        variant: "destructive",
      });
      return false;
    }
  };

  // Salvar grafo
  const saveGraph = async () => {
    try {
      updateState({ isLoading: true });
      
      const graph = graphRef.current;
      const vertices: VerticeCreate[] = [];
      const arestas: ArestaCreate[] = [];
      
      // Coletar vértices
      graph.forEachNode((nodeId, attributes) => {
        vertices.push({
          id: nodeId,
          atributos: {
            cor: attributes.color,
            label: attributes.label
          }
        });
      });
      
      // Coletar arestas
      graph.forEachEdge((edgeId, attributes, source, target) => {
        arestas.push({
          origem: source,
          destino: target,
          peso: attributes.weight || 1.0,
          atributos: {
            cor: attributes.color
          }
        });
      });
      
      // Criar novo grafo
      const resultado = await criarNovoGrafo(vertices, arestas);
      
      toast({
        title: "Sucesso",
        description: "Grafo salvo com sucesso!",
      });
      
      if (onSave && resultado) {
        onSave(resultado.id);
      }
      
    } catch (error) {
      console.error('Error saving graph:', error);
      toast({
        title: "Erro",
        description: "Não foi possível salvar o grafo.",
        variant: "destructive",
      });
    } finally {
      updateState({ isLoading: false });
    }
  };

  // Criar novo grafo
  const criarNovoGrafo = async (vertices: VerticeCreate[], arestas: ArestaCreate[]) => {
    const novoGrafo: GrafoCreate = {
      nome: grafoInfo?.nome || `Grafo Visual ${new Date().toLocaleString()}`,
      direcionado: state.isDirected,
      ponderado: state.isWeighted,
      vertices,
      arestas
    };
    
    return await graphService.criarGrafo(novoGrafo);
  };

  // Função para alterar modo
  const handleModeChange = (newMode: EditorMode) => {
    console.log('handleModeChange called: changing from', state.mode, 'to', newMode);
    updateState({ 
      mode: newMode,
      selectedNode: null,
      sourceNode: null 
    });
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
