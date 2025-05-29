import { Handle } from 'reactflow';

export default function CustomNode({ id }) {
  const nodeSize = 60; // Tamanho do nó
  const handleSize = nodeSize * 0.5; // Tamanho do handle (50% menor)

  return (
    <div
      style={{
        background: '#4f46e5',
        color: 'white',
        borderRadius: '50%',
        width: nodeSize,
        height: nodeSize,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        cursor: 'move',
        position: 'relative',
      }}
    >
      {id}

      {/* Handle central para iniciar conexão */}
      <Handle
        type="source"
        position="top"
        style={{
          width: handleSize,
          height: handleSize,
          background: 'transparent', // Invisível ou defina cor se quiser
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          borderRadius: '50%',
          border: '2px solid red', // Visível para teste, remova depois
          cursor: 'crosshair',
        }}
        isConnectable={true}
      />
    </div>
  );
}
