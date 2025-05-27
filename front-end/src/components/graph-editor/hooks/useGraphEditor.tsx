import { useState, useRef } from 'react';
import Graph from 'graphology';
import { Grafo, VerticeCreate, ArestaCreate, GrafoCreate } from '@/types/graph';
import { graphService } from '@/services/graphService';
import { useToast } from '@/hooks/use-toast';
import { EditorMode, GraphEditorState, NodeProperties, EdgeProperties } from '../types';
import { generateNodeName } from '../utils';
import { useCallback, useEffect, useState, useRef } from "react";
import { useSigma } from "react-sigma-v2";
import { useSigmaInstance } from './useSigmaInstance';

export function useGraphEditor(grafoId, onSave) {
  const [state, setState] = useState({
    isDirected: true,
    isWeighted: false,
    layoutType: 'circular',
    mode: 'select',
    selectedNode: null,
    sourceNode: null,
    nodeProperties: {},
    edgeProperties: {},
    isLoading: false,
    grafoNome: ''
  });
  
  const graphRef = useRef(new Graph());
  const grafoInfo = useRef(null);
  const { refresh } = useSigmaInstance();

  useEffect(() => {
    if (grafoId) loadGrafo(grafoId);
    else initEmptyGraph();
  }, [grafoId]);

  function updateState(updates) {
    setState(prev => ({ ...prev, ...updates }));
  }

  function loadGrafo(id) {
    updateState({ isLoading: true });
    return fetch(`/api/grafos/${id}`)
      .then(res => res.json())
      .then(data => {
        const graph = new Graph();
        data.nodes.forEach(node => graph.addNode(node.id, node));
        data.edges.forEach(edge => graph.addEdge(edge.source, edge.target, edge));
        graphRef.current = graph;
        grafoInfo.current = data.info;
        updateState({
          isDirected: data.isDirected,
          isWeighted: data.isWeighted,
          layoutType: data.layoutType,
          grafoNome: data.info?.nome || ''
        });
        return graph;
      })
      .finally(() => updateState({ isLoading: false }));
  }

  function initEmptyGraph() {
    const graph = new Graph();
    graphRef.current = graph;
    return graph;
  }

  function addNode({ x, y }) {
    const id = String(graphRef.current.order + 1);
    graphRef.current.addNode(id, { label: id, x, y, size: 10, color: '#1E88E5' });
    return true;
  }

  function addEdge(source, target) {
    if (!graphRef.current.hasEdge(source, target)) {
      graphRef.current.addEdge(source, target, { label: `${source}-${target}` });
      return true;
    }
    return false;
  }

  function removeSelectedNode() {
    if (state.selectedNode && graphRef.current.hasNode(state.selectedNode)) {
      graphRef.current.dropNode(state.selectedNode);
      updateState({ selectedNode: null });
      return true;
    }
    return false;
  }

  function saveGraph() {
    const data = {
      nodes: graphRef.current.nodes().map(id => ({
        id,
        ...graphRef.current.getNodeAttributes(id)
      })),
      edges: graphRef.current.edges().map(id => {
        const [source, target] = graphRef.current.extremities(id);
        return { id, source, target, ...graphRef.current.getEdgeAttributes(id) };
      }),
      info: grafoInfo.current
    };
    onSave?.(data);
  }

  function handleModeChange(newMode) {
    updateState({ mode: newMode });
  }

  return {
    state,
    updateState,
    grafoInfo,
    graphRef,
    loadGrafo,
    initEmptyGraph,
    addNode,
    addEdge,
    removeSelectedNode,
    saveGraph,
    handleModeChange
  };
}
