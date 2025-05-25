
import React from 'react';
import { Button } from '@/components/ui/button';
import { Github, Network } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-gradient-to-r from-blue-900 via-purple-900 to-indigo-900 text-white shadow-lg">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Network className="h-8 w-8 text-blue-300" />
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-300 to-purple-300 bg-clip-text text-transparent">
                Teoria dos Grafos
              </h1>
              <p className="text-sm text-blue-200">Plataforma de Estudos Interativa</p>
            </div>
          </div>
          
          <Button
            onClick={() => window.open('https://github.com/1endell/teoria-dos-grafos-webapp', '_blank')}
            variant="outline"
            className="bg-transparent border-blue-300 text-blue-300 hover:bg-blue-300 hover:text-blue-900 transition-colors"
          >
            <Github className="mr-2 h-5 w-5" />
            GitHub
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;
