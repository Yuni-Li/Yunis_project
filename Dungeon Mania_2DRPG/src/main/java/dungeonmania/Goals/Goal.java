package dungeonmania.Goals;

import java.util.ArrayList;

import org.json.JSONObject;

import dungeonmania.Entity;
import dungeonmania.GameMap;
import dungeonmania.CollectableEntities.Treasure;
import dungeonmania.MovingEntities.MovingEntity;
import dungeonmania.StaticEntities.FloorSwitch;

public class Goal {
    private Integer tc;
    private Integer sc;
    private Integer ec;
    private GoalComponent goalHead;

    /**
     * This class stores the goal head as well as counters used for initialisation upon
     * generating the composite pattern.
     * A container for all things goal related.
     * @param goalCondition
     * @param gameMap
     * @param leafObservers
     */
    public Goal(JSONObject goalCondition, GameMap gameMap, ArrayList<GoalLeaf> leafObservers) {
        initialGoalCounters(gameMap);
        goalHead = GoalFactory.goalParser(goalCondition, tc, sc, ec, leafObservers);
    }

    /**
     * initialises the counters for making the goals in GoalFactory.
     * @param gameMap
     */
    private void initialGoalCounters(GameMap gameMap) {
        int tcTemp = 0;
        int scTemp = 0;
        int ecTemp = 0;
        
        for (int i = 0; i < gameMap.getWidth(); i++) {
            for (int j = 0; j < gameMap.getLength(); j++) {
                if (gameMap.getEntity(i, j, 3) instanceof Treasure) {
                    tcTemp++;
                }
                if (gameMap.getEntity(i, j, 1) instanceof FloorSwitch) {
                    if (!((FloorSwitch) gameMap.getEntity(i, j, 1)).isActive()) {
                        scTemp++;
                    }
                }
                //placeholder code.
                for (int k = 11; k <= 55; k++) {
                    if (gameMap.getEntity(i, j, k) instanceof MovingEntity) {
                        ecTemp++;
                    }
                }
            }
        }
        ec = ecTemp;
        sc = scTemp;
        tc = tcTemp;
    }

    public String getGoalString() {
        if (goalHead.isComplete()) return "";
        return goalHead.prettyPrint();
    }


}
