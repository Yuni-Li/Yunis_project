package dungeonmania.CollectableEntities;

import dungeonmania.Entity;

public class Treasure extends Entity {

    /**
     * constructor for Treasure
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public Treasure(String id, String type) {
        super(id, type);
    }
    
}
