package dungeonmania.Goals;

import java.util.ArrayList;

import org.json.JSONArray;
import org.json.JSONObject;

public class GoalFactory {
    
    /**
     * makes an and node
     * @param child1
     * @param child2
     * @return
     */
    private static And makeAnd(GoalComponent child1, GoalComponent child2) {
        return new And(child1, child2);
    }
    /**
     * makes an or node
     * @param child1
     * @param child2
     * @return
     */
    private static Or makeOr(GoalComponent child1, GoalComponent child2) {
        return new Or(child1, child2);
    }
    /**
     * makes a boulder leaf and is also given the leafObservers list in order
     * to add the newly created goal to
     * @param switchCount
     * @param leafObservers
     * @return
     */
    private static GoalComponent makeBouldersGoal(int switchCount, ArrayList<GoalLeaf> leafObservers) {
        GoalLeaf goal = new BouldersGoal(switchCount);
        
        leafObservers.add(goal);
        return goal;
    }

    /**
     * makes an enemies leaf and is also given the leafObservers list in order
     * to add the newly created goal to
     * @param switchCount
     * @param leafObservers
     * @return
     */
    private static GoalComponent makeEnemiesGoal(Integer enemyCount, ArrayList<GoalLeaf> leafObservers) {
        GoalLeaf goal = new EnemiesGoal(enemyCount);
        
        leafObservers.add(goal);
        return goal;
    }

    /**
     * makes an exit leaf and is also given the leafObservers list in order
     * to add the newly created goal to
     * @param switchCount
     * @param leafObservers
     * @return
     */
    private static GoalComponent makeExitGoal(ArrayList<GoalLeaf> leafObservers) {
        GoalLeaf goal = new ExitGoal();
        
        leafObservers.add(goal);
        return goal;
    }

    /**
     * makes a treasure leaf and is also given the leafObservers list in order
     * to add the newly created goal to
     * @param switchCount
     * @param leafObservers
     * @return
     */
    private static GoalComponent makeTreasureGoal(int treasureCount, ArrayList<GoalLeaf> leafObservers) {
        GoalLeaf goal = new TreasureGoal(treasureCount);
        
        leafObservers.add(goal);
        return goal;
    }

    /**
     * parses the JSONObject for goals given when reading in dungeon files
     * using the initial conditions found in Goal to instantiate the goals using the makeGoalComponent method.
     * @param jObject
     * @param tc
     * @param sc
     * @param ec
     * @param leafObservers
     * @return
     */
    public static GoalComponent goalParser(JSONObject jObject, int tc, int sc, int ec, ArrayList<GoalLeaf> leafObservers) {
        if (!jObject.has("goal")) return makeDummyGoal();
        return makeGoalComponent(jObject, "goal", tc, sc, ec, leafObservers);
    }
    
    private static GoalLeaf makeDummyGoal() {
        return new DummyGoal();
    }

    /**
     * Recursive method to generate all the goals of a given JSONObject. Returns the head of goals.
     * @param jObject
     * @param key
     * @param treasureCount
     * @param switchCount
     * @param enemyCount
     * @param leafObservers
     * @return
     */
    private static GoalComponent makeGoalComponent(JSONObject jObject, String key, int treasureCount, int switchCount, int enemyCount, ArrayList<GoalLeaf> leafObservers) {

        if (jObject.get(key).equals("enemies")) {
            return makeEnemiesGoal(enemyCount, leafObservers);
        }
        else if (jObject.get(key).equals("boulders")) {
            return makeBouldersGoal(switchCount, leafObservers);
        }
        else if (jObject.get(key).equals("exit")) {
            return makeExitGoal(leafObservers);
        }
        else if (jObject.get(key).equals("treasure")) {
            return makeTreasureGoal(treasureCount, leafObservers);
        }
        else if (jObject.get(key).equals("AND")) {
            JSONArray jArray = jObject.getJSONArray("subgoals");
            return makeAnd(
                makeGoalComponent(jArray.getJSONObject(0), "goal", treasureCount, switchCount, enemyCount, leafObservers), 
                makeGoalComponent(jArray.getJSONObject(1), "goal", treasureCount, switchCount, enemyCount, leafObservers)
            );
        }
        else if (jObject.get(key).equals("OR")) {
            JSONArray jArray = jObject.getJSONArray("subgoals");
            return makeOr(
                makeGoalComponent(jArray.getJSONObject(0), "goal", treasureCount, switchCount, enemyCount, leafObservers), 
                makeGoalComponent(jArray.getJSONObject(1), "goal", treasureCount, switchCount, enemyCount, leafObservers)
                );
        }

        return null;
    }

    

}
