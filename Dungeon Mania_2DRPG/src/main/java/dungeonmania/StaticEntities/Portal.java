package dungeonmania.StaticEntities;

import javax.sound.sampled.Port;

import dungeonmania.Entity;

public class Portal extends Entity {

    /**
     * constructor for Portal
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public Portal(String id, String type) {
        super(id, type);
    }
}
