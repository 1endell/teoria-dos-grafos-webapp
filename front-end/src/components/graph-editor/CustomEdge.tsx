import React from 'react';
import { BaseEdge, EdgeLabelRenderer, getBezierPath, EdgeProps } from 'reactflow';

const CustomEdge: React.FC<EdgeProps> = ({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  style = {},
  markerEnd,
  data
}) => {
  // Definindo estilo customizado (com dados opcionais)
  const strokeColor = data?.color || '#f43f5e'; // Vermelho padrão
  const strokeWidth = data?.width || 3;
  const dashed = data?.dashed ? '5,5' : undefined;

  const [edgePath, labelX, labelY] = getBezierPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition
  });

  return (
    <>
      <BaseEdge
        path={edgePath}
        style={{
          stroke: strokeColor,
          strokeWidth: strokeWidth,
          strokeDasharray: dashed,
          ...style
        }}
        markerEnd={markerEnd}
      />
      {data?.label && (
        <EdgeLabelRenderer>
          <div
            style={{
              position: 'absolute',
              transform: `translate(-50%, -50%) translate(${labelX}px,${labelY}px)`,
              background: '#fff',
              padding: '2px 4px',
              borderRadius: 4,
              fontSize: 12,
              pointerEvents: 'all',
              border: `1px solid ${strokeColor}`
            }}
          >
            {data.label}
          </div>
        </EdgeLabelRenderer>
      )}
    </>
  );
};

export default CustomEdge;
