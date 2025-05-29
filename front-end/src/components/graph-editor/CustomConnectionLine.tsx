import React from 'react';
import { ConnectionLineComponentProps, getStraightPath } from 'reactflow';

const CustomConnectionLine = ({ fromX, fromY, toX, toY }: ConnectionLineComponentProps) => {
  const [edgePath] = getStraightPath({ sourceX: fromX, sourceY: fromY, targetX: toX, targetY: toY });
  return (
    <path
      d={edgePath}
      stroke="#000"
      strokeWidth={2}
      fill="none"
    />
  );
};

export default CustomConnectionLine;
