package dungeonmania.Goals;

public class Or extends GoalNode {

    /**
     * logical or for child1 and child2 goal evaluations.
     * @param child1
     * @param child2
     */
    Or(GoalComponent child1, GoalComponent child2) {
        super(child1, child2);
    }

    @Override
    public String prettyPrint() {
        return ("(" + child1.prettyPrint() + " OR " + child2.prettyPrint() + ")");
    }

    public boolean isComplete() {
        return child1.isComplete() || child2.isComplete();
    }
    
}
