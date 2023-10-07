package dungeonmania.StaticEntities;

import java.util.List;

import dungeonmania.GameMap;
import dungeonmania.util.Position;

public class HardSpawn implements SpawnStrategy{
    /**
     * Strategy interface for spawning zombies on Hard difficulty. Used in ZombieToastSpawner.
     * @param tick current number of ticks
     * @param spawnerPosition the position of the spawner calling this strategy
     * @param gameMap the map on which the entities are located
     * @return returns the position of where the zombie is being spawned.
     */
    @Override
    public Position spawn(int tick, Position spawnerPosition, GameMap gameMap) {
        List<Position> adjacent = spawnerPosition.getAdjacentPositions();
        Position zombiePos = null;

        if (tick % 15 == 0) { 
            for (Position pos: adjacent) {
                if (!obstructed(pos, gameMap)) {
                    zombiePos = pos;
                    break;
                }
            }

        }

        return zombiePos;
    }

    /**
     * Helper function for spawn. Checks if the current position isn't obstructed by a wall/boulder/door.
     * @param currPos the current cell being checked for obstruction
     * @param gameMap the map on which entities are located
     * @return true of obsructed, false if not.
     */
    private boolean obstructed(Position currPos, GameMap gameMap){

        for (int i = 0; i < 3; i++) {
            if (gameMap.getEntity(currPos.getX(), currPos.getY(), i) == null) {
                return false;
            }

            String type = gameMap.getEntity(currPos.getX(), currPos.getY(), i).getType();
            if (type.equals("wall") || type.equals("boulder") || type.equals("door")) {
                return true;
            }
        }
        
        return false;
    }
}
