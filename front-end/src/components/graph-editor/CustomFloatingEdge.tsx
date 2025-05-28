import React from 'react';
import { EdgeProps, getStraightPath } from 'reactflow';

const CustomFloatingEdge: React.FC<EdgeProps> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  style = {},
  markerEnd,
}) => {
  const [edgePath] = getStraightPath({ sourceX, sourceY, targetX, targetY });

  return (
    <path
      id={id}
      style={{ ...style, stroke: '#333', strokeWidth: 2 }}
      className="react-flow__edge-path"
      d={edgePath}
      markerEnd={markerEnd}
    />
  );
};

export default CustomFloatingEdge;
