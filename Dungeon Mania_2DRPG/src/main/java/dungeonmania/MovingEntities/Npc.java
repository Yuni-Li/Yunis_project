package dungeonmania.MovingEntities;

import dungeonmania.Entity;
import dungeonmania.GameMap;
import dungeonmania.util.Position;

public abstract class Npc extends MovingEntity{
    private boolean enemy;
    private int wait = 0;

    public Npc(String id, String type, Position position, GameMap gameMap) {
        super(id, type, position, gameMap);
        this.enemy = true;
        wait = 0;
    }

    public abstract void move();

    public void tryMove(){
        if(wait == 0){ 
            move();
            GameMap gameMap = this.getGameMap();
            
            Entity swamp = gameMap.getEntity(this.getPosition().getX(), this.getPosition().getY(), 1);
            if(swamp != null){
                if(swamp.getType().equals("swamp_tile")){
                    incrementWait();
                }
            }

        }

        else {
            decrementWait();
        }
    }
    private void decrementWait(){
        this.wait = this.wait - 1;
    }

    private void incrementWait(){
        this.wait = this.wait + 1;
    }

    public boolean isEnemy() {
        return enemy;
    }

    public void setEnemy(boolean enemy) {
        this.enemy = enemy;
    }

    public int getWait() {
        return wait;
    }

    public void setWait(int wait) {
        this.wait = wait;
    }    
   
}
