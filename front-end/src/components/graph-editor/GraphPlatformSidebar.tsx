
import React, { useState, useEffect } from 'react';
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarHeader,
  SidebarTrigger,
} from '@/components/ui/sidebar';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { graphService } from '@/services/graphService';
import { GrafoInfo } from '@/types/graph';
import { useToast } from '@/hooks/use-toast';

interface GraphPlatformSidebarProps {
  onLoadGrafo: (grafoId: string) => void;
}

const GraphPlatformSidebar: React.FC<GraphPlatformSidebarProps> = ({ onLoadGrafo }) => {
  const [grafos, setGrafos] = useState<GrafoInfo[]>([]);
  const [algoritmos, setAlgoritmos] = useState<any[]>([]);
  const [selectedGrafo1, setSelectedGrafo1] = useState<string>('');
  const [selectedGrafo2, setSelectedGrafo2] = useState<string>('');
  const [selectedAlgoritmo, setSelectedAlgoritmo] = useState<string>('');
  const [operationResult, setOperationResult] = useState<string>('');
  const [algorithmResult, setAlgorithmResult] = useState<any>(null);
  const { toast } = useToast();

  useEffect(() => {
    loadGrafos();
    loadAlgoritmos();
  }, []);

  const loadGrafos = async () => {
    try {
      const response = await graphService.listarGrafos();
      setGrafos(response.grafos);
    } catch (error) {
      console.error('Error loading graphs:', error);
    }
  };

  const loadAlgoritmos = async () => {
    try {
      const response = await graphService.listarAlgoritmos();
      setAlgoritmos(response);
    } catch (error) {
      console.error('Error loading algorithms:', error);
    }
  };

  const handleGraphOperation = async (operation: string) => {
    if (!selectedGrafo1 || !selectedGrafo2) {
      toast({
        title: "Erro",
        description: "Selecione dois grafos para a operação.",
        variant: "destructive",
      });
      return;
    }

    try {
      let result;
      const nomeResultado = `${operation}_${Date.now()}`;
      
      switch (operation) {
        case 'uniao':
          result = await graphService.unirGrafos(selectedGrafo1, selectedGrafo2, nomeResultado);
          break;
        case 'intersecao':
          result = await graphService.intersecaoGrafos(selectedGrafo1, selectedGrafo2, nomeResultado);
          break;
        case 'diferenca':
          result = await graphService.diferencaGrafos(selectedGrafo1, selectedGrafo2, nomeResultado);
          break;
        case 'diferenca-simetrica':
          result = await graphService.diferencaSimetricaGrafos(selectedGrafo1, selectedGrafo2, nomeResultado);
          break;
        case 'composicao':
          result = await graphService.composicaoGrafos(selectedGrafo1, selectedGrafo2, nomeResultado);
          break;
      }

      if (result) {
        setOperationResult(`Operação ${operation} concluída! Novo grafo: ${result.nome}`);
        loadGrafos(); // Recarregar lista de grafos
        toast({
          title: "Sucesso",
          description: `Operação ${operation} realizada com sucesso!`,
        });
      }
    } catch (error) {
      toast({
        title: "Erro",
        description: `Erro ao executar operação ${operation}.`,
        variant: "destructive",
      });
    }
  };

  const handleAlgorithmExecution = async () => {
    if (!selectedAlgoritmo || !selectedGrafo1) {
      toast({
        title: "Erro",
        description: "Selecione um algoritmo e um grafo.",
        variant: "destructive",
      });
      return;
    }

    try {
      const result = await graphService.executarAlgoritmo(selectedAlgoritmo, selectedGrafo1);
      setAlgorithmResult(result);
      toast({
        title: "Sucesso",
        description: "Algoritmo executado com sucesso!",
      });
    } catch (error) {
      toast({
        title: "Erro",
        description: "Erro ao executar algoritmo.",
        variant: "destructive",
      });
    }
  };

  const menuItems = [
    {
      title: "Grafos Salvos",
      items: grafos.slice(0, 10).map(grafo => ({
        title: grafo.nome,
        onClick: () => onLoadGrafo(grafo.id)
      }))
    },
    {
      title: "Operações",
      items: [
        { title: "União de Grafos", action: "operations" },
        { title: "Interseção de Grafos", action: "operations" },
        { title: "Diferença de Grafos", action: "operations" },
        { title: "Comparar Grafos", action: "comparison" }
      ]
    },
    {
      title: "Algoritmos",
      items: [
        { title: "Executar Algoritmo", action: "algorithms" },
        { title: "Busca em Largura", action: "algorithms" },
        { title: "Busca em Profundidade", action: "algorithms" },
        { title: "Dijkstra", action: "algorithms" }
      ]
    }
  ];

  return (
    <Sidebar>
      <SidebarHeader className="border-b p-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">Plataforma de Grafos</h2>
          <SidebarTrigger />
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        {menuItems.map((section, index) => (
          <SidebarGroup key={index}>
            <SidebarGroupLabel>{section.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {section.items.map((item, itemIndex) => (
                  <SidebarMenuItem key={itemIndex}>
                    <SidebarMenuButton asChild>
                      {item.onClick ? (
                        <button onClick={item.onClick} className="w-full text-left">
                          {item.title}
                        </button>
                      ) : (
                        <Dialog>
                          <DialogTrigger asChild>
                            <button className="w-full text-left">
                              {item.title}
                            </button>
                          </DialogTrigger>
                          <DialogContent className="sm:max-w-md">
                            <DialogHeader>
                              <DialogTitle>{item.title}</DialogTitle>
                            </DialogHeader>
                            
                            {item.action === 'operations' && (
                              <div className="space-y-4">
                                <div>
                                  <Label>Primeiro Grafo</Label>
                                  <Select value={selectedGrafo1} onValueChange={setSelectedGrafo1}>
                                    <SelectTrigger>
                                      <SelectValue placeholder="Selecione um grafo" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {grafos.map(grafo => (
                                        <SelectItem key={grafo.id} value={grafo.id}>
                                          {grafo.nome}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                </div>
                                
                                <div>
                                  <Label>Segundo Grafo</Label>
                                  <Select value={selectedGrafo2} onValueChange={setSelectedGrafo2}>
                                    <SelectTrigger>
                                      <SelectValue placeholder="Selecione um grafo" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {grafos.map(grafo => (
                                        <SelectItem key={grafo.id} value={grafo.id}>
                                          {grafo.nome}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                </div>
                                
                                <div className="flex flex-wrap gap-2">
                                  <Button onClick={() => handleGraphOperation('uniao')} size="sm">
                                    União
                                  </Button>
                                  <Button onClick={() => handleGraphOperation('intersecao')} size="sm">
                                    Interseção
                                  </Button>
                                  <Button onClick={() => handleGraphOperation('diferenca')} size="sm">
                                    Diferença
                                  </Button>
                                  <Button onClick={() => handleGraphOperation('diferenca-simetrica')} size="sm">
                                    Dif. Simétrica
                                  </Button>
                                  <Button onClick={() => handleGraphOperation('composicao')} size="sm">
                                    Composição
                                  </Button>
                                </div>
                                
                                {operationResult && (
                                  <div className="mt-4 p-2 bg-green-50 border border-green-200 rounded">
                                    <p className="text-sm text-green-800">{operationResult}</p>
                                  </div>
                                )}
                              </div>
                            )}
                            
                            {item.action === 'algorithms' && (
                              <div className="space-y-4">
                                <div>
                                  <Label>Selecionar Grafo</Label>
                                  <Select value={selectedGrafo1} onValueChange={setSelectedGrafo1}>
                                    <SelectTrigger>
                                      <SelectValue placeholder="Selecione um grafo" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {grafos.map(grafo => (
                                        <SelectItem key={grafo.id} value={grafo.id}>
                                          {grafo.nome}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                </div>
                                
                                <div>
                                  <Label>Selecionar Algoritmo</Label>
                                  <Select value={selectedAlgoritmo} onValueChange={setSelectedAlgoritmo}>
                                    <SelectTrigger>
                                      <SelectValue placeholder="Selecione um algoritmo" />
                                    </SelectTrigger>
                                    <SelectContent>
                                      {algoritmos.map(alg => (
                                        <SelectItem key={alg.id} value={alg.id}>
                                          {alg.nome}
                                        </SelectItem>
                                      ))}
                                    </SelectContent>
                                  </Select>
                                </div>
                                
                                <Button onClick={handleAlgorithmExecution} className="w-full">
                                  Executar Algoritmo
                                </Button>
                                
                                {algorithmResult && (
                                  <div className="mt-4 p-2 bg-blue-50 border border-blue-200 rounded">
                                    <h4 className="font-medium text-sm mb-2">Resultado:</h4>
                                    <pre className="text-xs overflow-auto max-h-32">
                                      {JSON.stringify(algorithmResult.resultado, null, 2)}
                                    </pre>
                                    <p className="text-xs text-gray-600 mt-2">
                                      Tempo: {algorithmResult.tempo_execucao}ms
                                    </p>
                                  </div>
                                )}
                              </div>
                            )}
                          </DialogContent>
                        </Dialog>
                      )}
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
    </Sidebar>
  );
};

export default GraphPlatformSidebar;
