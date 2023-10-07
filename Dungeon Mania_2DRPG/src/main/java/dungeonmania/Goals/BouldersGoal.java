package dungeonmania.Goals;

public class BouldersGoal extends GoalLeaf {
    private Integer switchCount;
    
    /**
     * BouldersGoal constructor.
     * This goal isn't strictly a boulder goal but rather a goal for boulders being on all switches.
     * @param switchCount
     */
    BouldersGoal(int switchCount) {
        this.switchCount = switchCount;
    }

    public String prettyPrint() {
        return ":boulders(" + switchCount.toString() + ")" ;
    }

    public void updateSwitchCount(int switchCount) {
        this.switchCount = switchCount;
    }

    public int getSwitchCount() {
        return switchCount;
    }

    public boolean isComplete() {
        if (switchCount <= 0) return true;
        return false;
    }

    public void incrementSwitches() {
        switchCount++;
    }

    public void decrementSwitches() {
        if (switchCount == 0) return;
        switchCount--;
    }

}
