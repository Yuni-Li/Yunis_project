package dungeonmania;

import java.util.ArrayList;
import java.util.List;

import dungeonmania.StaticEntities.Boulder;
import dungeonmania.response.models.EntityResponse;
import dungeonmania.util.Position;

public class GameMap {
    private Entity gameMap[][][];

    /**
     * Constructor for GameMap. Initialises the 3d array map of the game.
     * @param width width of map (x)
     * @param length length of map (y)
     * @param height height of map (layer)
     */
    public GameMap(int width, int length, int height) {
        gameMap = new Entity[width][length][height];
    }

    /**
     * adds an entity to the gamemap
     * @param entity entity to be added
     * @param x x position of entity
     * @param y y position of entity
     * @param z z position of entity
     */
    public void addEntity(Entity entity, int x, int y, int z) {
        gameMap[x][y][z] = entity;
    }

    /**
     * get entity from gamemap
     * @param x x position of entity
     * @param y y position of entity
     * @param z z position of entity
     * @return returns the entity object
     */
    public Entity getEntity(int x, int y, int z) {
        return gameMap[x][y][z];
    }

    /**
     * get the max width of map
     * @return
     */
    public int getWidth() {
        return gameMap.length;
    }

    /**
     * get max length of map
     * @return
     */
    public int getLength() {
        return gameMap[0].length;
    }

    /**
     * get max height of map
     * @return
     */
    public int getHeight() {
        return gameMap[0][0].length;
    }

    /**
     * remove an entity from the map
     * @param x x position of entity
     * @param y y position of entity
     * @param z z position of entity
     */
    public void removeEntity(int x, int y, int z) {
        gameMap[x][y][z] = null;
    }

    /**
     * makes a list of entity responses of everything in the map
     * @return returns a list of entity responses
     */
    public List<EntityResponse> makeEntityResponseList() {
        List<EntityResponse> entityResponseList = new ArrayList<>();
        // loop through all entities on map and make dungeonresponse
        for(int i = 0 ; i < this.getWidth() ; i++){
            for(int j = 0 ; j < this.getLength() ; j++){
                for(int k=0 ; k < this.getHeight() ; k++){
            
                    if (this.getEntity(i, j, k) != null) {
                        Entity currEntity = this.getEntity(i, j, k);
                        Position currPosition = new  Position(i, j, k);
                        Boolean interactable = (currEntity.getType().equals("mercenary") || currEntity.getType().equals("zombie_toast_spawner"));
                        if (currEntity instanceof Boulder) {
                            currPosition = new Position(i, j, k + 2);
                        }
                        EntityResponse currResponse = new EntityResponse(currEntity.getId(), currEntity.getType(), currPosition, interactable);
                        entityResponseList.add(currResponse);
                    }

                }
            }
        }
        return entityResponseList;
    }

}
