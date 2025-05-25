
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Eye, Edit, Trash2, Calendar } from 'lucide-react';
import { GrafoInfo } from '@/types/graph';

interface GraphCardProps {
  grafo: GrafoInfo;
  onView: (id: string) => void;
  onEdit: (id: string) => void;
  onDelete: (id: string) => void;
}

const GraphCard: React.FC<GraphCardProps> = ({ grafo, onView, onEdit, onDelete }) => {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <Card className="hover:shadow-lg transition-shadow duration-200 bg-gradient-to-br from-white to-gray-50 border-l-4 border-l-blue-500">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg font-semibold text-gray-800 truncate">
            {grafo.nome}
          </CardTitle>
          <div className="flex space-x-1">
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onView(grafo.id)}
              className="h-8 w-8 p-0 hover:bg-blue-100"
            >
              <Eye className="h-4 w-4 text-blue-600" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onEdit(grafo.id)}
              className="h-8 w-8 p-0 hover:bg-green-100"
            >
              <Edit className="h-4 w-4 text-green-600" />
            </Button>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => onDelete(grafo.id)}
              className="h-8 w-8 p-0 hover:bg-red-100"
            >
              <Trash2 className="h-4 w-4 text-red-600" />
            </Button>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-3">
        <div className="flex flex-wrap gap-2">
          {grafo.direcionado && (
            <Badge variant="secondary" className="bg-blue-100 text-blue-800">
              Direcionado
            </Badge>
          )}
          {grafo.ponderado && (
            <Badge variant="secondary" className="bg-green-100 text-green-800">
              Ponderado
            </Badge>
          )}
          {grafo.bipartido && (
            <Badge variant="secondary" className="bg-purple-100 text-purple-800">
              Bipartido
            </Badge>
          )}
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Vértices:</span>
            <span className="font-medium">{grafo.num_vertices}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-600">Arestas:</span>
            <span className="font-medium">{grafo.num_arestas}</span>
          </div>
        </div>

        <div className="flex items-center text-xs text-gray-500 pt-2 border-t">
          <Calendar className="h-3 w-3 mr-1" />
          <span>Criado em {formatDate(grafo.data_criacao)}</span>
        </div>
      </CardContent>
    </Card>
  );
};

export default GraphCard;
