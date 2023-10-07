package dungeonmania;

import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.ArrayList;

import org.junit.jupiter.api.Test;

import dungeonmania.response.models.DungeonResponse;
import dungeonmania.response.models.ItemResponse;
import dungeonmania.util.Direction;

public class NewGameTests {
    
    @Test
    public void advancedTest() {
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse newGameResponse = controller.newGame("advanced", "standard");
        assertFalse(newGameResponse == null); 
        assertFalse(newGameResponse.getEntities() == null);
        ArrayList<ItemResponse> itemList = new ArrayList<ItemResponse>();
        assertTrue(newGameResponse.getInventory().equals(itemList));
        ArrayList<String> buildables = new ArrayList<>();
        assertTrue(newGameResponse.getBuildables().equals(buildables));
        String goals = "(:enemies AND :treasure(1))";
        assertTrue(newGameResponse.getGoals().equals(goals));
    }

    @Test
    public void boulderTest() {
        DungeonManiaController controller = new DungeonManiaController();
        assertFalse((controller.newGame("boulders", "standard") == null)); 
        //Nothing else except a switch can occupy the same cell as a boulder
        

    }

    @Test
    public void mazeTest() {
        DungeonManiaController controller = new DungeonManiaController();
        assertFalse((controller.newGame("maze", "standard") == null)); 
    }

    @Test
    public void saveAndLoadGameTest() {
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse newGameResponse = controller.newGame("advanced", "standard");
        assertFalse(newGameResponse == null); 
        assertFalse(newGameResponse.getEntities() == null);
        assertDoesNotThrow(() -> controller.saveGame("game1"));
        assertDoesNotThrow(() -> controller.loadGame("game1"));
    }

    @Test
    public void failSaveAndLoadGameTest() {
        DungeonManiaController controller = new DungeonManiaController();
        DungeonResponse newGameResponse = controller.newGame("advanced", "standard");
        assertFalse(newGameResponse == null); 
        assertFalse(newGameResponse.getEntities() == null);
        assertDoesNotThrow(() -> controller.saveGame("game1"));
        assertDoesNotThrow(() -> controller.loadGame("game2"));
    }

    //@Test
    //public void tickTest() {
    //    DungeonManiaController controller = new DungeonManiaController();
    //    DungeonResponse newGameResponse = controller.newGame("advanced", "standard");
    //    assertFalse(newGameResponse == null); 
    //    assertFalse(newGameResponse.getEntities() == null);
    //    assertDoesNotThrow(() -> controller.tick("", new Direction(0, 1)));
//
    //}

}
