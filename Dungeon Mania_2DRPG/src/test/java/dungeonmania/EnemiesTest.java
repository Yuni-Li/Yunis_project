package dungeonmania;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.Test;

import dungeonmania.response.models.DungeonResponse;
import dungeonmania.response.models.EntityResponse;
import dungeonmania.util.Direction;
public class EnemiesTest {
    /**
     * Things to test:
     *      - Merc path finding and battle
     *      - remove dead mercenary from map
     *      - test bribes
     *             - mercenary
     *             - assassin
     *      - check isInteractble for all the enemies
     */

    @Test
    public void mercBattleAndPathFinding() {
        // mercenary should find player and battle with player 
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse response = controller.newGame("mercTest", "standard");

        //Player stand still for 200 ticks. Spawned enemies (mercenaries and assassins in particular) 
        //should be able to track the player and kill it
        
        for(int i = 0; i < 200; i++){
            response = controller.tick(null, Direction.RIGHT);
        }
        
        List<EntityResponse> entityResponses = response.getEntities();

        boolean foundPlayer = false;
        for (EntityResponse entityRes : entityResponses){
            String type = entityRes.getType();
            if (type.equals("player")){
                foundPlayer = true;
            }
        }

        assertTrue(!foundPlayer);
    }

    @Test
    public void deadMercRemoved() {
        // First mercenary should be dead and removed from the map
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse response = controller.newGame("mercTest", "standard");

        //Player stand still for 100 ticks. Spawned enemies (mercenaries and assassins in particular) 
        //should be able to track the player and kill it
        for(int i = 0; i < 100; i++){
            response = controller.tick("", Direction.NONE);
        }
        
        List<EntityResponse> entityResponses = response.getEntities();

        boolean foundEntityMerc = false;
        for (EntityResponse entityRes : entityResponses){
            String id = entityRes.getId();
            if (id.equals("entity-mercenary")){
                foundEntityMerc = true;
            }
        }

        assertTrue(!foundEntityMerc);
    }

    @Test
    public void bribeMerc() {
        // Tests if bribe works
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse response = controller.newGame("mercTest", "standard");
        
        String mercToBribe = "";
        List<EntityResponse> entityResponses = response.getEntities();
        for (EntityResponse entityRes : entityResponses){
            String type = entityRes.getType();
            if (type.equals("mercenary")){
                mercToBribe = entityRes.getId();
            }
        }

        response = controller.tick("", Direction.RIGHT);    //Player picking up treasure
        response = controller.tick(mercToBribe, Direction.NONE);    //Player bribing mercenary

        //Player stand still for 300 ticks. Newly spawned enemies will eventually kill the player.
        // Mercenary ally is invinvible, so will still be on map 
        for(int i = 0; i < 100; i++){
            response = controller.tick("", Direction.NONE);
        }
        

        boolean foundPlayer = false;
        for (EntityResponse entityRes : entityResponses){
            String type = entityRes.getType();
            if (type.equals("player")){
                foundPlayer = true;
            }
        }
        assertTrue(!foundPlayer);

        boolean foundEntityMerc = false;
        for (EntityResponse entityRes : entityResponses){
            String id = entityRes.getId();
            if (id.equals(mercToBribe)){
                foundEntityMerc = true;
            }
        }
        assertTrue(foundEntityMerc);
    }

    @Test
    public void bribeAssassin() {
        // Tests if bribe works
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse response = controller.newGame("assassinTest", "standard");
        
        String assassinToBribe = "";
        List<EntityResponse> entityResponses = response.getEntities();
        for (EntityResponse entityRes : entityResponses){
            String type = entityRes.getType();
            if (type.equals("assassin")){
                assassinToBribe = entityRes.getId();
            }
        }

        response = controller.tick("", Direction.RIGHT);    //Player picking up treasure
        response = controller.tick("", Direction.RIGHT);    //Player picking up one ring
        response = controller.tick(assassinToBribe, Direction.NONE);    //Player bribing assassin

        //Player stand still for 300 ticks. Newly spawned enemies will eventually kill the player.
        // assassin ally is invinvible, so will still be on map 
        for(int i = 0; i < 100; i++){
            response = controller.tick("", Direction.NONE);
        }
        

        boolean foundPlayer = false;
        for (EntityResponse entityRes : entityResponses){
            String type = entityRes.getType();
            if (type.equals("player")){
                foundPlayer = true;
            }
        }
        assertTrue(!foundPlayer);

        boolean foundEntityAssassin = false;
        for (EntityResponse entityRes : entityResponses){
            String id = entityRes.getId();
            if (id.equals(assassinToBribe)){
                foundEntityAssassin = true;
            }
        }
        assertTrue(foundEntityAssassin);
    }

    @Test
    public void checkIsInteractive() {
        // Tests if bribe works
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse response = controller.newGame("allEnemies", "standard");
        
        List<EntityResponse> entityResponses = response.getEntities();
        for (EntityResponse entityRes : entityResponses){
            String type = entityRes.getType();
            // Only mercenaries and assassins can be interacted with
            if(type.equals("zombie_toast")){
                assertTrue(!entityRes.isInteractable());
            }
            else if(type.equals("hydra")){
                assertTrue(!entityRes.isInteractable());
            }
            else if(type.equals("mercenary")){
                assertTrue(entityRes.isInteractable());
            }
            else if(type.equals("assassin")){
                assertTrue(entityRes.isInteractable());
            }
            else if(type.equals("spider")){
                assertTrue(!entityRes.isInteractable());
            }
        }
    }
}
