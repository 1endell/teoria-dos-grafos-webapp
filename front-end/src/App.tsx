import React, { useCallback } from 'react';
import {
  Background,
  ReactFlow,
  addEdge,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';

import CustomNode from './components/graph-editor/CustomNode';
import CustomFloatingEdge from './components/graph-editor/CustomFloatingEdge';
import CustomConnectionLine from './components/graph-editor/CustomConnectionLine';

const initialNodes = [
  { id: '1', type: 'custom', position: { x: 100, y: 100 } },
  { id: '2', type: 'custom', position: { x: 300, y: 200 } },
  { id: '3', type: 'custom', position: { x: 200, y: 400 } },
  { id: '4', type: 'custom', position: { x: 500, y: 300 } },
];

const initialEdges = [];

const nodeTypes = { custom: CustomNode };
const edgeTypes = { floating: CustomFloatingEdge };

const connectionLineStyle = { stroke: '#000', strokeWidth: 2 };

const App = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge({ ...params, type: 'floating' }, eds)),
    [setEdges]
  );

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        nodeTypes={nodeTypes}
        edgeTypes={edgeTypes}
        connectionLineComponent={CustomConnectionLine}
        connectionLineStyle={connectionLineStyle}
        connectionMode="loose"  // Permite conexões em toda a área do vértice
        style={{ width: '100%', height: '100%' }}
      >
        <Background />
      </ReactFlow>
    </div>
  );
};

export default App;
