package dungeonmania;

import dungeonmania.response.models.*;
import dungeonmania.util.*;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.ArrayList;

public class ControllerTests {
    // some simple tests (subject to change depending on further implementation)
    @Test
    public void simpleNewGame() {
        DungeonManiaController controller = new DungeonManiaController();
        List<EntityResponse> entities = new ArrayList<>();

        entities.add(new EntityResponse("entity-1", "wall", new Position(0, 0, 2), false));
        entities.add(new EntityResponse("entity-2", "wall", new Position(1, 0, 2), false));
        entities.add(new EntityResponse("entity-player", "player", new Position(1, 1, 2), false));
        entities.add(new EntityResponse("entity-sword", "sword", new Position(6, 1, 2), true));
        entities.add(new EntityResponse("entity-bomb", "bomb", new Position(13, 4, 2), true));
        entities.add(new EntityResponse("entity-mercenary", "mercenary", new Position(3, 5, 2), false));
        entities.add(new EntityResponse("entity-treasure", "treasure", new Position(7, 10, 2), true));
        entities.add(new EntityResponse("entity-invincibility_potion", "invincibility_potion", new Position(11, 10, 2), true));

        assertTrue(new DungeonResponse("some-random-id", "testDungeon.json", entities, new ArrayList<>(), new ArrayList<>(), ":enemies AND :treasure") == controller.newGame("testDungeon.json", "Standard"));
    }

    @Test
    public void simpleNewGameTwo() {
        DungeonManiaController controller = new DungeonManiaController();
        List<EntityResponse> entities = new ArrayList<>();

        entities.add(new EntityResponse("entity-1", "wall", new Position(2, 0, 2), false));
        entities.add(new EntityResponse("entity-2", "wall", new Position(3, 0, 2), false));
        entities.add(new EntityResponse("entity-3", "switch", new Position(1, 2, 2), false));
        entities.add(new EntityResponse("entity-4", "switch", new Position(5, 3, 2), false));
        entities.add(new EntityResponse("entity-player", "player", new Position(2, 2, 2), false));
        entities.add(new EntityResponse("entity-5", "boulder", new Position(3, 2, 2), false));
        entities.add(new EntityResponse("entity-6", "boulder", new Position(4, 3, 2), false));

        assertTrue(new DungeonResponse("some-random-id", "testDungeonTwo.json", entities, new ArrayList<>(), new ArrayList<>(), ":boulders") == controller.newGame("testDungeonTwo.json", "Standard"));
    }
}
