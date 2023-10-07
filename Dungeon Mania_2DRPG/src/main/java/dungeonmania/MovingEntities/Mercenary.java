package dungeonmania.MovingEntities;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

import dungeonmania.GameMap;
import dungeonmania.Dijkstra.DijkstraAlgo;
import dungeonmania.Dijkstra.Graph;
import dungeonmania.Dijkstra.Vertex;
import dungeonmania.util.Position;

public class Mercenary extends Npc{
    private Graph dijkstraGraph;
    private boolean underSpectreInfluence;
    private Player player;
    
    
    public Mercenary(String id, String type, Position position, Player player, GameMap gameMap, Graph dijkstraGraph){
        super(id, type, position, gameMap);
        this.player = player;
        this.dijkstraGraph  = dijkstraGraph;
        this.underSpectreInfluence = false;
        this.setAttack(10);
    }

    /**
     * Move method uses Dijkstra algorithm so that it will always move towards the player
     * in the shortest path possible
     */
    public void move(){
        Position target = this.player.getPosition();
        Vertex player;

        if(this.isEnemy() || !isUnderSpectreInfluence()){
            player = dijkstraGraph.findVertex(target);
        }

        else {
            List<Position> adjPosList = target.getAdjacentPositions();
            player = dijkstraGraph.findVertex(getPosFromList(adjPosList));
        }

        Vertex merc = dijkstraGraph.findVertex(this.getPosition());
        
        DijkstraAlgo dijkstra = new DijkstraAlgo(dijkstraGraph);
        dijkstra.execute(merc);
        LinkedList<Vertex> path = dijkstra.getPath(player);
        if(path!=null){
            Vertex nextVertex = path.get(1);
            int tempLayer = this.getPosition().getLayer();
            this.setPosition(nextVertex.getPosition());
            Position newPosition = new Position(this.getPosition().getX(), this.getPosition().getY(), tempLayer);
            this.setPosition(newPosition);
        }

    }

    /**
     * Bribe method allows the mercenary to accept bribes. 
     * @param amountReceived
     * @param giveOneRing
     * @return boolean depending on whether a OneRing was received or not
     */
    public boolean bribe(int amountReceived, boolean giveOneRing){
        int requiredAmount = 1;

        if(amountReceived >= requiredAmount) {
            this.setEnemy(false);
            return true;
        }

        else{
            this.setEnemy(true);
            return false;
        }
    }

    private Position getPosFromList(List<Position> adjPosList){
        for(Position adjPos : adjPosList){
            if(this.getGameMap().getEntity(adjPos.getX(), adjPos.getY(), 0) == null){
                if(this.getGameMap().getEntity(adjPos.getX(), adjPos.getY(), player.getPosition().getLayer()) == null){
                    return adjPos;
                }
            }
        }
        return null;
    }

    public boolean isUnderSpectreInfluence() {
        return underSpectreInfluence;
    }

    public void setUnderSpectreInfluence(boolean underSpectreInfluence) {
        this.underSpectreInfluence = underSpectreInfluence;
    }
 }
