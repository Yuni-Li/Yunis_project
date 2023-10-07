package dungeonmania.Goals;


public class EnemiesGoal extends GoalLeaf {
    private Integer enemyCount;

    /**
     * Constructor for enemiesGoal
     * @param enemyCount - number of active enemies
     */
    EnemiesGoal(Integer enemyCount) {
        this.enemyCount = enemyCount;
    }

    @Override
    public String prettyPrint() {
        return ":spider(" + enemyCount.toString() + ")";
    }

    @Override
    public boolean isComplete() {
        if (enemyCount <= 0) return true;
        else return false;
    }

    public void incrementEnemyCount() {
        enemyCount++;
    }

    public void decrementEnemyCount() {
        enemyCount--;
    }
}
