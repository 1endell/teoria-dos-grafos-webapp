import { useRef, useEffect } from 'react';
import Graph from 'graphology';
import { Sigma } from 'sigma';
import { circular } from 'graphology-layout';
import forceAtlas2 from 'graphology-layout-forceatlas2';
import { EditorMode } from '../types';

export function useSigmaInstance({ containerRef, graph, isDirected, isWeighted, layoutType, mode, selectedNode, sourceNode, onNodeClick, onStageClick, onModeChange, onSelectedNodeChange, onSourceNodeChange }) {
  const sigmaRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    if (sigmaRef.current) {
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }

    sigmaRef.current = new Sigma(graph, containerRef.current, {
      renderEdgeLabels: isWeighted,
      defaultEdgeType: isDirected ? 'arrow' : 'line',
      labelColor: 'default',
      defaultNodeColor: '#1E88E5',
      defaultEdgeColor: '#757575'
    });

    sigmaRef.current.on('clickNode', e => {
      onNodeClick?.(e.node);
    });

    sigmaRef.current.on('clickStage', e => {
      onStageClick?.(sigmaRef.current.viewportToGraph(e.event));
    });

    return () => {
      if (sigmaRef.current) {
        sigmaRef.current.kill();
        sigmaRef.current = null;
      }
    };
  }, [containerRef, graph, isDirected, isWeighted, layoutType]);

  function applyLayout(type) {
    // Layout logic to be implemented here
    sigmaRef.current.refresh();
  }

  function resetZoom() {
    sigmaRef.current.getCamera().animatedReset();
  }

  function refresh() {
    sigmaRef.current.refresh();
  }

  return { sigmaRef, initSigma: graph => sigmaRef.current && sigmaRef.current.refresh(), applyLayout, resetZoom, refresh };
}

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
  onStageClick: (coords: { x: number, y: number }) => void;
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

  useEffect(() => {
    currentModeRef.current = mode;
    console.log('Mode updated in useSigmaInstance:', mode);
  }, [mode]);

  const initSigma = (graph: Graph) => {
    if (!containerRef.current) return;
    console.log('Initializing Sigma with graph order:', graph.order);

    if (graph.order > 0) {
      if (layoutType === 'circular') {
        circular.assign(graph);
      } else if (layoutType === 'forceatlas2') {
        const settings = forceAtlas2.inferSettings(graph);
        forceAtlas2.assign(graph, { settings, iterations: 100 });
      }
    }

    const nodeReducer = (node, data) => {
      return {
        ...data,
        label: data.label || node,
        color: data.color || '#1E88E5',
        labelColor: '#FFFFFF', // Label branco dentro do nó
        labelSize: data.size * 0.5, // Tamanho proporcional ao nó
      };
    };

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
      nodeReducer
    };

    sigmaRef.current = new Sigma(graph, containerRef.current, sigmaSettings);
    window.sigmaInstance = sigmaRef.current;

    setupSigmaEvents();
    sigmaRef.current.refresh();
  };

  const setupSigmaEvents = () => {
    if (!sigmaRef.current) return;
    console.log('Setting up Sigma events');
    const sigma = sigmaRef.current;

    sigma.on('clickStage', (event: any) => {
      if (isDraggingRef.current) {
        isDraggingRef.current = false;
        return;
      }

      const currentMode = currentModeRef.current;
      if (currentMode === 'addNode') {
        const coords = sigma.viewportToGraph({
          x: event.event.offsetX,
          y: event.event.offsetY
        });
        onStageClick(coords);
      } else if (currentMode === 'select') {
        onSelectedNodeChange(null);
        onSourceNodeChange(null);
      }
    });

    sigma.on('clickNode', (event: any) => {
      const nodeId = event.node;
      const currentMode = currentModeRef.current;

      if (currentMode === 'select') {
        onSelectedNodeChange(nodeId);
      } else if (currentMode === 'addEdge') {
        if (sourceNode === null) {
          onSourceNodeChange(nodeId);
        } else if (sourceNode !== nodeId) {
          onNodeClick(nodeId);
          onSourceNodeChange(null);
        }
      }
    });

    let draggedNode: string | null = null;

    sigma.on('downNode', (event: any) => {
      if (currentModeRef.current === 'select') {
        draggedNode = event.node;
        sigma.getGraph().setNodeAttribute(draggedNode, 'highlighted', true);
        event.preventSigmaDefault();
        event.original.preventDefault();
        event.original.stopPropagation();
      }
    });

    sigma.getMouseCaptor().on('mousemove', (event: any) => {
      if (draggedNode && currentModeRef.current === 'select') {
        isDraggingRef.current = true;
        const pos = sigma.viewportToGraph(event);
        sigma.getGraph().setNodeAttribute(draggedNode, 'x', pos.x);
        sigma.getGraph().setNodeAttribute(draggedNode, 'y', pos.y);
        event.preventSigmaDefault();
        event.original.preventDefault();
        event.original.stopPropagation();
      }
    });

    sigma.getMouseCaptor().on('mouseup', () => {
      if (draggedNode) {
        sigma.getGraph().removeNodeAttribute(draggedNode, 'highlighted');
        draggedNode = null;
        setTimeout(() => { isDraggingRef.current = false; }, 100);
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

  const resetZoom = () => {
    if (sigmaRef.current) {
      const camera = sigmaRef.current.getCamera();
      camera.animatedReset();
    }
  };

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
