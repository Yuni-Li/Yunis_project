package dungeonmania.MovingEntities;

import java.util.ArrayList;

import dungeonmania.Entity;
import dungeonmania.GameMap;
import dungeonmania.Inventory;
import dungeonmania.BuildableEntities.Sceptre;
import dungeonmania.StaticEntities.Boulder;
import dungeonmania.StaticEntities.ClosedDoor;
import dungeonmania.StaticEntities.OpenDoor;
import dungeonmania.util.Direction;
import dungeonmania.util.Position;

public class Player extends MovingEntity{

    private int winNo;
    private boolean invincibility;
    private boolean invisibility;
    private boolean oneRing;

    private Inventory inventory;


    /**
     * 
     * @param winNo Number of times the player win a battle
     * @param items List of inventory of the player
     * @param invincibility Check if player is invincible
     * @param invisibility Check if player is invisibility
     * @param wood Amount of wood the player has
     * @param arrow Amount of arrow the player has
     * @param treasure Amount of treasure the player has
     */
    public Player(String id, String type, Position position, GameMap gameMap) {
        super(id, type, position, gameMap);
        this.setHealth(500);
        this.setAttack(20);
        this.winNo = 0;
        this.invincibility= false;
        this.invisibility = false;
        inventory = new Inventory();
    }

    // Getters
    public int getWinNo() {
        return winNo;
    }

    public Inventory getInventory() {
        return inventory;
    }

    public boolean isInvincibility() {
        return invincibility;
    }

    public boolean isInvisibility() {
        return invisibility;
    }

    public boolean isOneRing() {
        return oneRing;
    }


    // Setters
    public void setWinNo(int winNo) {
        this.winNo = winNo;
    }

    public void setInvincibility(boolean invincibility) {
        this.invincibility = invincibility;
    }

    public void setInvisibility(boolean invisibility) {
        this.invisibility = invisibility;
    }

    public void setOneRing(boolean oneRing) {
        this.oneRing = oneRing;
    }


    // Updates
    public void updateWinNo(int winNo) {
        this.winNo += winNo;
    }

    public void updateHp(double health) {
        double currHp = super.getHealth();
        this.setHealth(currHp += health);
    }

    

    /*
    // Check if player has weapon
    public boolean checkWeapon() {
        for (Inventory item: items) {
            if (item.getType().equals("sword") || item.getType().equals("bomb") || item.getType().equals("bow")) {
                    return true;
                }
        }
        return false;
    }
    */

    /*
    // Add a new item in Inventory list
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
            newItem = new Inventory();
            // For key, potion, treasure, bomb, arrow and wood, 
            // amount will be using(setting) as durability, and attack stays initial value 0 with them.
            switch (type) {
                case "treasure":
                    newItem.setDurability(newItem.getDurability() + 1);
                    updateTreasure(1);
                case "key":
                    for (Inventory item: items) {
                        // player can only carry one key
                        if (item.getType().equals("key")) {
                            add = false;
                            break;
                        }
                    }
                    if (add) {
                        newItem.setDurability(1);
                    }
                case "health_potion":
                    newItem.setDurability(newItem.getDurability() + 1);
                case "invincibility_potion":
                    this.setInvincibility(true);
                    newItem.setDurability(newItem.getDurability() + 1);
                case "invisibile_potion":
                    this.setInvisibility(true);
                    newItem.setDurability(newItem.getDurability() + 1);
                case "wood":
                    updateWood(1);
                    newItem.setDurability(newItem.getDurability() + 1);
                case "arrow":
                    updateArrow(1);
                    newItem.setDurability(newItem.getDurability() + 1);
                case "bomb":
                    newItem.setDurability(newItem.getDurability() + 1);
                case "sword":
                    newItem.setAttack(20);
                    newItem.setDurability(newItem.getDurability() + 10);
                case "armour":
                    newItem.setDurability(newItem.getDurability() + 10);
                case "one_ring":
                    this.setOneRing(true);
                    newItem.setDurability(newItem.getDurability() + 1);
                case "bow":
                    newItem.setAttack(50);
                    newItem.setDurability(newItem.getDurability() + 50);
                case "shield":
                    newItem.setDurability(newItem.getDurability() + 50);
            }
        }
        
        // Add if item can be added into inventory
        if (add) {
            items.add(newItem);
        }
    } 

    */

    public void move(Direction direction) {
        if (!obstructed(direction, this.getPosition().translateBy(direction))) {
            Position playerPositionCopy = this.getPosition();
            Position newPlayerPosition = this.getPosition().translateBy(direction);
            this.setPosition(newPlayerPosition);
            this.getGameMap().removeEntity(playerPositionCopy.getX(), playerPositionCopy.getY(), playerPositionCopy.getLayer());
            this.getGameMap().addEntity(this, newPlayerPosition.getX(), newPlayerPosition.getY(), newPlayerPosition.getLayer());
        }
        
    }

    

    private boolean obstructed(Direction direction, Position i){
        Entity entity = this.getGameMap().getEntity(i.getX(), i.getY(), 0);

        if (entity instanceof Boulder) {
            return !((Boulder) entity).move(direction, this.getGameMap());
        } 
        else if (entity instanceof ClosedDoor) {
            if (((ClosedDoor) entity).canOpenDoor(inventory)) {
                this.getGameMap().removeEntity(i.getX(), i.getY(), 0);
                this.getGameMap().addEntity(new OpenDoor(entity.getId(), "doorOpen"), i.getX(), i.getY(), 1);
                return false;
            }
            return true;
        }
        else if (entity == null) {
            //No obstructions
            return false;
        }
        
        return true;
    }

    /*
    public Sceptre getAvailableSceptre(){        
        if(getActiveSceptre() != null){
            return getActiveSceptre();
        }

        else if (getChargedSceptre() != null){
            Sceptre sceptre = getChargedSceptre();
            sceptre.setActive(true);
            return sceptre;
        }

        return null;
    }

    private Sceptre getActiveSceptre(){
        Sceptre activeSceptre = null;
        
        ArrayList<Entity> sceptreList = inventory.getItemList("sceptre");
        for(Entity sceptreEntity : sceptreList){
            Sceptre sceptre = (Sceptre) sceptreEntity;
            if (sceptre.isActive()){
                activeSceptre = sceptre;
            }
        }

        return activeSceptre;
    }
    */
    
    public Sceptre getSceptre(String id){
        Sceptre chargedSceptre = null;

        ArrayList<Entity> sceptreList = inventory.getItemList("sceptre");
        for(Entity sceptreEntity : sceptreList){
            Sceptre sceptre = (Sceptre) sceptreEntity;
            if (sceptre.getTicksLeft() > 0 && sceptre.getId().equals(id)){
                chargedSceptre = sceptre;
            }
        }

        return chargedSceptre;
    }

    public void rechargeAllSceptresExceptFor(String id){

        ArrayList<Entity> sceptreList = inventory.getItemList("sceptre");
        for(Entity sceptreEntity : sceptreList){
            Sceptre sceptre = (Sceptre) sceptreEntity;
            if (sceptre.getTicksLeft() < 10 && sceptre.getId().equals(id)){
                sceptre.rechargeSceptre();
            }
        }
    }
}
