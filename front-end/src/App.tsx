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
  { id: '1', type: 'custom', position: { x: 0, y: 0 } },
  { id: '2', type: 'custom', position: { x: 250, y: 320 } },
  { id: '3', type: 'custom', position: { x: 40, y: 300 } },
  { id: '4', type: 'custom', position: { x: 300, y: 0 } },
];

const initialEdges = [];

const nodeTypes = { custom: CustomNode };
const edgeTypes = { floating: FloatingEdge };

const connectionLineStyle = { stroke: '#000', strokeWidth: 2 };

const EasyConnectExample = () => {
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
      fitView
      nodeTypes={nodeTypes}
      edgeTypes={edgeTypes}
      connectionLineComponent={CustomConnectionLine}
      connectionLineStyle={connectionLineStyle}
    >
      <Background />
    </ReactFlow>
  );
};

export default EasyConnectExample;
