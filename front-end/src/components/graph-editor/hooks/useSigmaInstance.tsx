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
  const isDraggingRef = useRef(false);
  const draggedNodeRef = useRef<string | null>(null);
  const modeRef = useRef<EditorMode>(mode);

  useEffect(() => {
    modeRef.current = mode;
  }, [mode]);

  useEffect(() => {
    if (!containerRef.current) return;

    if (sigmaRef.current) {
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }

    const nodeReducer = (node, data) => ({
      ...data,
      label: data.label || node,
      color: data.color || '#1E88E5',
      labelColor: '#FFFFFF',
      labelSize: data.size ? data.size * 0.5 : 7
    });

    const sigmaSettings = {
      renderEdgeLabels: isWeighted,
      defaultEdgeType: isDirected ? 'arrow' : 'line',
      defaultNodeColor: '#1E88E5',
      defaultEdgeColor: '#757575',
      nodeReducer
    };

    sigmaRef.current = new Sigma(graph, containerRef.current, sigmaSettings);
    window.sigmaInstance = sigmaRef.current;

    setupEvents();
    applyLayout(layoutType);
    sigmaRef.current.refresh();

    return () => {
      sigmaRef.current?.kill();
      sigmaRef.current = null;
    };
  }, [containerRef, graph, isDirected, isWeighted, layoutType]);

  const setupEvents = () => {
    if (!sigmaRef.current) return;
    const sigma = sigmaRef.current;

    sigma.on('clickStage', e => {
      if (modeRef.current === 'addNode') {
        const coords = sigma.viewportToGraph(e.event);
        onStageClick(coords);
      } else if (modeRef.current === 'select') {
        onSelectedNodeChange(null);
        onSourceNodeChange(null);
      }
    });

    sigma.on('clickNode', e => {
      const nodeId = e.node;
      if (modeRef.current === 'select') {
        onSelectedNodeChange(nodeId);
      } else if (modeRef.current === 'addEdge') {
        if (!sourceNode) {
          onSourceNodeChange(nodeId);
        } else if (sourceNode !== nodeId) {
          onNodeClick(nodeId);  // target node
          onSourceNodeChange(null);
        }
      }
    });

    // Arrastar nós individualmente no modo SELECT
    sigma.on('downNode', e => {
      if (modeRef.current === 'select') {
        draggedNodeRef.current = e.node;
        isDraggingRef.current = false;
        e.preventSigmaDefault();
      }
    });

    sigma.getMouseCaptor().on('mousemove', e => {
      if (draggedNodeRef.current && modeRef.current === 'select') {
        isDraggingRef.current = true;
        const pos = sigmaRef.current!.viewportToGraph(e);
        graph.setNodeAttribute(draggedNodeRef.current, 'x', pos.x);
        graph.setNodeAttribute(draggedNodeRef.current, 'y', pos.y);
      }
    });

    sigma.getMouseCaptor().on('mouseup', () => {
      if (draggedNodeRef.current) {
        draggedNodeRef.current = null;
        setTimeout(() => { isDraggingRef.current = false; }, 100);
      }
    });

    sigma.getMouseCaptor().on('mouseleave', () => {
      draggedNodeRef.current = null;
      isDraggingRef.current = false;
    });
  };

  const applyLayout = (type: string) => {
    if (graph.order === 0) return;
    if (type === 'circular') circular.assign(graph);
    else if (type === 'forceatlas2') {
      const settings = forceAtlas2.inferSettings(graph);
      forceAtlas2.assign(graph, { settings, iterations: 100 });
    }
  };

  const resetZoom = () => sigmaRef.current?.getCamera().animatedReset();
  const refresh = () => sigmaRef.current?.refresh();

  return { sigmaRef, applyLayout, resetZoom, refresh };
};
