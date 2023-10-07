package dungeonmania.Dijkstra;

import java.util.List;

import dungeonmania.util.Position;

public class Graph {
    private final List<Vertex> vertexes;
    private final List<Edge> edges;

    public Graph(List<Vertex> vertexes, List<Edge> edges) {
        this.vertexes = vertexes;
        this.edges = edges;
    }

    public List<Vertex> getVertexes() {
        return vertexes;
    }

    public List<Edge> getEdges() {
        return edges;
    }   

    public Vertex findVertex(Position pos){
        for(Vertex node : vertexes){
            if(pos.equals(node.getPosition())){
                return node;
            }
        }

        return null;
    }
}
