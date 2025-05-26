import React, { useEffect, useRef, useState } from 'react';
import Graph from 'graphology';
import { Sigma } from 'sigma';
import { circular } from 'graphology-layout';
import forceAtlas2 from 'graphology-layout-forceatlas2';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { 
  Plus, Minus, Move, MousePointer, Circle, ArrowRight, 
  Save, Trash2, RotateCcw, RotateCw, Maximize, Settings 
} from 'lucide-react';
import { graphService } from '@/services/graphService';
import { Grafo, GrafoCreate, VerticeCreate, ArestaCreate } from '@/types/graph';
import { useToast } from '@/hooks/use-toast';

// Definição de tipos para o editor
type EditorMode = 'select' | 'addNode' | 'addEdge' | 'pan';

interface GraphEditorProps {
  grafoId?: string;
  onSave?: (grafoId: string) => void;
}

const GraphEditor: React.FC<GraphEditorProps> = ({ grafoId, onSave }) => {
  // Refs
  const containerRef = useRef<HTMLDivElement>(null);
  const sigmaRef = useRef<Sigma | null>(null);
  const graphRef = useRef<Graph>(new Graph({ multi: false, type: 'directed' }));
  
  // Estado
  const [mode, setMode] = useState<EditorMode>('select');
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [sourceNode, setSourceNode] = useState<string | null>(null);
  const [grafoInfo, setGrafoInfo] = useState<Grafo | null>(null);
  const [isDirected, setIsDirected] = useState(true);
  const [isWeighted, setIsWeighted] = useState(true);
  const [nodeCounter, setNodeCounter] = useState(0);
  const [nodeProperties, setNodeProperties] = useState({ label: '', color: '#1E88E5' });
  const [edgeProperties, setEdgeProperties] = useState({ weight: 1.0, color: '#757575' });
  const [isLoading, setIsLoading] = useState(false);
  const [layoutType, setLayoutType] = useState('circular');
  
  const { toast } = useToast();

  // Inicialização do Sigma e carregamento do grafo
  useEffect(() => {
    console.log('GraphEditor useEffect triggered');
    if (!containerRef.current) {
      console.log('Container ref not available');
      return;
    }
    
    // Limpar instância anterior se existir
    if (sigmaRef.current) {
      console.log('Cleaning previous sigma instance');
      sigmaRef.current.kill();
      sigmaRef.current = null;
    }
    
    // Inicializar grafo vazio ou carregar existente
    if (grafoId) {
      console.log('Loading existing graph:', grafoId);
      loadGrafo(grafoId);
    } else {
      console.log('Initializing empty graph');
      initEmptyGraph();
    }
    
    return () => {
      if (sigmaRef.current) {
        sigmaRef.current.kill();
        sigmaRef.current = null;
      }
    };
  }, [grafoId]);

  // Carregar grafo existente
  const loadGrafo = async (id: string) => {
    try {
      setIsLoading(true);
      console.log('Loading graph data for ID:', id);
      const grafo = await graphService.obterGrafo(id);
      setGrafoInfo(grafo);
      setIsDirected(grafo.direcionado);
      setIsWeighted(grafo.ponderado);
      
      // Obter visualização para posições dos nós
      const visualizacao = await graphService.obterVisualizacao(id, 'spring', true);
      
      // Criar novo grafo
      const graph = new Graph({ multi: false, type: grafo.direcionado ? 'directed' : 'undirected' });
      
      // Adicionar vértices
      visualizacao.vertices.forEach(v => {
        graph.addNode(v.id, {
          x: v.x,
          y: v.y,
          size: 10,
          color: v.atributos?.cor || '#1E88E5',
          label: v.id
        });
      });
      
      // Adicionar arestas
      visualizacao.arestas.forEach(a => {
        if (graph.hasNode(a.origem) && graph.hasNode(a.destino)) {
          graph.addEdge(a.origem, a.destino, {
            size: 2,
            color: '#757575',
            label: a.peso !== undefined ? a.peso.toString() : '',
            weight: a.peso || 1,
            type: grafo.direcionado ? 'arrow' : 'line'
          });
        }
      });
      
      // Atualizar contador de nós
      const nodeIds = graph.nodes();
      if (nodeIds.length > 0) {
        const numericIds = nodeIds
          .filter(id => /^\d+$/.test(id))
          .map(id => parseInt(id, 10));
        
        if (numericIds.length > 0) {
          setNodeCounter(Math.max(...numericIds) + 1);
        }
      }
      
      graphRef.current = graph;
      initSigma(graph);
      
    } catch (error) {
      console.error('Error loading graph:', error);
      toast({
        title: "Erro",
        description: "Não foi possível carregar o grafo.",
        variant: "destructive",
      });
      initEmptyGraph();
    } finally {
      setIsLoading(false);
    }
  };

  // Inicializar grafo vazio
  const initEmptyGraph = () => {
    console.log('Initializing empty graph');
    const graph = new Graph({ multi: false, type: isDirected ? 'directed' : 'undirected' });
    graphRef.current = graph;
    initSigma(graph);
  };

  // Inicializar Sigma
  const initSigma = (graph: Graph) => {
    if (!containerRef.current) {
      console.log('Container not available for sigma init');
      return;
    }
    
    console.log('Initializing Sigma with graph order:', graph.order);
    
    try {
      // Aplicar layout se o grafo tiver nós
      if (graph.order > 0) {
        if (layoutType === 'circular') {
          circular.assign(graph);
        } else if (layoutType === 'forceatlas2') {
          const settings = forceAtlas2.inferSettings(graph);
          forceAtlas2.assign(graph, { settings, iterations: 100 });
        }
      }
      
      // Configuração do Sigma com configurações mais simples
      const sigmaSettings = {
        renderEdgeLabels: isWeighted,
        defaultEdgeType: isDirected ? 'arrow' : 'line',
        defaultNodeColor: '#1E88E5',
        defaultEdgeColor: '#757575',
        labelSize: 14,
        labelWeight: 'bold' as const,
        minCameraRatio: 0.1,
        maxCameraRatio: 5,
      };
      
      console.log('Creating Sigma instance with settings:', sigmaSettings);
      
      // Inicializar Sigma
      sigmaRef.current = new Sigma(graph, containerRef.current, sigmaSettings);
      
      console.log('Sigma instance created successfully');
      
      // Configurar eventos
      setupSigmaEvents();
      
      // Refresh para garantir que tudo seja renderizado
      sigmaRef.current.refresh();
      
    } catch (error) {
      console.error('Error initializing Sigma:', error);
      toast({
        title: "Erro",
        description: "Erro ao inicializar o editor visual.",
        variant: "destructive",
      });
    }
  };

  // Configurar eventos do Sigma
  const setupSigmaEvents = () => {
    if (!sigmaRef.current) {
      console.log('No sigma instance for event setup');
      return;
    }
    
    console.log('Setting up Sigma events');
    const sigma = sigmaRef.current;
    
    // Evento de clique no canvas - CORRIGIDO
    sigma.on('clickStage', (event: any) => {
      console.log('Stage clicked, mode:', mode, 'event:', event);
      
      if (mode === 'addNode') {
        // Corrigir a obtenção das coordenadas do clique
        const coords = sigma.viewportToGraph(event);
        console.log('Adding node at coordinates:', coords);
        addNode(coords);
      } else if (mode === 'select') {
        setSelectedNode(null);
        setSourceNode(null);
      }
    });
    
    // Evento de clique em nó
    sigma.on('clickNode', (event: any) => {
      const nodeId = event.node;
      console.log('Node clicked:', nodeId, 'mode:', mode);
      
      if (mode === 'select') {
        setSelectedNode(nodeId);
      } else if (mode === 'addEdge') {
        if (sourceNode === null) {
          setSourceNode(nodeId);
          console.log('Source node selected:', nodeId);
        } else if (sourceNode !== nodeId) {
          console.log('Target node selected, creating edge:', sourceNode, '->', nodeId);
          addEdge(sourceNode, nodeId);
          setSourceNode(null);
        }
      }
    });
  };

  // Gerar nome automático para vértice com letras minúsculas
  const generateNodeName = (): string => {
    const getLetterName = (num: number): string => {
      let name = '';
      let n = num;
      
      if (n < 26) {
        // a-z
        return String.fromCharCode(97 + n);
      } else {
        // aa, ab, ac, ... 
        const firstLetter = Math.floor((n - 26) / 26);
        const secondLetter = (n - 26) % 26;
        return String.fromCharCode(97 + firstLetter) + String.fromCharCode(97 + secondLetter);
      }
    };
    
    const graph = graphRef.current;
    const usedNames = new Set<string>();
    
    // Coletar nomes já utilizados
    graph.forEachNode((nodeId, attributes) => {
      if (attributes.label) {
        usedNames.add(attributes.label);
      }
    });
    
    let index = 0;
    let name = getLetterName(index);
    
    // Encontrar próximo nome disponível
    while (usedNames.has(name)) {
      index++;
      name = getLetterName(index);
    }
    
    return name;
  };

  // Adicionar nó
  const addNode = (coords: {x: number, y: number}) => {
    const graph = graphRef.current;
    const nodeId = nodeCounter.toString();
    const nodeName = nodeProperties.label || generateNodeName();
    
    console.log('Adding node:', { nodeId, nodeName, coords });
    
    try {
      graph.addNode(nodeId, {
        ...coords,
        size: 15,
        color: nodeProperties.color,
        label: nodeName
      });
      
      setNodeCounter(prev => prev + 1);
      
      // Refresh sigma para mostrar o novo nó
      if (sigmaRef.current) {
        sigmaRef.current.refresh();
      }
      
      toast({
        title: "Sucesso",
        description: `Vértice ${nodeName} adicionado.`,
      });
      
      console.log('Node added successfully');
    } catch (error) {
      console.error('Error adding node:', error);
      toast({
        title: "Erro",
        description: "Erro ao adicionar vértice.",
        variant: "destructive",
      });
    }
  };

  // Adicionar aresta
  const addEdge = (source: string, target: string) => {
    const graph = graphRef.current;
    
    if (graph.hasEdge(source, target)) {
      toast({
        title: "Aviso",
        description: "Esta aresta já existe.",
        variant: "default",
      });
      return;
    }
    
    try {
      graph.addEdge(source, target, {
        size: 2,
        color: edgeProperties.color,
        label: isWeighted ? edgeProperties.weight.toString() : '',
        weight: edgeProperties.weight,
        type: isDirected ? 'arrow' : 'line'
      });
      
      // Refresh sigma para mostrar a nova aresta
      if (sigmaRef.current) {
        sigmaRef.current.refresh();
      }
      
      const sourceLabel = graph.getNodeAttribute(source, 'label');
      const targetLabel = graph.getNodeAttribute(target, 'label');
      
      toast({
        title: "Sucesso",
        description: `Aresta de ${sourceLabel} para ${targetLabel} adicionada.`,
      });
    } catch (error) {
      console.error('Error adding edge:', error);
      toast({
        title: "Erro",
        description: "Erro ao adicionar aresta.",
        variant: "destructive",
      });
    }
  };

  // Remover nó selecionado
  const removeSelectedNode = () => {
    if (!selectedNode) return;
    
    const graph = graphRef.current;
    const nodeLabel = graph.getNodeAttribute(selectedNode, 'label');
    
    try {
      graph.dropNode(selectedNode);
      setSelectedNode(null);
      
      if (sigmaRef.current) {
        sigmaRef.current.refresh();
      }
      
      toast({
        title: "Sucesso",
        description: `Vértice ${nodeLabel} removido.`,
      });
    } catch (error) {
      console.error('Error removing node:', error);
      toast({
        title: "Erro",
        description: "Erro ao remover vértice.",
        variant: "destructive",
      });
    }
  };

  // Aplicar layout
  const applyLayout = (type: string) => {
    const graph = graphRef.current;
    
    if (graph.order === 0) return;
    
    try {
      if (type === 'circular') {
        circular.assign(graph);
      } else if (type === 'forceatlas2') {
        const settings = forceAtlas2.inferSettings(graph);
        forceAtlas2.assign(graph, { settings, iterations: 100 });
      }
      
      setLayoutType(type);
      if (sigmaRef.current) {
        sigmaRef.current.refresh();
      }
    } catch (error) {
      console.error('Error applying layout:', error);
    }
  };

  // Resetar zoom
  const resetZoom = () => {
    if (sigmaRef.current) {
      const camera = sigmaRef.current.getCamera();
      camera.animatedReset();
    }
  };

  // Salvar grafo
  const saveGraph = async () => {
    try {
      setIsLoading(true);
      
      const graph = graphRef.current;
      const vertices: VerticeCreate[] = [];
      const arestas: ArestaCreate[] = [];
      
      // Coletar vértices
      graph.forEachNode((nodeId, attributes) => {
        vertices.push({
          id: nodeId,
          atributos: {
            cor: attributes.color,
            label: attributes.label
          }
        });
      });
      
      // Coletar arestas
      graph.forEachEdge((edgeId, attributes, source, target) => {
        arestas.push({
          origem: source,
          destino: target,
          peso: attributes.weight || 1.0,
          atributos: {
            cor: attributes.color
          }
        });
      });
      
      // Criar novo grafo
      const resultado = await criarNovoGrafo(vertices, arestas);
      
      toast({
        title: "Sucesso",
        description: "Grafo salvo com sucesso!",
      });
      
      if (onSave && resultado) {
        onSave(resultado.id);
      }
      
    } catch (error) {
      console.error('Error saving graph:', error);
      toast({
        title: "Erro",
        description: "Não foi possível salvar o grafo.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Criar novo grafo
  const criarNovoGrafo = async (vertices: VerticeCreate[], arestas: ArestaCreate[]) => {
    const novoGrafo: GrafoCreate = {
      nome: grafoInfo?.nome || `Grafo Visual ${new Date().toLocaleString()}`,
      direcionado: isDirected,
      ponderado: isWeighted,
      vertices,
      arestas
    };
    
    return await graphService.criarGrafo(novoGrafo);
  };

  // Alternar tipo de grafo (direcionado/não direcionado)
  const toggleDirected = () => {
    setIsDirected(prev => !prev);
    
    const oldGraph = graphRef.current;
    const newGraph = new Graph({ multi: false, type: !isDirected ? 'directed' : 'undirected' });
    
    // Copiar nós
    oldGraph.forEachNode((nodeId, attributes) => {
      newGraph.addNode(nodeId, attributes);
    });
    
    // Copiar arestas
    oldGraph.forEachEdge((edgeId, attributes, source, target) => {
      const newAttributes = {
        ...attributes,
        type: !isDirected ? 'arrow' : 'line'
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

  // Alternar pesos nas arestas
  const toggleWeighted = () => {
    setIsWeighted(prev => !prev);
    
    if (sigmaRef.current) {
      sigmaRef.current.setSetting('renderEdgeLabels', !isWeighted);
      sigmaRef.current.refresh();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Barra de ferramentas */}
      <div className="bg-white border-b p-2 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <Button
            size="sm"
            variant={mode === 'select' ? 'default' : 'outline'}
            onClick={() => setMode('select')}
            title="Selecionar"
          >
            <MousePointer className="h-4 w-4" />
          </Button>
          <Button
            size="sm"
            variant={mode === 'addNode' ? 'default' : 'outline'}
            onClick={() => setMode('addNode')}
            title="Adicionar Vértice"
          >
            <Circle className="h-4 w-4" />
          </Button>
          <Button
            size="sm"
            variant={mode === 'addEdge' ? 'default' : 'outline'}
            onClick={() => setMode('addEdge')}
            title="Adicionar Aresta"
          >
            <ArrowRight className="h-4 w-4" />
          </Button>
          <Button
            size="sm"
            variant={mode === 'pan' ? 'default' : 'outline'}
            onClick={() => setMode('pan')}
            title="Mover Canvas"
          >
            <Move className="h-4 w-4" />
          </Button>
          
          <div className="h-6 border-r mx-2"></div>
          
          <Button
            size="sm"
            variant="outline"
            onClick={() => applyLayout('circular')}
            title="Layout Circular"
            disabled={isLoading}
          >
            <span className="text-xs">Circular</span>
          </Button>
          <Button
            size="sm"
            variant="outline"
            onClick={() => applyLayout('forceatlas2')}
            title="Layout Force Atlas 2"
            disabled={isLoading}
          >
            <span className="text-xs">Force</span>
          </Button>
          
          <div className="h-6 border-r mx-2"></div>
          
          <Button
            size="sm"
            variant="outline"
            onClick={resetZoom}
            title="Resetar Zoom"
          >
            <Maximize className="h-4 w-4" />
          </Button>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-2">
            <div className="flex items-center space-x-1">
              <Checkbox 
                id="directed"
                checked={isDirected}
                onCheckedChange={toggleDirected}
              />
              <Label htmlFor="directed" className="text-xs">Direcionado</Label>
            </div>
            <div className="flex items-center space-x-1">
              <Checkbox 
                id="weighted"
                checked={isWeighted}
                onCheckedChange={toggleWeighted}
              />
              <Label htmlFor="weighted" className="text-xs">Ponderado</Label>
            </div>
          </div>
          
          <div className="h-6 border-r mx-2"></div>
          
          <Button
            size="sm"
            variant="outline"
            onClick={removeSelectedNode}
            disabled={!selectedNode}
            title="Remover Selecionado"
          >
            <Trash2 className="h-4 w-4" />
          </Button>
          
          <Button
            size="sm"
            variant="default"
            onClick={saveGraph}
            disabled={isLoading}
            title="Salvar Grafo"
          >
            <Save className="h-4 w-4 mr-1" />
            <span>Salvar</span>
          </Button>
        </div>
      </div>
      
      {/* Área principal */}
      <div className="flex flex-1 overflow-hidden">
        {/* Canvas do grafo com grid */}
        <div 
          ref={containerRef} 
          className="flex-1 bg-gray-50 relative"
          style={{ 
            position: 'relative',
            backgroundImage: `
              linear-gradient(rgba(0,0,0,0.1) 1px, transparent 1px),
              linear-gradient(90deg, rgba(0,0,0,0.1) 1px, transparent 1px)
            `,
            backgroundSize: '20px 20px'
          }}
        >
          {isLoading && (
            <div className="absolute inset-0 bg-white/70 flex items-center justify-center z-10">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          )}
          
          {mode === 'addNode' && (
            <div className="absolute top-4 left-4 bg-white p-2 rounded shadow-md z-10">
              <p className="text-sm font-medium">Clique no canvas para adicionar um vértice</p>
            </div>
          )}
          
          {mode === 'addEdge' && (
            <div className="absolute top-4 left-4 bg-white p-2 rounded shadow-md z-10">
              <p className="text-sm font-medium">
                {sourceNode 
                  ? `Selecione o vértice de destino (origem: ${sourceNode})` 
                  : 'Selecione o vértice de origem'}
              </p>
            </div>
          )}
        </div>
        
        {/* Painel lateral de propriedades */}
        <div className="w-64 border-l bg-white p-4 overflow-y-auto">
          <Tabs defaultValue="node">
            <TabsList className="w-full">
              <TabsTrigger value="node" className="flex-1">Vértice</TabsTrigger>
              <TabsTrigger value="edge" className="flex-1">Aresta</TabsTrigger>
            </TabsList>
            
            <TabsContent value="node" className="space-y-4 mt-4">
              <div>
                <Label htmlFor="nodeLabel">Rótulo</Label>
                <Input
                  id="nodeLabel"
                  value={nodeProperties.label}
                  onChange={(e) => setNodeProperties({...nodeProperties, label: e.target.value})}
                  placeholder="Auto (a, b, c...)"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Deixe vazio para gerar automaticamente (a, b, c, ..., z, aa, ab...)
                </p>
              </div>
              
              <div>
                <Label htmlFor="nodeColor">Cor</Label>
                <div className="flex items-center space-x-2">
                  <Input
                    id="nodeColor"
                    type="color"
                    value={nodeProperties.color}
                    onChange={(e) => setNodeProperties({...nodeProperties, color: e.target.value})}
                    className="w-12 h-8 p-0"
                  />
                  <Input
                    value={nodeProperties.color}
                    onChange={(e) => setNodeProperties({...nodeProperties, color: e.target.value})}
                    className="flex-1"
                  />
                </div>
              </div>
              
              {selectedNode && (
                <div className="mt-4 p-2 bg-gray-50 rounded">
                  <h4 className="text-sm font-medium mb-2">Vértice Selecionado: {selectedNode}</h4>
                  <Button 
                    size="sm" 
                    variant="destructive"
                    onClick={removeSelectedNode}
                    className="w-full"
                  >
                    <Trash2 className="h-4 w-4 mr-1" />
                    Remover
                  </Button>
                </div>
              )}
            </TabsContent>
            
            <TabsContent value="edge" className="space-y-4 mt-4">
              {isWeighted && (
                <div>
                  <Label htmlFor="edgeWeight">Peso</Label>
                  <div className="flex items-center space-x-2">
                    <Input
                      type="number"
                      step="0.1"
                      min="0"
                      value={edgeProperties.weight}
                      onChange={(e) => setEdgeProperties({...edgeProperties, weight: parseFloat(e.target.value) || 0})}
                      className="flex-1"
                    />
                  </div>
                </div>
              )}
              
              <div>
                <Label htmlFor="edgeColor">Cor</Label>
                <div className="flex items-center space-x-2">
                  <Input
                    id="edgeColor"
                    type="color"
                    value={edgeProperties.color}
                    onChange={(e) => setEdgeProperties({...edgeProperties, color: e.target.value})}
                    className="w-12 h-8 p-0"
                  />
                  <Input
                    value={edgeProperties.color}
                    onChange={(e) => setEdgeProperties({...edgeProperties, color: e.target.value})}
                    className="flex-1"
                  />
                </div>
              </div>
              
              <div className="mt-4">
                <p className="text-sm text-gray-500">
                  Para adicionar uma aresta, selecione o modo de aresta e clique em dois vértices consecutivamente.
                </p>
              </div>
            </TabsContent>
          </Tabs>
          
          <div className="mt-6">
            <h3 className="text-sm font-medium mb-2">Informações do Grafo</h3>
            <div className="text-xs space-y-1">
              <p>Vértices: {graphRef.current?.order || 0}</p>
              <p>Arestas: {graphRef.current?.size || 0}</p>
              <p>Tipo: {isDirected ? 'Direcionado' : 'Não direcionado'}</p>
              <p>Pesos: {isWeighted ? 'Sim' : 'Não'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GraphEditor;
