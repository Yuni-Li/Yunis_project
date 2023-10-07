package dungeonmania;

public abstract class Entity {
    private String id;
    private String type;

    /**
     * constructor for Entity
     * @param id unique id
     * @param type the type of Entity the object is
     */
    public Entity(String id, String type) {
        this.id = id;
        this.type = type;
    }

    public String getId() {
        return id;
    }

    public String getType() {
        return type;
    }
}

