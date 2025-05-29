import React, { useState, useEffect, useRef, useCallback } from 'react';
import { SidebarProvider } from '@/components/ui/sidebar';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import GraphEditorToolbarReactFlow from './graph-editor/GraphEditorToolbarReactFlow';
import ReactFlow, {
  MiniMap, Controls, Background,
  useNodesState, useEdgesState, addEdge, Connection, Edge, Node
} from 'reactflow';
import 'reactflow/dist/style.css';

const REPULSION_FORCE = 5000;
const DAMPING = 0.9;

const GraphMainEditor: React.FC = () => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const { toast } = useToast();
  const [graphName, setGraphName] = useState('Novo Grafo');

  const [nodes, setNodes, onNodesChange] = useNodesState<Node[]>([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState<Edge[]>([]);
  const animationRef = useRef<number | null>(null);

  const alphabet = 'abcdefghijklmnopqrstuvwxyz';
  const getNextLabel = () => {
    const count = nodes.length;
    let label = '';
    let n = count;
    do {
      label = alphabet[n % 26] + label;
      n = Math.floor(n / 26) - 1;
    } while (n >= 0);
    return label;
  };

  const handleAddNode = () => {
    const id = `${+new Date()}`;
    const label = getNextLabel();
    const newNode: Node = {
      id,
      data: { label },
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      type: 'custom',
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const onConnect = useCallback((params: Edge | Connection) => {
    setEdges((eds) => addEdge(params, eds));
  }, [setEdges]);

  const handleResetView = () => {
    toast({ title: "Resetar Visão", description: "Visão resetada", variant: "default" });
  };

  const handleSaveGraph = () => {
    const graphData = { nodes, edges, name: graphName };
    console.log("Graph Saved:", graphData);
    toast({ title: "Grafo salvo", description: "Os dados foram salvos no console.", variant: "success" });
  };

  const handleTitleEdit = () => setIsEditingTitle(true);
  const handleTitleSave = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const newName = (e.target as HTMLInputElement).value.trim();
      if (newName) {
        setGraphName(newName);
        setIsEditingTitle(false);
      } else {
        toast({ title: "Erro", description: "Nome do grafo não pode estar vazio.", variant: "destructive" });
      }
    } else if (e.key === 'Escape') {
      setIsEditingTitle(false);
    }
  };

  // Física de repulsão simples
  const applyPhysics = () => {
    const updatedNodes = [...nodes];

    for (let i = 0; i < updatedNodes.length; i++) {
      for (let j = i + 1; j < updatedNodes.length; j++) {
        const nodeA = updatedNodes[i];
        const nodeB = updatedNodes[j];
        const dx = nodeB.position.x - nodeA.position.x;
        const dy = nodeB.position.y - nodeA.position.y;
        const distance = Math.max(1, Math.sqrt(dx * dx + dy * dy));
        const force = REPULSION_FORCE / (distance * distance);
        const fx = (dx / distance) * force;
        const fy = (dy / distance) * force;

        nodeA.position.x -= fx * DAMPING;
        nodeA.position.y -= fy * DAMPING;
        nodeB.position.x += fx * DAMPING;
        nodeB.position.y += fy * DAMPING;
      }
    }

    setNodes(updatedNodes);
    animationRef.current = requestAnimationFrame(applyPhysics);
  };

  useEffect(() => {
    animationRef.current = requestAnimationFrame(applyPhysics);
    return () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
    };
  }, [nodes]);

  const nodeTypes = {
    custom: ({ data }: { data: any }) => (
      <div
        style={{
          width: 50,
          height: 50,
          borderRadius: '50%',
          background: '#ffcc00',
          border: '2px solid #333',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          fontWeight: 'bold',
          zIndex: 1,
        }}
      >
        {data.label}
      </div>
    ),
  };

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <GraphPlatformSidebar onLoadGrafo={() => {}} />
        <div className="flex flex-col flex-1">
          <div className="bg-white border-b p-4 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {isEditingTitle ? (
                <Input defaultValue={graphName} className="text-xl font-semibold" onKeyDown={handleTitleSave} onBlur={() => setIsEditingTitle(false)} autoFocus />
              ) : (
                <h1 className="text-xl font-semibold cursor-pointer hover:text-blue-600" onClick={handleTitleEdit} title="Clique para editar o nome">
                  {graphName}
                </h1>
              )}
              <span className="text-sm text-gray-500">Vértices: {nodes.length} | Arestas: {edges.length}</span>
            </div>
          </div>

          <GraphEditorToolbarReactFlow
            onAddNode={handleAddNode}
            onAddEdge={() => toast({ title: "Modo Aresta", description: "Use o mouse para conectar nós", variant: "default" })}
            onLayout={() => toast({ title: "Layout", description: "Não implementado", variant: "default" })}
            onResetView={handleResetView}
            onSaveGraph={handleSaveGraph}
          />

          <div className="flex-1 overflow-hidden">
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              fitView
              nodeTypes={nodeTypes}
            >
              <MiniMap />
              <Controls />
              <Background />
            </ReactFlow>
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default GraphMainEditor;
