import { Handle } from '@xyflow/react';

export default function CustomNode({ id, data }) {
  const size = 60 * 0.4;
  const showHandles = data?.mode === 'addEdge';

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
        cursor: 'move',
        position: 'relative',
      }}
    >
      {id}

      {showHandles && (
        <>
          {/* Handle para iniciar a conexão */}
          <Handle
            type="source"
            position="right"
            isConnectable={true}
            style={{
              width: 10,
              height: 10,
              background: 'red', // Visível para teste
              borderRadius: '50%',
              right: -5, // Posição relativa ao nó
              top: '50%',
              transform: 'translateY(-50%)',
            }}
          />
          {/* Handle para finalizar a conexão */}
          <Handle
            type="target"
            position="left"
            isConnectable={true}
            style={{
              width: 10,
              height: 10,
              background: 'blue', // Visível para teste
              borderRadius: '50%',
              left: -5, // Posição relativa ao nó
              top: '50%',
              transform: 'translateY(-50%)',
            }}
          />
        </>
      )}
    </div>
  );
}
