package dungeonmania.StaticEntities;

import java.util.ArrayList;

import dungeonmania.Entity;
import dungeonmania.Goals.BouldersGoal;
import dungeonmania.util.Position;

public class FloorSwitch extends Entity {
    private ArrayList<Boulder> boulderSubjects;
    private BouldersGoal bouldergoal;
    private Position position;
    private boolean active;
    /**
     * constructor for FloorSwitch
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public FloorSwitch(String id, String type, Position position) {
        super(id, type);
        this.position = position;
        boulderSubjects = new ArrayList<Boulder>();
        bouldergoal = null;
        active = false;
    }

    public void addBoulderSubject(Boulder boulder) {
        boulderSubjects.add(boulder);
    }
    
    public void boulderUpdate() {
        boolean wasActive = active;
        boolean flipped = false;
        active = false;
        for (Boulder boulder : boulderSubjects) {
            if (boulder.getPosition().equals(position)) {
                active = true;
                break;
            }
            
        }

        if (wasActive != active) {
            flipped = true;
        }

        if (flipped && !active) {
            bouldergoal.incrementSwitches();
        }
        if (flipped && active) {
            bouldergoal.decrementSwitches();
        }
        
    }

    public void boulderInitialise(Boulder boulder) {
        if (boulder.getPosition().equals(position)) {
            active = true;
        }
    }

    public void addBoulderGoal(BouldersGoal leafObserver) {
        bouldergoal = leafObserver;
    }

    public boolean isActive() {
        return active;
    }

}
