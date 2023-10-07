package dungeonmania.MovingEntities;
import dungeonmania.util.Position;
import dungeonmania.GameMap;

public class ZombieToast extends Npc{
    
    public ZombieToast(String id, String type, Position position, GameMap gameMap){
        super(id, type, position, gameMap);
        this.setHealth(100);
        this.setAttack(5);;
    }
    
    /**
     * Move method allows ZombieToast to move randomly around the map.
     * This method will continously call the "doMove" method until there is no obstruction or when its
     * looped a max of 4 times
     */
    public void move(){
        GameMap gameMap = getGameMap();

        int loopCounter = 0;       
        while (doMove(gameMap) == false && loopCounter < 4) {  //Keeps moving randomly. If ZombieToast is boxed in (i.e false for all 8 moves)
            doMove(gameMap);                                   // Then position doesn't get updated
            loopCounter += 1;
        }
    }

    /**
     * Sets the position of the zombie if the randomly generated direction leads to an empty cell
     * @param gameMap
     * @return  returns true if the position was successfully set or false if the move leads to an obstruction
     */
    private boolean doMove(GameMap gameMap){
        Position newPosition = this.getPosition().translateBy(randomDirection(), randomDirection());
        int newX = newPosition.getX();
        int newY = newPosition.getY();
        
        if(newX >= 0 && newX <= gameMap.getWidth() && newY >= 0 && newY <= gameMap.getLength()){
            if (gameMap.getEntity(newX, newY, 0) == null){   //No items in layer 0 (Wall, boulder and doors)
                this.setPosition(newPosition);
                return true;
            }
        }
        return false;
    }

    /**
     * Provides a random direction in 1 dimesnion: -1, 0 ,1
     * @return
     */
    private int randomDirection(){
        int min = -1;
        int max = 1;
          
        //Generate random int value from -1 to 1
        int random_int = (int)Math.floor(Math.random()*(max-min+1)+min);
        return random_int;
    }

    /*
    public void addItem(String id, String type) {
        Inventory newItem = null;
        boolean exist = false;
        for (Inventory item: this.items) {
            if (item.getId().equals(id)) {
                exist = true;
            }
        }

        boolean add = true;
        if (!exist) {
            newItem = new Inventory(id, type);
            switch (type) {
                case "sword":
                    newItem.setAttack(20);
                    newItem.setDurability(newItem.getDurability() + 10);
                case "armour":
                    newItem.setDurability(newItem.getDurability() + 10);
                case "shield":
                    newItem.setDurability(newItem.getDurability() + 50);
            }
        }
        
        if (add) {
            items.add(newItem);
        }
    } 

    public void removeItem(String itemId) {
        for (Inventory item: items) {
            if (item.getId().equals(itemId)) {
                this.items.remove(item);
            }
        }
    }
    */
}
