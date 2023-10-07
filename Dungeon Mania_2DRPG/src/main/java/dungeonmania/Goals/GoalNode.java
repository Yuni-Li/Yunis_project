package dungeonmania.Goals;

public abstract class GoalNode implements GoalComponent {

    protected GoalComponent child1 = null;
    protected GoalComponent child2 = null;

    /**
     * goalNode is either logical and or logical or for 2 leaf/node children.
     */
    GoalNode(GoalComponent child1, GoalComponent child2) {
        this.child1 = child1;
        this.child2 = child2;
    }


    public void addChild(GoalComponent child) {
        if (child1 == null) {
            child1 = child;
        } else child2 = child;
    }

    public void removeChild() {
        if (child2 != null) {
            child2 = null;
        } else child1 = null;
    }

    public GoalComponent getChild1() {
        return child1;
    }

    public GoalComponent getChild2() {
        return child2;
    }

}
