package dungeonmania.MovingEntities;

import dungeonmania.GameMap;
import dungeonmania.Dijkstra.Graph;
import dungeonmania.util.Position;

public class Assassin extends Mercenary{

    public Assassin(String id, String type, Position position, Player player, GameMap gameMap, Graph dijkstraGraph) {
        super(id, type, position, player, gameMap, dijkstraGraph);
        this.setAttack(25);
        this.setUnderSpectreInfluence(false);
    }
    
    /**
     * Assassin requires base amount for bribe in addition to the one ring
     * @param amountReceived amount given to the assassin
     * @param giveOneRing true if oneRing is provided
     */
    @Override
    public boolean bribe(int amountReceived, boolean giveOneRing){
        //giveOneRing is true when a OneRing is provided to the assassin

        int requiredAmount = 1;

        if(amountReceived >= requiredAmount && giveOneRing) {
            this.setEnemy(false);
            return true;
        }

        else{
            this.setEnemy(true);
            return false;
        }
    }

}
