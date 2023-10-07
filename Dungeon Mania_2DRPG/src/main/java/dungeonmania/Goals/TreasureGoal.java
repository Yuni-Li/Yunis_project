package dungeonmania.Goals;

public class TreasureGoal extends GoalLeaf {
    private Integer treasureCount;
    
    /**
     * as players pick up treasure this goal is reduced. 
     * A negative means the player has picked up more treasure than required.
     * @param treasureCount
     */
    TreasureGoal(int treasureCount) {
        this.treasureCount = treasureCount;
    }

    @Override
    public String prettyPrint() {
        return ":treasure(" + treasureCount.toString() + ")";
    }

    public void updateTreasureCount(int treasureCount) {
        this.treasureCount = treasureCount;
    }

    public boolean isComplete() {
        if (treasureCount <= 0) return true;
        return false;
    }

    public void decrementTreasure() {
        if (treasureCount == 0) return;
        treasureCount--;
    }

}
