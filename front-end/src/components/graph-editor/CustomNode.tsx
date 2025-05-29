import React from 'react';

const CustomNode = ({ data, selected }) => {
  const { label, color = '#4f46e5', size = 60 } = data;

  return (
    <div
      style={{
        background: color,
        border: selected ? '3px solid #333' : '2px solid #1e40af',
        borderRadius: '50%',
        width: size,
        height: size,
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontWeight: 'bold',
        fontSize: size / 3,
        color: 'white',
        position: 'relative',
        cursor: 'pointer',
        userSelect: 'none',
      }}
    >
      {label}
    </div>
  );
};

export default CustomNode;
