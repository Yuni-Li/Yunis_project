package dungeonmania.BuildableEntities;

import java.util.Random;

import dungeonmania.Entity;

public abstract class BuildableEntity extends Entity {
    
    private int durability;

    public BuildableEntity(String id, String type, int durabilityOffset) {
        super(id, type);
        this.durability = generateDurability(durabilityOffset);
    }

    public int getDurability() {
        return durability;
    }

    /**
     * generate a random durability between offset and durability offset + 40.
     * @return durability
     */
    private int generateDurability(int durabilityOffset) {
        Random random = new Random();
        return durabilityOffset + random.nextInt(26);
    }

    public void updateDurability(int change) {
        durability -= change;
    }

}
