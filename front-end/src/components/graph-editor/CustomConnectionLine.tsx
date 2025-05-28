import React from 'react';
import { ConnectionLineComponentProps, getStraightPath } from 'reactflow';

const CustomConnectionLine: React.FC<ConnectionLineComponentProps> = ({
  fromX,
  fromY,
  toX,
  toY,
}) => {
  const [edgePath] = getStraightPath({
    sourceX: fromX,
    sourceY: fromY,
    targetX: toX,
    targetY: toY,
  });

  return (
    <path
      fill="none"
      stroke="#b1b1b7"
      strokeWidth={2}
      className="animated"
      d={edgePath}
    />
  );
};

export default CustomConnectionLine;
