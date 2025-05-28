import React from 'react';
import { EdgeProps, getStraightPath } from 'reactflow';

const CustomEdge = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  style = {},
  markerEnd,
}: EdgeProps) => {
  // Utilizamos getStraightPath para uma linha reta
  const [edgePath] = getStraightPath({
    sourceX,
    sourceY,
    targetX,
    targetY,
  });

  return (
    <>
      <path
        id={id}
        style={{
          ...style,
          stroke: '#333',
          strokeWidth: 2,
          zIndex: 1, // Opcional, para garantir que a linha fique atrás dos nós
        }}
        className="react-flow__edge-path"
        d={edgePath}
        markerEnd={markerEnd}
      />
    </>
  );
};

export default CustomEdge;
