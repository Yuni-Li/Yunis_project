package dungeonmania.BuildableEntities;

public class Sceptre extends BuildableEntity {
    int ticksLeft;
    boolean active;
    
    public Sceptre(String id, String type) {
        super(id, type, 25);
        ticksLeft = 10;
        active = false;
    }

    public void rechargeSceptre(){
        //Can only recharge to a max of 10 uses
        if(ticksLeft < 10) {
            ticksLeft += 1;
        }
    }
    public void dischargingSceptre(){
        if(ticksLeft > 0){
            ticksLeft -= 1;
        }
        
        else {
            this.active = false;
        }
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public int getTicksLeft() {
        return ticksLeft;
    }    
}
