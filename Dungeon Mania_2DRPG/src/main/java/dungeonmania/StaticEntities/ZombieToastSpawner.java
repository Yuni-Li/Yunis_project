package dungeonmania.StaticEntities;

import java.util.List;

import dungeonmania.Entity;
import dungeonmania.GameMap;
import dungeonmania.MovingEntities.ZombieToast;
import dungeonmania.util.Position;

public class ZombieToastSpawner extends Entity {
    private Position spawnerPosition;
    private GameMap gameMap;
    private SpawnStrategy spawnStrategy;

    /**
     * Constructor for a ZombieToastSpawner.
     * @param id unique id of object
     * @param type the type of object as string
     * @param position the position of the object on the map
     * @param gameMap the map of the game as an object
     * @param spawnStrategy Strategy pattern object for spawning zombies (set differently depending on gameMode)
     */
    public ZombieToastSpawner(String id, String type, Position position, GameMap gameMap, SpawnStrategy spawnStrategy) {
        super(id, type);
        this.spawnerPosition = position;
        this.gameMap = gameMap;
        this.spawnStrategy = spawnStrategy;
    }

    /**
     * gets position of the ZombieToastSpawner
     * @return returns spawner position
     */
    public Position getSpawnerPosition() {
        return spawnerPosition;
    }

    /**
     * sets position of the ZombieToastSpawner
     * @param spawnerPosition the spawner's position
     */
    public void setSpawnerPosition(Position spawnerPosition) {
        this.spawnerPosition = spawnerPosition;
    }

    /**
     * Gets the position of where a zombie will spawn.
     * @param tick the current number of ticks that have occurred
     * @return returns the positon of where the zombie is about to be spawner. Returns null if no valid position available.
     */
    public Position spawnZombie(int tick) {
        return spawnStrategy.spawn(tick, spawnerPosition, gameMap);

    }

}
