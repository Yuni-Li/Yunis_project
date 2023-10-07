package dungeonmania.CollectableEntities;

import java.util.Random;

import dungeonmania.Entity;

public abstract class DurableEntity extends Entity {

    private int durability;

    /**
     * an entity with durability.
     * @param id
     * @param type
     */
    public DurableEntity(String id, String type) {
        super(id, type);
        
        durability = randomDurability();
    }

    /**
     * 
     * @return durability between 15 and 30 inclusive
     */
    private int randomDurability() {
        Random random = new Random();
        int randomInt = 0;
        while (randomInt < 15) {
            randomInt = random.nextInt(31);
        }
        return randomInt;
        
    }

    public int getDurability() {
        return durability;
    }

    public void decrementDurability() {
        durability--;
    }

}
