
import React from 'react';
import { EdgeProps, getStraightPath } from '@xyflow/react';

const CustomEdge = ({ id, sourceX, sourceY, targetX, targetY, markerEnd }: EdgeProps) => {
  const [edgePath] = getStraightPath({ sourceX, sourceY, targetX, targetY });
  return (
    <path
      id={id}
      d={edgePath}
      stroke="#000"
      strokeWidth={2}
      fill="none"
      markerEnd={markerEnd}
    />
  );
};

export default CustomEdge;
