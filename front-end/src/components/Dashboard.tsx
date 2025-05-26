
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Plus, Search, Download, Upload } from 'lucide-react';
import { graphService } from '@/services/graphService';
import { GrafoInfo, GrafoCreate } from '@/types/graph';
import GraphCard from './GraphCard';
import { useToast } from '@/hooks/use-toast';

const Dashboard: React.FC = () => {
  const [grafos, setGrafos] = useState<GrafoInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newGraph, setNewGraph] = useState<GrafoCreate>({
    nome: '',
    direcionado: false,
    ponderado: false,
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
  const { toast } = useToast();

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
      await graphService.criarGrafo(newGraph);
      toast({
        title: "Sucesso",
        description: "Grafo criado com sucesso!",
      });
      setIsCreateDialogOpen(false);
      setNewGraph({
        nome: '',
        direcionado: false,
        ponderado: false,
        bipartido: false,
      });
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
      loadGrafos();
    } catch (error) {
      toast({
        title: "Erro",
        description: "Não foi possível excluir o grafo.",
        variant: "destructive",
      });
    }
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
          <Button 
            onClick={() => setIsCreateDialogOpen(true)}
            className="bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
          >
            <Plus className="mr-2 h-4 w-4" />
            Criar Primeiro Grafo
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {filteredGrafos.map((grafo) => (
            <GraphCard
              key={grafo.id}
              grafo={grafo}
              onView={(id) => console.log('View graph:', id)}
              onEdit={(id) => console.log('Edit graph:', id)}
              onDelete={handleDeleteGraph}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
