package dungeonmania.CollectableEntities;

import dungeonmania.Entity;
import dungeonmania.MovingEntities.Player;

public class TheOneRing extends Entity {

    /**
     * constructor for TheOneRing
     * @param id unique id
     * @param type the type of Entity the object is (e.g. Sword, Boulder etc.)
     */
    public TheOneRing(String id, String type) {
        super(id, type);
    }

    // Winning a respawn ring
    public void winRing(int winNo, Player player, String id) {
        // The one ring: Each time a character wins a battle, there is a 0.8% chance of getting a "rare item". 
        // If the ring doesnot appear within 100 times of win, the player will definitely get it for the 100th win.
        if (getResultRandom(1, 1000, 8) || (player.getWinNo() == 100 && !player.isOneRing())) {
            // Add this ring and reset winNo
            //player.addItem(id, "one ring");
            player.setWinNo(0);
        } 
    }

    public int getRandom(int max, int min) {
        // final int max = 1000;
        // final int min = 1;
        int random = (int)Math.floor(Math.random() * (max - min + 1) + min);
        return random;
    }

    // Get a random number from 1 to 1000, the probability is 8/1000 = 0.8%
    public boolean getResultRandom(int min, int max, int probability){
        int random = this.getRandom(min, max);
        if (probability < random) {
            return true;
        }
        return false;
    }
}
