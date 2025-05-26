
import { useRef, useEffect } from 'react';
import Graph from 'graphology';
import { Sigma } from 'sigma';
import { circular } from 'graphology-layout';
import forceAtlas2 from 'graphology-layout-forceatlas2';
import { EditorMode } from '../types';

interface UseSigmaInstanceProps {
  containerRef: React.RefObject<HTMLDivElement>;
  graph: Graph;
  isDirected: boolean;
  isWeighted: boolean;
  layoutType: string;
  mode: EditorMode;
  selectedNode: string | null;
  sourceNode: string | null;
  onNodeClick: (nodeId: string) => void;
  onStageClick: (coords: {x: number, y: number}) => void;
  onModeChange: (mode: EditorMode) => void;
  onSelectedNodeChange: (nodeId: string | null) => void;
  onSourceNodeChange: (nodeId: string | null) => void;
}

export const useSigmaInstance = ({
  containerRef,
  graph,
  isDirected,
  isWeighted,
  layoutType,
  mode,
  selectedNode,
  sourceNode,
  onNodeClick,
  onStageClick,
  onModeChange,
  onSelectedNodeChange,
  onSourceNodeChange
}: UseSigmaInstanceProps) => {
  const sigmaRef = useRef<Sigma | null>(null);
  const currentModeRef = useRef<EditorMode>(mode);

  // Atualizar referência do modo
  useEffect(() => {
    currentModeRef.current = mode;
    console.log('Mode updated in useSigmaInstance:', mode);
  }, [mode]);

  // Inicializar Sigma
  const initSigma = (graph: Graph) => {
    if (!containerRef.current) {
      console.log('Container not available for sigma init');
      return;
    }
    
    console.log('Initializing Sigma with graph order:', graph.order);
    
    try {
      // Aplicar layout se o grafo tiver nós
      if (graph.order > 0) {
        if (layoutType === 'circular') {
          circular.assign(graph);
        } else if (layoutType === 'forceatlas2') {
          const settings = forceAtlas2.inferSettings(graph);
          forceAtlas2.assign(graph, { settings, iterations: 100 });
        }
      }
      
      // Configuração do Sigma
      const sigmaSettings = {
        renderEdgeLabels: isWeighted,
        defaultEdgeType: isDirected ? 'arrow' : 'line',
        defaultNodeColor: '#1E88E5',
        defaultEdgeColor: '#757575',
        labelSize: 14,
        labelWeight: 'bold' as const,
        minCameraRatio: 0.1,
        maxCameraRatio: 5,
      };
      
      console.log('Creating Sigma instance with settings:', sigmaSettings);
      
      // Inicializar Sigma
      sigmaRef.current = new Sigma(graph, containerRef.current, sigmaSettings);
      
      console.log('Sigma instance created successfully');
      
      // Configurar eventos
      setupSigmaEvents();
      
      // Refresh para garantir que tudo seja renderizado
      sigmaRef.current.refresh();
      
    } catch (error) {
      console.error('Error initializing Sigma:', error);
    }
  };

  // Configurar eventos do Sigma
  const setupSigmaEvents = () => {
    if (!sigmaRef.current) {
      console.log('No sigma instance for event setup');
      return;
    }
    
    console.log('Setting up Sigma events');
    const sigma = sigmaRef.current;
    
    // Evento de clique no canvas
    sigma.on('clickStage', (event: any) => {
      const currentMode = currentModeRef.current;
      console.log('Stage clicked, current mode:', currentMode, 'event:', event);
      
      if (currentMode === 'addNode') {
        // Obter coordenadas corretas do clique
        const coords = sigma.viewportToGraph(event);
        console.log('Adding node at coordinates:', coords);
        onStageClick(coords);
      } else if (currentMode === 'select') {
        onSelectedNodeChange(null);
        onSourceNodeChange(null);
      }
    });
    
    // Evento de clique em nó
    sigma.on('clickNode', (event: any) => {
      const nodeId = event.node;
      const currentMode = currentModeRef.current;
      console.log('Node clicked:', nodeId, 'current mode:', currentMode);
      
      if (currentMode === 'select') {
        onSelectedNodeChange(nodeId);
      } else if (currentMode === 'addEdge') {
        if (sourceNode === null) {
          onSourceNodeChange(nodeId);
          console.log('Source node selected:', nodeId);
        } else if (sourceNode !== nodeId) {
          console.log('Target node selected, creating edge:', sourceNode, '->', nodeId);
          onNodeClick(nodeId);
          onSourceNodeChange(null);
        }
      }
    });
  };

  // Aplicar layout
  const applyLayout = (type: string) => {
    if (graph.order === 0) return;
    
    try {
      if (type === 'circular') {
        circular.assign(graph);
      } else if (type === 'forceatlas2') {
        const settings = forceAtlas2.inferSettings(graph);
        forceAtlas2.assign(graph, { settings, iterations: 100 });
      }
      
      if (sigmaRef.current) {
        sigmaRef.current.refresh();
      }
    } catch (error) {
      console.error('Error applying layout:', error);
    }
  };

  // Resetar zoom
  const resetZoom = () => {
    if (sigmaRef.current) {
      const camera = sigmaRef.current.getCamera();
      camera.animatedReset();
    }
  };

  // Refresh sigma
  const refresh = () => {
    if (sigmaRef.current) {
      sigmaRef.current.refresh();
    }
  };

  return {
    sigmaRef,
    initSigma,
    applyLayout,
    resetZoom,
    refresh
  };
};
