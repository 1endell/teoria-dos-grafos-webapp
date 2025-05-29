import React, { useState, useCallback } from 'react';
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
];
const initialEdges = [];

const nodeTypes = { custom: CustomNode };
const edgeTypes = { floating: CustomFloatingEdge };

const connectionLineStyle = { stroke: '#000', strokeWidth: 2 };

const App = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mode, setMode] = useState('move'); // 'move', 'addNode', 'addEdge'

  const onConnect = useCallback(
    (params) => {
      if (mode === 'addEdge') {
        setEdges((eds) => addEdge({ ...params, type: 'floating' }, eds));
      }
    },
    [setEdges, mode]
  );

  const onPaneClick = useCallback(
    (event) => {
      if (mode === 'addNode') {
        const newNode = {
          id: `${+new Date()}`,
          type: 'custom',
          position: { x: event.clientX - 100, y: event.clientY - 40 },
        };
        setNodes((nds) => [...nds, newNode]);
      }
    },
    [mode, setNodes]
  );

  return (
    <div style={{ display: 'flex', width: '100vw', height: '100vh' }}>
      <div style={{ flexGrow: 1, position: 'relative' }}>
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
          style={{ width: '100%', height: '100%' }}
          connectionMode={mode === 'addEdge' ? 'loose' : 'invalid'}
          onPaneClick={onPaneClick}
        >
          <Background />
        </ReactFlow>

        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          style={{
            position: 'absolute',
            top: 10,
            right: sidebarOpen ? 210 : 10,
            zIndex: 10,
            padding: '5px 10px',
            cursor: 'pointer',
          }}
        >
          {sidebarOpen ? 'Fechar' : 'Abrir'}
        </button>
      </div>

      {sidebarOpen && (
        <div
          style={{
            width: 200,
            background: '#f5f5f5',
            borderLeft: '1px solid #ccc',
            padding: 10,
            boxSizing: 'border-box',
          }}
        >
          <h3>Ferramentas</h3>
          <button onClick={() => setMode('move')} style={{ display: 'block', marginBottom: 10 }}>
            Mover Vértice
          </button>
          <button onClick={() => setMode('addNode')} style={{ display: 'block', marginBottom: 10 }}>
            Adicionar Vértice
          </button>
          <button onClick={() => setMode('addEdge')} style={{ display: 'block' }}>
            Adicionar Aresta
          </button>
          <p style={{ marginTop: 10 }}>Modo atual: {mode}</p>
        </div>
      )}
    </div>
  );
};

export default App;
