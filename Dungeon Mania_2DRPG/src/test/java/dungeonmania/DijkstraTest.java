package dungeonmania;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import org.junit.jupiter.api.Test;

import dungeonmania.Dijkstra.DijkstraAlgo;
import dungeonmania.Dijkstra.Edge;
import dungeonmania.Dijkstra.Graph;
import dungeonmania.Dijkstra.Vertex;
import dungeonmania.util.Position;


public class DijkstraTest {

    private List<Vertex> nodes;
    private List<Edge> edges;

    //Basic test on just a grid
    @Test
    public void testExcute() {
        nodes = new ArrayList<Vertex>();
        edges = new ArrayList<Edge>();
        
        int verticeCount = 0;
        for (int i = 0; i < 3; i++) {
            for(int j = 0; j < 3; j++){
                Vertex location = new Vertex("Node_" + verticeCount, new Position(i, j));
                nodes.add(location);
                verticeCount +=1;
            }
        }

        addLane("Edge_0", 0, 1, 100);
        addLane("Edge_1", 0, 3, 1);
        addLane("Edge_2", 1, 0, 1);
        addLane("Edge_3", 1, 4, 1);
        addLane("Edge_4", 1, 2, 1);
        addLane("Edge_5", 2, 1, 100);
        addLane("Edge_6", 2, 5, 1);
        addLane("Edge_7", 3, 0, 1);
        addLane("Edge_8", 3, 4, 1);
        addLane("Edge_9", 3, 6, 1);
        addLane("Edge_10", 4, 1, 100);
        addLane("Edge_10", 4, 3, 1);
        addLane("Edge_11", 4, 5, 1);
        addLane("Edge_10", 4, 7, 100);
        addLane("Edge_10", 5, 2, 1);
        addLane("Edge_10", 5, 4, 1);
        addLane("Edge_10", 5, 8, 1);
        addLane("Edge_10", 6, 3, 1);
        addLane("Edge_10", 6, 7, 100);
        addLane("Edge_10", 7, 6, 1);
        addLane("Edge_10", 7, 4, 1);
        addLane("Edge_10", 7, 8, 1);
        addLane("Edge_10", 8, 7, 100);
        addLane("Edge_10", 8, 5, 1);

        // Lets check from location Loc_0 to Loc_8
        Graph graph = new Graph(nodes, edges);
        DijkstraAlgo dijkstra = new DijkstraAlgo(graph);
        dijkstra.execute(graph.getVertexes().get(0));
        LinkedList<Vertex> path = dijkstra.getPath(graph.getVertexes().get(8));

        assertNotNull(path);
        assertTrue(path.size() > 0);

    }

    private void addLane(String laneId, int sourceLocNo, int destLocNo,
            int duration) {
        Edge lane = new Edge(laneId,nodes.get(sourceLocNo), nodes.get(destLocNo), duration );
        edges.add(lane);

    }   
}