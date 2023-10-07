package dungeonmania.CollectableEntities;

import dungeonmania.Entity;

public class Key extends Entity {
    private Integer keyPairId;
    /**
     * constructor for Key
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public Key(String id, String type, Integer keyPairId) {
        super(id, type);
        this.keyPairId = keyPairId;
    }

    public Integer getKeyPairId() {
        return keyPairId;
    }

}
