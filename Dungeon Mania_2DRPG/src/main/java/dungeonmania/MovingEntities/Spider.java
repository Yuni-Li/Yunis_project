package dungeonmania.MovingEntities;
import java.util.ArrayList;

import dungeonmania.GameMap;
import dungeonmania.util.Position;

public class Spider extends Npc{
    private Position centre = null;
    private ArrayList<Position> spiderSquarePath = null;
    private boolean reversing;

    public Spider(String id, String type, Position position, GameMap gameMap){
        super(id, type, position, gameMap);    //Spawns immediately into centre of the circle
        this.setHealth(100);
        this.setAttack(10);

        // moves up if possible
        //Position newPos = moveBy(position, 0, -1);
        //this.setPosition(newPos);

        //this.startPosition = newPos;
        this.centre = position;
        this.reversing = false;
         
        spiderSquarePath = new ArrayList<>();
        createSquarePath();
    }

    /**
     * Move method makes spider move in a clockwise direction on a square path
     */
    public void move(){
        int currPosIndex = spiderSquarePath.indexOf(this.getPosition());
        int newPosIndex;
        Position newPos = null;
        
        newPosIndex = (currPosIndex + 1)%8;
        newPos = spiderSquarePath.get(newPosIndex);

        if(!reversing) {
            // Continuing in clockwise direction
            this.setPosition(newPos); 
        }
        
        else {
            // Going anticlockwise
            newPosIndex = (currPosIndex - 1) < 0 ? 7:(currPosIndex - 1);
            newPos = spiderSquarePath.get(newPosIndex);
            this.setPosition(newPos);
        }  
    }

    /**
     * Creates a square path around a centre point 
     */
    private void createSquarePath(){
        this.spiderSquarePath.add(this.centre.translateBy(0, -1));
        this.spiderSquarePath.add(this.centre.translateBy(1, -1));
        this.spiderSquarePath.add(this.centre.translateBy(1, 0));
        this.spiderSquarePath.add(this.centre.translateBy(1, 1));
        this.spiderSquarePath.add(this.centre.translateBy(0, 1));
        this.spiderSquarePath.add(this.centre.translateBy(-1, 1));
        this.spiderSquarePath.add(this.centre.translateBy(-1, 0));
        this.spiderSquarePath.add(this.centre.translateBy(-1, -1));
        
        // 7    0   1
        // 6        2
        // 5    4   3

        // 7    0
        // 6     
        // 5    4

    }
}
