import React, { useEffect, useRef } from 'react';
import Graph from 'graphology';
import GraphEditorToolbar from './graph-editor/GraphEditorToolbar';
import GraphEditorCanvas from './graph-editor/GraphEditorCanvas';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { useGraphEditor } from './graph-editor/hooks/useGraphEditor';
import { useSigmaInstance } from './graph-editor/hooks/useSigmaInstance';
import { GraphEditorProps } from './graph-editor/types';

const GraphEditor: React.FC<GraphEditorProps> = ({ grafoId, onSave }) => {
  const containerRef = useRef<HTMLDivElement>(null);

  const {
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
  } = useGraphEditor(grafoId, onSave);

  const {
    sigmaRef,
    initSigma,
    applyLayout,
    resetZoom,
    refresh
  } = useSigmaInstance({
    containerRef,
    graph: graphRef.current,
    isDirected: state.isDirected,
    isWeighted: state.isWeighted,
    layoutType: state.layoutType,
    mode: state.mode,
    selectedNode: state.selectedNode,
    sourceNode: state.sourceNode,
    onNodeClick: (nodeId: string) => {
      if (state.sourceNode && state.sourceNode !== nodeId) {
        const success = addEdge(state.sourceNode, nodeId);
        if (success) {
          refresh();
        }
      }
    },
    onStageClick: (coords: {x: number, y: number}) => {
      const success = addNode(coords);
      if (success) {
        refresh();
      }
    },
    onModeChange: handleModeChange,
    onSelectedNodeChange: (nodeId: string | null) => {
      updateState({ selectedNode: nodeId });
    },
    onSourceNodeChange: (nodeId: string | null) => {
      updateState({ sourceNode: nodeId });
    }
  });

  useEffect(() => {
    console.log('GraphEditor useEffect triggered');
    if (!containerRef.current) {
      console.log('Container ref not available');
      return;
    }

    if (sigmaRef.current) {
      console.log('Cleaning previous sigma instance');
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }

    if (grafoId) {
      console.log('Loading existing graph:', grafoId);
      loadGrafo(grafoId).then((graph) => {
        if (graph) {
          initSigma(graph);
        }
      });
    } else {
      console.log('Initializing empty graph');
      const graph = initEmptyGraph();
      initSigma(graph);
    }

    return () => {
      if (sigmaRef.current) {
        sigmaRef.current.kill();
        sigmaRef.current = null;
      }
    };
  }, [grafoId]);

  const toggleDirected = () => {
    const newIsDirected = !state.isDirected;
    updateState({ isDirected: newIsDirected });

    const oldGraph = graphRef.current;
    const newGraph = new Graph({ multi: false, type: newIsDirected ? 'directed' : 'undirected' });

    oldGraph.forEachNode((nodeId, attributes) => {
      newGraph.addNode(nodeId, attributes);
    });

    oldGraph.forEachEdge((edgeId, attributes, source, target) => {
      const newAttributes = {
        ...attributes,
        type: newIsDirected ? 'arrow' : 'line'
      };
      newGraph.addEdge(source, target, newAttributes);
    });

    graphRef.current = newGraph;
    if (sigmaRef.current) {
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }
    initSigma(newGraph);
  };

  const toggleWeighted = () => {
    const newIsWeighted = !state.isWeighted;
    updateState({ isWeighted: newIsWeighted });

    if (sigmaRef.current) {
      sigmaRef.current.setSetting('renderEdgeLabels', newIsWeighted);
      sigmaRef.current.refresh();
    }
  };

  const handleApplyLayout = (type: string) => {
    updateState({ layoutType: type });
    applyLayout(type);
  };

  const handleRemoveSelectedNode = () => {
    const success = removeSelectedNode();
    if (success && sigmaRef.current) {
      sigmaRef.current.refresh();
    }
  };

  const handleContainerRef = (ref: React.RefObject<HTMLDivElement>) => {
    containerRef.current = ref.current;
  };

  return (
    <div className="flex flex-col h-full">
      <GraphEditorToolbar
        mode={state.mode}
        isDirected={state.isDirected}
        isWeighted={state.isWeighted}
        selectedNode={state.selectedNode}
        isLoading={state.isLoading}
        onModeChange={handleModeChange}
        onToggleDirected={toggleDirected}
        onToggleWeighted={toggleWeighted}
        onApplyLayout={handleApplyLayout}
        onResetZoom={resetZoom}
        onRemoveSelectedNode={handleRemoveSelectedNode}
        onSaveGraph={saveGraph}
        nodeProperties={state.nodeProperties}
        edgeProperties={state.edgeProperties}
        onNodePropertiesChange={(properties) => updateState({ nodeProperties: properties })}
        onEdgePropertiesChange={(properties) => updateState({ edgeProperties: properties })}
      />

      <div className="flex flex-1 overflow-hidden">
        <GraphEditorCanvas
          mode={state.mode}
          sourceNode={state.sourceNode}
          isLoading={state.isLoading}
          onContainerRef={handleContainerRef}
        />

        <GraphPlatformSidebar
          graph={graphRef.current}
          selectedNode={state.selectedNode}
          isWeighted={state.isWeighted}
          nodeProperties={state.nodeProperties}
          edgeProperties={state.edgeProperties}
          onNodePropertiesChange={(properties) => updateState({ nodeProperties: properties })}
          onEdgePropertiesChange={(properties) => updateState({ edgeProperties: properties })}
          onRemoveSelectedNode={handleRemoveSelectedNode}
        />
      </div>
    </div>
  );
};

export default GraphEditor;
