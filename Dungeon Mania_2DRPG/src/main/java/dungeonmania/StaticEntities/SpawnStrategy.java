package dungeonmania.StaticEntities;

import dungeonmania.GameMap;
import dungeonmania.util.Position;

public interface SpawnStrategy {
    /**
     * Strategy interface for spawning zombies. Used in ZombieToastSpawner.
     * @param tick current number of ticks
     * @param spawnerPosition the position of the spawner calling this strategy
     * @param gameMap the map on which the entities are located
     * @return returns the position of where the zombie is being spawned.
     */
    public Position spawn(int tick, Position spawnerPosition, GameMap gameMap);

}
