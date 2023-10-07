package dungeonmania.Goals;

public class ExitGoal extends GoalLeaf {
    private boolean onExit;

    /**
     * goal for player to exit. onExit is a boolean, if the player is on the exit it is true.
     */
    ExitGoal() {
        onExit = false;
    }

    @Override
    public String prettyPrint() {
        return ":exit";
    }

    @Override
    public boolean isComplete() {
        return onExit;
    }

    public void setOnExit(boolean onExit) {
        this.onExit = onExit;
    }

}
