import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Plus, Search, Download, Upload } from 'lucide-react';
import { graphService } from '@/services/graphService';
import { GrafoInfo, GrafoCreate } from '@/types/graph';
import GraphEditor from './GraphEditor';
import { useToast } from '@/hooks/use-toast';

const GraphVisualEditor: React.FC = () => {
  const [grafos, setGrafos] = useState<GrafoInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [selectedGrafoId, setSelectedGrafoId] = useState<string | null>(null);
  const [newGraph, setNewGraph] = useState<GrafoCreate>({
    nome: '',
    direcionado: true,
    ponderado: true,
    bipartido: false,
  });
  const [importData, setImportData] = useState({
    nome: '',
    formato: 'json',
    conteudo: ''
  });
  const [exportData, setExportData] = useState({
    grafoId: '',
    formato: 'json'
  });
  const [isEditorMode, setIsEditorMode] = useState(false);
  const { toast } = useToast();

  useEffect(() => {
    loadGrafos();
  }, []);

  const loadGrafos = async () => {
    try {
      setLoading(true);
      const response = await graphService.listarGrafos();
      setGrafos(response.grafos);
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível carregar os grafos. Verifique a conexão com a API.",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCreateGraph = async () => {
    if (!newGraph.nome.trim()) {
      toast({
        title: "Erro",
        description: "O nome do grafo é obrigatório.",
        variant: "destructive",
      });
      return;
    }

    try {
      const grafo = await graphService.criarGrafo(newGraph);
      toast({
        title: "Sucesso",
        description: "Grafo criado com sucesso!",
      });
      setIsCreateDialogOpen(false);
      setNewGraph({
        nome: '',
        direcionado: true,
        ponderado: true,
        bipartido: false,
      });
      
      // Carregar o grafo recém-criado no editor
      setSelectedGrafoId(grafo.id);
      setIsEditorMode(true);
      
      // Atualizar a lista de grafos
      loadGrafos();
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível criar o grafo.",
        variant: "destructive",
      });
    }
  };

  const handleDeleteGraph = async (id: string) => {
    if (!confirm('Tem certeza que deseja excluir este grafo?')) return;

    try {
      await graphService.excluirGrafo(id);
      toast({
        title: "Sucesso",
        description: "Grafo excluído com sucesso!",
      });
      
      // Se o grafo excluído estiver aberto no editor, voltar para a lista
      if (selectedGrafoId === id) {
        setSelectedGrafoId(null);
        setIsEditorMode(false);
      }
      
      loadGrafos();
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível excluir o grafo.",
        variant: "destructive",
      });
    }
  };

  // Funções para importação e exportação
  const handleImport = async () => {
    if (!importData.nome.trim()) {
      toast({
        title: "Erro",
        description: "O nome do grafo é obrigatório.",
        variant: "destructive",
      });
      return;
    }

    if (!importData.conteudo.trim()) {
      toast({
        title: "Erro",
        description: "O conteúdo do grafo é obrigatório.",
        variant: "destructive",
      });
      return;
    }

    try {
      const grafoImportado = await graphService.importarGrafo(
        importData.nome,
        importData.formato,
        btoa(importData.conteudo) // Codifica em base64
      );
      
      toast({
        title: "Sucesso",
        description: `Grafo "${grafoImportado.nome}" importado com sucesso!`,
      });
      
      // Carregar o grafo importado no editor
      setSelectedGrafoId(grafoImportado.id);
      setIsEditorMode(true);
      
      loadGrafos();
      setImportData({
        nome: '',
        formato: 'json',
        conteudo: ''
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível importar o grafo. Verifique o formato e o conteúdo.",
        variant: "destructive",
      });
    }
  };

  const handleExport = async () => {
    if (!exportData.grafoId) {
      toast({
        title: "Erro",
        description: "Selecione um grafo para exportar.",
        variant: "destructive",
      });
      return;
    }

    try {
      const resultado = await graphService.exportarGrafo(exportData.grafoId, exportData.formato);
      
      // Decodifica o conteúdo de base64
      const conteudo = atob(resultado.conteudo);
      
      // Cria um blob e um link para download
      const blob = new Blob([conteudo], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `grafo_${exportData.grafoId}.${exportData.formato}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      toast({
        title: "Sucesso",
        description: "Grafo exportado com sucesso!",
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível exportar o grafo.",
        variant: "destructive",
      });
    }
  };

  const handleEditorSave = (grafoId: string) => {
    toast({
      title: "Sucesso",
      description: "Grafo salvo com sucesso!",
    });
    loadGrafos();
  };

  const handleOpenEditor = (grafoId: string) => {
    setSelectedGrafoId(grafoId);
    setIsEditorMode(true);
  };

  const handleBackToList = () => {
    setSelectedGrafoId(null);
    setIsEditorMode(false);
  };

  const handleNewEmptyGraph = () => {
    setSelectedGrafoId(null);
    setIsEditorMode(true);
  };

  const filteredGrafos = grafos.filter(grafo =>
    grafo.nome.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Modo editor visual
  if (isEditorMode) {
    return (
      <div className="flex flex-col h-full">
        <div className="bg-white border-b p-2 flex items-center justify-between">
          <h2 className="text-lg font-semibold">
            {selectedGrafoId ? 'Editar Grafo' : 'Novo Grafo'}
          </h2>
          <Button variant="outline" onClick={handleBackToList}>
            Voltar para Lista
          </Button>
        </div>
        <div className="flex-1 overflow-hidden">
          <GraphEditor 
            grafoId={selectedGrafoId || undefined} 
            onSave={handleEditorSave}
          />
        </div>
      </div>
    );
  }

  // Modo lista de grafos
  return (
    <div className="container mx-auto px-6 py-8">
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between mb-8">
        <div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Meus Grafos</h2>
          <p className="text-gray-600">Gerencie e visualize seus grafos de estudo</p>
        </div>
        
        <div className="flex flex-col sm:flex-row gap-3 mt-4 lg:mt-0">
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" className="border-blue-600 text-blue-600 hover:bg-blue-50">
                <Upload className="mr-2 h-4 w-4" />
                Importar
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Importar Grafo</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="nome-import">Nome do Grafo</Label>
                  <Input
                    id="nome-import"
                    placeholder="Digite o nome do grafo"
                    value={importData.nome}
                    onChange={(e) => setImportData({...importData, nome: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="formato">Formato</Label>
                  <select 
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    value={importData.formato}
                    onChange={(e) => setImportData({...importData, formato: e.target.value})}
                  >
                    <option value="json">JSON</option>
                    <option value="graphml">GraphML</option>
                    <option value="gml">GML</option>
                    <option value="gexf">GEXF</option>
                    <option value="csv">CSV</option>
                  </select>
                </div>
                <div>
                  <Label htmlFor="conteudo">Conteúdo</Label>
                  <textarea 
                    className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    placeholder="Cole o conteúdo do grafo aqui"
                    value={importData.conteudo}
                    onChange={(e) => setImportData({...importData, conteudo: e.target.value})}
                  />
                </div>
                <div className="flex justify-end space-x-2 pt-4">
                  <Button variant="outline">
                    Cancelar
                  </Button>
                  <Button onClick={handleImport}>
                    Importar
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
          
          <Dialog>
            <DialogTrigger asChild>
              <Button variant="outline" className="border-green-600 text-green-600 hover:bg-green-50">
                <Download className="mr-2 h-4 w-4" />
                Exportar
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Exportar Grafo</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="grafo-export">Selecione o Grafo</Label>
                  <select 
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    value={exportData.grafoId}
                    onChange={(e) => setExportData({...exportData, grafoId: e.target.value})}
                  >
                    <option value="">Selecione um grafo</option>
                    {grafos.map(grafo => (
                      <option key={grafo.id} value={grafo.id}>{grafo.nome}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <Label htmlFor="formato-export">Formato</Label>
                  <select 
                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                    value={exportData.formato}
                    onChange={(e) => setExportData({...exportData, formato: e.target.value})}
                  >
                    <option value="json">JSON</option>
                    <option value="graphml">GraphML</option>
                    <option value="gml">GML</option>
                    <option value="gexf">GEXF</option>
                    <option value="csv">CSV</option>
                  </select>
                </div>
                <div className="flex justify-end space-x-2 pt-4">
                  <Button variant="outline">
                    Cancelar
                  </Button>
                  <Button onClick={handleExport}>
                    Exportar
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
          
          <Dialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                <Plus className="mr-2 h-4 w-4" />
                Novo Grafo
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-md">
              <DialogHeader>
                <DialogTitle>Criar Novo Grafo</DialogTitle>
              </DialogHeader>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="nome">Nome do Grafo</Label>
                  <Input
                    id="nome"
                    value={newGraph.nome}
                    onChange={(e) => setNewGraph({ ...newGraph, nome: e.target.value })}
                    placeholder="Digite o nome do grafo"
                  />
                </div>
                
                <div className="space-y-3">
                  <Label>Propriedades do Grafo</Label>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="direcionado"
                      checked={newGraph.direcionado}
                      onCheckedChange={(checked) => 
                        setNewGraph({ ...newGraph, direcionado: checked as boolean })
                      }
                    />
                    <Label htmlFor="direcionado">Direcionado</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="ponderado"
                      checked={newGraph.ponderado}
                      onCheckedChange={(checked) => 
                        setNewGraph({ ...newGraph, ponderado: checked as boolean })
                      }
                    />
                    <Label htmlFor="ponderado">Ponderado</Label>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Checkbox
                      id="bipartido"
                      checked={newGraph.bipartido}
                      onCheckedChange={(checked) => 
                        setNewGraph({ ...newGraph, bipartido: checked as boolean })
                      }
                    />
                    <Label htmlFor="bipartido">Bipartido</Label>
                  </div>
                </div>
                
                <div className="flex justify-end space-x-2 pt-4">
                  <Button variant="outline" onClick={() => setIsCreateDialogOpen(false)}>
                    Cancelar
                  </Button>
                  <Button onClick={handleCreateGraph}>
                    Criar Grafo
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>
      </div>

      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <Input
            placeholder="Buscar grafos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </div>

      <div className="mb-4 flex justify-between items-center">
        <h3 className="text-lg font-semibold">Grafos Disponíveis</h3>
        <Button 
          variant="outline" 
          className="border-blue-600 text-blue-600 hover:bg-blue-50"
          onClick={handleNewEmptyGraph}
        >
          <Plus className="mr-2 h-4 w-4" />
          Editor Visual
        </Button>
      </div>

      {filteredGrafos.length === 0 ? (
        <div className="text-center py-12">
          <div className="mx-auto w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-4">
            <Plus className="h-8 w-8 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            {grafos.length === 0 ? 'Nenhum grafo encontrado' : 'Nenhum resultado encontrado'}
          </h3>
          <p className="text-gray-500 mb-4">
            {grafos.length === 0 
              ? 'Comece criando seu primeiro grafo para estudar teoria dos grafos.'
              : 'Tente ajustar sua busca ou criar um novo grafo.'
            }
          </p>
          <div className="flex justify-center gap-4">
            <Button 
              onClick={() => setIsCreateDialogOpen(true)}
              className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
            >
              <Plus className="mr-2 h-4 w-4" />
              Criar Grafo
            </Button>
            <Button 
              onClick={handleNewEmptyGraph}
              variant="outline"
              className="border-blue-600 text-blue-600 hover:bg-blue-50"
            >
              Abrir Editor Visual
            </Button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredGrafos.map((grafo) => (
            <div 
              key={grafo.id}
              className="bg-white rounded-lg border shadow-sm overflow-hidden hover:shadow-md transition-shadow"
            >
              <div className="p-5">
                <h3 className="font-semibold text-lg mb-1 truncate">{grafo.nome}</h3>
                <div className="text-sm text-gray-500 space-y-1">
                  <p>Vértices: {grafo.num_vertices}</p>
                  <p>Arestas: {grafo.num_arestas}</p>
                  <p>
                    {grafo.direcionado ? 'Direcionado' : 'Não direcionado'}
                    {grafo.ponderado ? ', Ponderado' : ''}
                    {grafo.bipartido ? ', Bipartido' : ''}
                  </p>
                </div>
              </div>
              <div className="bg-gray-50 px-5 py-3 flex justify-between">
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => handleOpenEditor(grafo.id)}
                >
                  Editar
                </Button>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={() => handleDeleteGraph(grafo.id)}
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  Excluir
                </Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GraphVisualEditor;
