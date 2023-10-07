package dungeonmania.MovingEntities;

import dungeonmania.GameMap;
import dungeonmania.util.Position;

public class Hydra extends ZombieToast{

    public Hydra(String id, String type, Position position, GameMap gameMap) {
        super(id, type, position, gameMap);
        this.setHealth(400);
        this.setAttack(20);
    }
    
    /**
     * This method is called when the Hydra is attacked by the player. There is a 50% chance the player's attack 
     * damage will actually be added to the hydra's own health due to regeneration
     * @param damageReceived amount of damage dealt by the player
     */
    @Override
    public void loseHealth(double damageReceived){
        int min = 0;    //Lose health 
        int max = 1;    //Increase health
        int random_int = (int)Math.floor(Math.random()*(max-min+1)+min);

        if(random_int == 0) {
            this.setHealth(this.getHealth() - damageReceived);
        }

        else{
            this.setHealth(this.getHealth() + damageReceived);
        }
    }
}
