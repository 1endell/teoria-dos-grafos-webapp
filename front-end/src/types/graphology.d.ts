declare module 'graphology' {
  export default class Graph {
    constructor(options?: any);
    forEachNode(callback: (nodeId: string, attributes: any) => void): void;
    addNode(nodeId: string, attributes?: any): void;
    dropNode(nodeId: string): void;
    hasNode(nodeId: string): boolean;
    forEachEdge(callback: (edgeId: string, attributes: any, source: string, target: string, sourceAttributes: any, targetAttributes: any) => void): void;
    addEdge(source: string, target: string, attributes?: any): void;
    hasEdge(edgeId: string): boolean;
    getNodeAttribute(nodeId: string, attribute: string): any;
    setEdgeAttribute(edgeId: string, attribute: string, value: any): void;
    order: number;
    size: number;
  }
}
