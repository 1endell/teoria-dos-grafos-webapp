import { Handle } from '@xyflow/react';

export default function CustomNode({ id }) {
  const size = 60; // Tamanho do nó e do handle

  return (
    <div
      style={{
        background: '#4f46e5',
        color: 'white',
        borderRadius: '50%',
        width: size,
        height: size,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        position: 'relative', // Para posicionar o Handle dentro do nó
      }}
    >
      {id}

      {/* Handle cobrindo toda a área do Node */}
      <Handle
        type="source"
        position="top"
        style={{
          width: size,
          height: size,
          position: 'absolute',
          top: 0,
          left: 0,
          borderRadius: '50%',
          opacity: 0,
          cursor: 'crosshair',
        }}
      />

      <Handle
        type="target"
        position="top"
        style={{
          width: size,
          height: size,
          position: 'absolute',
          top: 0,
          left: 0,
          borderRadius: '50%',
          opacity: 0,
        }}
      />
    </div>
  );
}
