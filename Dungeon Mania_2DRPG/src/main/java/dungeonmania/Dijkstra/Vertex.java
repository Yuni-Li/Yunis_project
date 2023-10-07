package dungeonmania.Dijkstra;

import dungeonmania.util.Position;

public class Vertex {
    final private String id;
    //final private String name;
    final private Position position;

    public Vertex(String id, Position pos) {
        this.id = id;
        //this.name = id;
        this.position = pos;
    }
    public String getId() {
        return id;
    }

    /*
    public String getName() {
        return name;
    }
    */

    public Position getPosition() {
        return position;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj)
            return true;
        if (obj == null)
            return false;
        if (getClass() != obj.getClass())
            return false;
        Vertex other = (Vertex) obj;

        if (other.getPosition().equals(this.position)){
            return true;
        }
        if (id == null) {
            if (other.id != null)
                return false;
        } 
        else if (!id.equals(other.id))
            return false;
        return true;
    }

    /*
    @Override
    public String toString() {
        return name;
    }
    */
}
