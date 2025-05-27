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
