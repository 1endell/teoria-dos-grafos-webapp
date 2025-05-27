
import React, { useState, useRef } from 'react';
import { SidebarProvider } from '@/components/ui/sidebar';
import GraphEditorToolbar from './graph-editor/GraphEditorToolbar';
import GraphEditorCanvas from './graph-editor/GraphEditorCanvas';
import GraphPlatformSidebar from './graph-editor/GraphPlatformSidebar';
import { useGraphEditor } from './graph-editor/hooks/useGraphEditor';
import { useSigmaInstance } from './graph-editor/hooks/useSigmaInstance';
import { Input } from '@/components/ui/input';
import { useToast } from '@/hooks/use-toast';

const GraphMainEditor: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const [isEditingTitle, setIsEditingTitle] = useState(false);
  const { toast } = useToast();
  
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
  } = useGraphEditor();

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

  // Inicialização inicial
  React.useEffect(() => {
    if (!containerRef.current) return;
    
    if (sigmaRef.current) {
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }
    
    const graph = initEmptyGraph();
    initSigma(graph);
    
    return () => {
      if (sigmaRef.current) {
        sigmaRef.current.kill();
        sigmaRef.current = null;
      }
    };
  }, []);

  // Alternar tipo de grafo (direcionado/não direcionado)
  const toggleDirected = () => {
    const newIsDirected = !state.isDirected;
    updateState({ isDirected: newIsDirected });
    
    // Atualizar tipo de arestas no grafo
    const graph = graphRef.current;
    graph.forEachEdge((edgeId, attributes) => {
      graph.setEdgeAttribute(edgeId, 'type', newIsDirected ? 'arrow' : 'line');
    });
    
    if (sigmaRef.current) {
      sigmaRef.current.setSetting('defaultEdgeType', newIsDirected ? 'arrow' : 'line');
      sigmaRef.current.refresh();
    }
  };

  // Alternar pesos nas arestas
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

  const handleTitleEdit = () => {
    setIsEditingTitle(true);
  };

  const handleTitleSave = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      const newName = (e.target as HTMLInputElement).value.trim();
      if (newName) {
        updateState({ grafoNome: newName });
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

  const handleLoadGrafo = async (grafoId: string) => {
    const graph = await loadGrafo(grafoId);
    if (graph && sigmaRef.current) {
      sigmaRef.current.kill();
      sigmaRef.current = null;
      initSigma(graph);
    }
  };

  const currentTitle = state.grafoNome || grafoInfo?.nome || 'Novo Grafo';

  return (
    <SidebarProvider>
      <div className="min-h-screen flex w-full">
        <GraphPlatformSidebar onLoadGrafo={handleLoadGrafo} />
        
        <div className="flex flex-col flex-1">
          {/* Header com título editável */}
          <div className="bg-white border-b p-4 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {isEditingTitle ? (
                <Input
                  defaultValue={currentTitle}
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
                  {currentTitle}
                </h1>
              )}
              <span className="text-sm text-gray-500">
                Vértices: {graphRef.current?.order || 0} | Arestas: {graphRef.current?.size || 0}
              </span>
            </div>
          </div>

          {/* Toolbar */}
          <GraphEditorToolbar
            mode={state.mode}
            isDirected={state.isDirected}
            isWeighted={state.isWeighted}
            selectedNode={state.selectedNode}
            isLoading={state.isLoading}
            nodeProperties={state.nodeProperties}
            edgeProperties={state.edgeProperties}
            onModeChange={handleModeChange}
            onToggleDirected={toggleDirected}
            onToggleWeighted={toggleWeighted}
            onApplyLayout={handleApplyLayout}
            onResetZoom={resetZoom}
            onRemoveSelectedNode={handleRemoveSelectedNode}
            onSaveGraph={saveGraph}
            onNodePropertiesChange={(properties) => updateState({ nodeProperties: properties })}
            onEdgePropertiesChange={(properties) => updateState({ edgeProperties: properties })}
          />
          
          {/* Canvas */}
          <div className="flex-1 overflow-hidden">
            <GraphEditorCanvas
              mode={state.mode}
              sourceNode={state.sourceNode}
              isLoading={state.isLoading}
              onContainerRef={handleContainerRef}
            />
          </div>
        </div>
      </div>
    </SidebarProvider>
  );
};

export default GraphMainEditor;
