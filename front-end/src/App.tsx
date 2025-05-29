import React, { useCallback, useState } from 'react';
import {
  Background,
  ReactFlow,
  addEdge,
  useNodesState,
  useEdgesState,
  ReactFlowProvider
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import CustomNode from './components/graph-editor/CustomNode';
import CustomFloatingEdge from './components/graph-editor/CustomFloatingEdge';
import CustomConnectionLine from './components/graph-editor/CustomConnectionLine';

const initialNodes = [ /* seus nós iniciais */ ];
const initialEdges = [];

const AppContent = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params, type: 'floating' }, eds)),
    [setEdges]
  );

  return (
    <ReactFlow
      nodes={nodes}
      edges={edges}
      onNodesChange={onNodesChange}
      onEdgesChange={onEdgesChange}
      onConnect={onConnect}
      nodeTypes={{ custom: CustomNode }}
      edgeTypes={{ floating: CustomFloatingEdge }}
      connectionLineComponent={CustomConnectionLine}
      connectionMode="loose"
      fitView
      style={{ width: '100%', height: '100%' }}
    >
      <Background />
    </ReactFlow>
  );
};

const App = () => (
  <ReactFlowProvider>
    <div style={{ width: '100vw', height: '100vh' }}>
      <AppContent />
    </div>
  </ReactFlowProvider>
);

export default App;
