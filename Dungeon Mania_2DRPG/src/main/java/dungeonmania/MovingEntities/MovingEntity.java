package dungeonmania.MovingEntities;

import dungeonmania.Entity;
import dungeonmania.util.Position;
import dungeonmania.GameMap;

public abstract class MovingEntity extends Entity {
    private GameMap gameMap;
    private double health;
    private int attack;
    private Position position;
    

    public MovingEntity(String id, String type, Position position, GameMap gameMap){
        super(id, type);
        this.gameMap = gameMap;
        this.position = position;
        
        this.health = 100;
    }

    public GameMap getGameMap(){
        return gameMap;
    }
    
    public double getHealth() {
        return this.health;
    }

    public void setHealth(double health) {
        this.health = health;
    }

    public void loseHealth(double lostHealth){
        this.health -= lostHealth;
    }
    
    public int getAttack() {
        return attack;
    }

    public void setAttack(int attack) {
        this.attack = attack;
    }

    public Position getPosition() {
        return position;
    }

    public void setPosition(Position position) {
        this.position = position;
    }


    
    
}
