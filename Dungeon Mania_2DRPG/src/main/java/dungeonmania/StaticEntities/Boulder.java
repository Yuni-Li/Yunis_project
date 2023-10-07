package dungeonmania.StaticEntities;

import java.util.ArrayList;

import dungeonmania.Entity;
import dungeonmania.GameMap;
import dungeonmania.util.Direction;
import dungeonmania.util.Position;

public class Boulder extends Entity {
    private ArrayList<FloorSwitch> switchObservers;
    private Position position;
    /**
     * constructor for Boulder
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public Boulder(String id, String type, Position position) {
        super(id, type);
        this.position = position;
        switchObservers = new ArrayList<FloorSwitch>();
    }

    public Position getPosition() {
        return position;
    }

    public void addSwitchObserver(FloorSwitch floorSwitch) {
        switchObservers.add(floorSwitch);
    }

    public boolean move(Direction direction, GameMap gameMap) {
        if (!obstructed(direction, position.translateBy(direction), gameMap)) {
            Position newPosition = position.translateBy(direction);
            gameMap.removeEntity(position.getX(), position.getY(), position.getLayer());
            position = newPosition;
            gameMap.addEntity(this, position.getX(), position.getY(), position.getLayer());
            updateSwitches();
            return true;
        }
        return false;
    }

    private void updateSwitches() {
        for (FloorSwitch floorSwitch : switchObservers) {
            floorSwitch.boulderUpdate();
        }
    }

    private boolean obstructed(Direction direction, Position positionForCheck, GameMap gameMap) {
        Entity entityForCheck = gameMap.getEntity(positionForCheck.getX(), positionForCheck.getY(), 0);
        return !(entityForCheck == null || entityForCheck instanceof FloorSwitch);
    }
    
}
