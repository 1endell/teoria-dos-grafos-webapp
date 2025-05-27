
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
  const isDraggingRef = useRef(false);

  // Atualizar referência do modo
  useEffect(() => {
    currentModeRef.current = mode;
    console.log('Mode updated in useSigmaInstance:', mode);
  }, [mode]);

  // Node Renderer customizado
  const customNodeRenderer = (
    context: CanvasRenderingContext2D,
    data: PartialButFor<NodeDisplayData, 'x' | 'y'>,
    settings: any
  ) => {
    const size = data.size || 10;
    const color = data.color || settings.defaultNodeColor;
    const label = data.label || '';

    // Desenhar círculo do nó
    context.beginPath();
    context.arc(data.x, data.y, size, 0, Math.PI * 2, true);
    context.fillStyle = color;
    context.fill();
    context.closePath();

    // Desenhar rótulo centralizado
    context.fillStyle = '#ffffff'; // Cor do rótulo (branco dentro do vértice)
    context.font = `${Math.max(size * 0.8, 10)}px sans-serif`;
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(label, data.x, data.y);
  };

  // Inicializar Sigma
  const initSigma = (graph: Graph) => {
    if (!containerRef.current) return;

    console.log('Initializing Sigma with graph order:', graph.order);

    // Layout inicial
    if (graph.order > 0) {
      if (layoutType === 'circular') {
        circular.assign(graph);
      } else if (layoutType === 'forceatlas2') {
        const settings = forceAtlas2.inferSettings(graph);
        forceAtlas2.assign(graph, { settings, iterations: 100 });
      }
    }

    const sigmaSettings = {
      renderEdgeLabels: isWeighted,
      defaultEdgeType: isDirected ? 'arrow' : 'line',
      defaultNodeColor: '#1E88E5',
      defaultEdgeColor: '#757575',
      labelSize: 14,
      labelWeight: 'bold' as const,
      minCameraRatio: 0.1,
      maxCameraRatio: 5,
      enableEdgeClickEvents: true,
      enableEdgeWheelEvents: true,
      enableEdgeHoverEvents: true,
      labelDensity: 0,
      labelGridCellSize: 0,
      labelRenderedSizeThreshold: 0,
    };

    sigmaRef.current = new Sigma(graph, containerRef.current, {
      ...sigmaSettings,
      nodeProgramClasses: {
        default: customNodeRenderer,
      }
    });
   
     window.sigmaInstance = sigmaRef.current; // Torna acessível globalmente para refresh externo

    setupSigmaEvents();
    sigmaRef.current.refresh();
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
      if (isDraggingRef.current) {
        isDraggingRef.current = false;
        return;
      }
      
      const currentMode = currentModeRef.current;
      console.log('Stage clicked, current mode:', currentMode, 'event:', event);
      
      if (currentMode === 'addNode') {
        // Obter coordenadas exatas do clique para posicionamento preciso
        const coords = sigma.viewportToGraph({
          x: event.event.offsetX,
          y: event.event.offsetY
        });
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

    // Configurar dragging de nós individuais
    let draggedNode: string | null = null;
    let isDragging = false;

    sigma.on('downNode', (event: any) => {
      if (currentModeRef.current === 'select') {
        draggedNode = event.node;
        isDragging = false;
        sigma.getGraph().setNodeAttribute(draggedNode, 'highlighted', true);
        
        // Prevent sigma to move camera
        event.preventSigmaDefault();
        event.original.preventDefault();
        event.original.stopPropagation();
      }
    });

    sigma.getMouseCaptor().on('mousemove', (event: any) => {
      if (draggedNode && currentModeRef.current === 'select') {
        isDragging = true;
        isDraggingRef.current = true;
        
        // Get new position of node
        const pos = sigma.viewportToGraph(event);
        sigma.getGraph().setNodeAttribute(draggedNode, 'x', pos.x);
        sigma.getGraph().setNodeAttribute(draggedNode, 'y', pos.y);
        
        // Prevent sigma to move camera
        event.preventSigmaDefault();
        event.original.preventDefault();
        event.original.stopPropagation();
      }
    });

    sigma.getMouseCaptor().on('mouseup', () => {
      if (draggedNode) {
        sigma.getGraph().removeNodeAttribute(draggedNode, 'highlighted');
        draggedNode = null;
        
        setTimeout(() => {
          isDraggingRef.current = false;
        }, 100);
      }
    });

    sigma.getMouseCaptor().on('mouseleave', () => {
      if (draggedNode) {
        sigma.getGraph().removeNodeAttribute(draggedNode, 'highlighted');
        draggedNode = null;
        isDraggingRef.current = false;
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
