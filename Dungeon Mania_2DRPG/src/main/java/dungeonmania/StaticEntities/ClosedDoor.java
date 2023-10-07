package dungeonmania.StaticEntities;

import dungeonmania.Entity;
import dungeonmania.Inventory;

public class ClosedDoor extends Entity {

    private Integer keyPairId;

    /**
     * constructor for ClosedDoor
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public ClosedDoor(String id, String type, Integer keyPairId) {
        super(id, type);
        this.keyPairId = keyPairId;
    }

    public Integer getKeyPairId() {
        return keyPairId;
    }

    public boolean canOpenDoor(Inventory playerInventory) {
        return playerInventory.hasKey(keyPairId);
    }
}
