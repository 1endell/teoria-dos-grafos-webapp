export default function CustomNode({ id }) {
  return (
    <div
      style={{
        background: '#4f46e5',
        color: 'white',
        borderRadius: '50%',
        width: 24, // Tamanho reduzido (40%)
        height: 24,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        cursor: 'move',
      }}
    >
      {id}
    </div>
  );
}
