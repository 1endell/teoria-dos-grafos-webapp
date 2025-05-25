
import React from 'react';
import Header from '@/components/Header';
import Dashboard from '@/components/Dashboard';
import { SessionProvider } from '@/context/SessionContext';

const Index = () => {
  return (
    <SessionProvider>
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
        <Header />
        <main>
          <Dashboard />
        </main>
      </div>
    </SessionProvider>
  );
};

export default Index;
