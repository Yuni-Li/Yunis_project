package dungeonmania.Goals;

/**
 * this class is used for when no goals are specified.
 */
public class DummyGoal extends GoalLeaf {

    @Override
    public String prettyPrint() {
        return "";
    }

    @Override
    public boolean isComplete() {
        return false;
    }
    
}
