import React, { useState, useCallback, useRef } from 'react';
import { SidebarProvider } from '@/components/ui/sidebar';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';
import GraphEditorToolbarReactFlow from './graph-editor/GraphEditorToolbarReactFlow';
import ReactFlow, {
  MiniMap, Controls, Background,
  addEdge, useNodesState, useEdgesState, Connection, Edge, Node
} from 'reactflow';
import 'reactflow/dist/style.css';
import CustomEdge from './graph-editor/CustomEdge'; // Importa o CustomEdge

const GraphMainEditor: React.FC = () => {
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const { toast } = useToast();
  const [graphName, setGraphName] = useState('Novo Grafo');

  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const reactFlowWrapper = useRef<HTMLDivElement>(null);
  const [reactFlowInstance, setReactFlowInstance] = useState<any>(null);

  // Define os tipos de arestas disponíveis
  const edgeTypes = {
    custom: CustomEdge,
  };

  const onConnect = useCallback((params: Edge | Connection) => {
    setEdges((eds) => addEdge(
      { ...params, type: 'custom', data: { label: 'Aresta', color: '#f43f5e', width: 3, dashed: false } }, 
      eds
    ));
  }, [setEdges]);

  const handleAddNode = () => {
    const id = `${+new Date()}`;
    const label = String.fromCharCode(97 + nodes.length); // Letras: a, b, c...
    const newNode: Node = {
      id,
      position: { x: Math.random() * 400, y: Math.random() * 400 },
      data: { label },
      type: 'default',
      style: { borderRadius: '50%', width: 60, height: 60, textAlign: 'center', lineHeight: '60px' }
    };
    setNodes((nds) => nds.concat(newNode));
  };

  const handleAddEdge = () => {
    toast({
      title: "Modo Aresta",
      description: "Conecte dois nós para criar uma aresta.",
      variant: "default",
    });
  };

  const handleLayout = () => {
    toast({
      title: "Layout Automático",
      description: "Layout automático ainda não implementado.",
      variant: "default",
    });
  };

  const handleResetView = () => {
    reactFlowInstance?.fitView();
  };

  const handleSaveGraph = () => {
    const graphData = { nodes, edges, name: graphName };
    console.log("Graph Saved:", graphData);
    toast({
      title: "Grafo salvo",
      description: "Os dados do grafo foram salvos no console.",
      variant: "success",
    });
  };

  const handleTitleEdit = () => setIsEditingTitle(true);
  const handleTitleSave = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const newName = (e.target as HTMLInputElement).value.trim();
      if (newName) {
        setGraphName(newName);
        setIsEditingTitle(false);
      } else {
        toast({
          title: "Erro",
          description: "O nome do grafo não pode estar vazio.",
          variant: "destructive",
        });
      }
    } else if (e.key === 'Escape') {
      setIsEditingTitle(false);
    }
  };

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <GraphPlatformSidebar onLoadGrafo={() => {}} />

        <div className="flex flex-col flex-1">
          <div className="bg-white border-b p-4 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {isEditingTitle ? (
                <Input
                  defaultValue={graphName}
                  className="text-xl font-semibold"
                  onKeyDown={handleTitleSave}
                  onBlur={() => setIsEditingTitle(false)}
                  autoFocus
                />
              ) : (
                <h1
                  className="text-xl font-semibold cursor-pointer hover:text-blue-600"
                  onClick={handleTitleEdit}
                  title="Clique para editar o nome do grafo"
                >
                  {graphName}
                </h1>
              )}
              <span className="text-sm text-gray-500">
                Vértices: {nodes.length} | Arestas: {edges.length}
              </span>
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
              edgeTypes={edgeTypes} // Usa o CustomEdge
              fitView
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
