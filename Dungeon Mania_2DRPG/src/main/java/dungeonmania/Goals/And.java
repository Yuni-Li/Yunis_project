package dungeonmania.Goals;

public class And extends GoalNode {

    /**
     * constructor for And node. Logical and for child 1 and child 2
     * which can either be nodes or leaves.
     * @param child1
     * @param child2
     */
    public And(GoalComponent child1, GoalComponent child2) {
        super(child1, child2);
    }

    @Override
    public String prettyPrint() {
        return ("(" + child1.prettyPrint() + " AND " + child2.prettyPrint() + ")");
    }

    public boolean isComplete() {
        return child1.isComplete() && child2.isComplete();
    }
    
    public GoalLeaf getLeaves() {
        return null;
    }

}
