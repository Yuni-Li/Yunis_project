package dungeonmania.StaticEntities;

import dungeonmania.Entity;

public class Swamp extends Entity{
    private int movementFactor;
    public Swamp(String id, String type, int movementFactor) {
        super(id, type);
        this.movementFactor = movementFactor;
    }
    public int getMovementFactor() {
        return movementFactor;
    }    
}
