
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
          <Button variant="outline" className="border-blue-600 text-blue-600 hover:bg-blue-50">
            <Upload className="mr-2 h-4 w-4" />
            Importar
          </Button>
          <Button variant="outline" className="border-green-600 text-green-600 hover:bg-green-50">
            <Download className="mr-2 h-4 w-4" />
            Exportar
          </Button>
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
