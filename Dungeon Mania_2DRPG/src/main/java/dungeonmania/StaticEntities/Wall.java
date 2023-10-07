package dungeonmania.StaticEntities;

import dungeonmania.Entity;


public class Wall extends Entity {

    /**
     * constructor for Wall
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public Wall(String id, String type) {
        super(id, type);
    }
}
