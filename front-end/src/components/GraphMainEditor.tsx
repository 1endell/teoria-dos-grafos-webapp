import React, { useState, useCallback, useRef, useEffect } from 'react';
import { SidebarProvider } from '@/components/ui/sidebar';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import GraphEditorToolbarReactFlow from './graph-editor/GraphEditorToolbarReactFlow';
import ReactFlow, {
  MiniMap, Controls, Background,
  addEdge, useNodesState, useEdgesState, Connection, Edge, Node
} from 'reactflow';
import CustomEdge from './graph-editor/CustomEdge';
import CustomNode from './graph-editor/CustomNode';
import 'reactflow/dist/style.css';

const GraphMainEditor: React.FC = () => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const { toast } = useToast();
  const [graphName, setGraphName] = useState('Novo Grafo');

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [physicsEnabled, setPhysicsEnabled] = useState(true);
  const [repulsionForce, setRepulsionForce] = useState(10000);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);
  const selectedNodesRef = useRef<string[]>([]);

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
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: { label, color: '#ffcc00', icon: '⭐', size: 60 },
      type: 'custom',
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const handleAddEdge = () => {
    toast({ title: "Modo Aresta", description: "Conecte dois nós para criar uma aresta.", variant: "default" });
  };

  const handleLayout = () => {
    toast({ title: "Layout Automático", description: "Layout ainda não implementado.", variant: "default" });
  };

  const handleResetView = () => {
    reactFlowInstance?.fitView();
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

  // Física de repulsão + Snap to grid + Seleção múltipla
  useEffect(() => {
    let animationFrame: number;
    const applyPhysics = () => {
      if (!physicsEnabled) return;
      const updatedNodes = [...nodes];
      for (let i = 0; i < updatedNodes.length; i++) {
        for (let j = i + 1; j < updatedNodes.length; j++) {
          const node1 = updatedNodes[i];
          const node2 = updatedNodes[j];
          const dx = node2.position.x - node1.position.x;
          const dy = node2.position.y - node1.position.y;
          const distance = Math.sqrt(dx * dx + dy * dy) + 0.1;
          const force = repulsionForce / (distance * distance);
          const fx = (dx / distance) * force;
          const fy = (dy / distance) * force;
          node1.position.x -= fx * 0.1;
          node1.position.y -= fy * 0.1;
          node2.position.x += fx * 0.1;
          node2.position.y += fy * 0.1;
        }
      }
      setNodes(updatedNodes);
      animationFrame = requestAnimationFrame(applyPhysics);
    };
    if (physicsEnabled) animationFrame = requestAnimationFrame(applyPhysics);
    return () => cancelAnimationFrame(animationFrame);
  }, [nodes, physicsEnabled, repulsionForce]);

  // Teclas para Snap e Movimentação
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const step = 10;
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key)) {
        setNodes((nds) =>
          nds.map((node) =>
            selectedNodesRef.current.includes(node.id)
              ? {
                  ...node,
                  position: {
                    x: node.position.x + (e.key === 'ArrowRight' ? step : e.key === 'ArrowLeft' ? -step : 0),
                    y: node.position.y + (e.key === 'ArrowDown' ? step : e.key === 'ArrowUp' ? -step : 0),
                  },
                }
              : node
          )
        );
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const nodeTypes = { custom: CustomNode };
  const edgeTypes = { custom: CustomEdge };

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
                <h1 className="text-xl font-semibold cursor-pointer hover:text-blue-600" onClick={handleTitleEdit}>
                  {graphName}
                </h1>
              )}
              <span className="text-sm text-gray-500">Vértices: {nodes.length} | Arestas: {edges.length}</span>
            </div>
          </div>

          <GraphEditorToolbarReactFlow
            onAddNode={handleAddNode}
            onAddEdge={handleAddEdge}
            onLayout={handleLayout}
            onResetView={handleResetView}
            onSaveGraph={handleSaveGraph}
          />
          <div className="flex-1 overflow-hidden" ref={reactFlowWrapper}>
            <ReactFlow
              nodes={nodes}
              edges={edges}
              onNodesChange={onNodesChange}
              onEdgesChange={onEdgesChange}
              onConnect={onConnect}
              onInit={setReactFlowInstance}
              nodeTypes={nodeTypes}
              edgeTypes={edgeTypes}
              fitView
              multiSelectionKeyCode="Shift" // Multi-seleção com Shift
              onSelectionChange={(elements) =>
                (selectedNodesRef.current = elements?.nodes?.map((n) => n.id) || [])
              }
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
