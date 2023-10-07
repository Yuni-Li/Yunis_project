package dungeonmania;

import dungeonmania.MovingEntities.MovingEntity;
import dungeonmania.MovingEntities.Player;

public class Battle {

    private double playerDamage;
    private double playerHp;
    private double enemyDamage;
    private double enemyHp;
    private Inventory playerItems;
    private Inventory enemyItems;
    private Player player;
    private MovingEntity enemy;

    /**
     * 
     * @param playerDamage Attack ability of the player
     * @param playerHp Player's health
     * @param enemyDamege Attack ability of the damage
     * @param enemyHp Enemy's health
     * @param playerItems Inventory of the player
     * @param enemyItems Invenrtory of the enemy
     */
    public Battle(Player player, MovingEntity enemy) {
        this.enemy = enemy;
        this.player = player;
        this.enemyDamage = enemy.getAttack();
        this.playerDamage = player.getAttack();
        this.playerHp = player.getHealth();
        this.enemyHp = enemy.getHealth();
        //this.playerItems = new Inventory(player.getId(), player.getType());
        //this.enemyItems = new Inventory(enemy.getId(), enemy.getType());

        if (!enemy.isEnemy()) {
            return;
        }

        int attackNo = 0;
        while(playerHp > 0 && enemyHp > 0) {
            if (playerItems.getType().contains("bow")) {  
                // If player has a Bow, attack twice within one round
                for (attackNo = 0; attackNo <= 3; attackNo++) {
                    // Calculus the damage in each round
                    damageCalc(enemyDamage, playerDamage);
                    if (attackNo < 3) {
                        enemyHp -= playerDamage;
                        
                    } else {
                        playerHp -= enemyDamage;
                    }
                } 
            } else {
                // If it is even number -> player's round
                // If odd -> enemy's round
                // Calculus the damage in each round
                damageCalc(enemyDamage, playerDamage);
                if (attackNo % 2 == 0) {
                    enemyHp -= playerDamage;
                } else {
                    playerHp -= enemyDamage;
                }
                attackNo++;
            }
            
            // If player's health <= 0 before the enemy, 
            // Check if player has the oneRing and use it directly
            if (player.isOneRing()){
                player.setHealth(500);
            }
        }

        player.setHealth(playerHp);
        enemy.setHealth(enemyHp);
        
    }

    public void damageCalc(double enemyDamage, double playerDamage) {
        // If player has a sheild/armour, half enemy's damage
        // If enemy has an armour, half player's damage
        if (enemyItems != null && enemyItems.getType() != null) {
            if (enemyItems.getType().contains("armour")) {
                if (enemyItems.getDurability() > 0) {
                    // If the enemy has an armour, it can defense 30% of the player's attack
                    enemyDamage = (playerHp * 0.7 * player.getAttack()) / 5;
                    enemyItems.setDurability(enemyItems.getDurability() - 1);
                } else {
                    enemyDamage = (playerHp * player.getAttack()) / 5;

                }
            }
        } else {
            enemyDamage = (playerHp * playerDamage) / 5;
        }

        if (playerItems != null && enemyItems.getType() != null) {
            if (playerItems.getType().contains("armour")) {
                if (playerItems.getDurability() > 0) {
                    // If player has an armour, it can defense 30% of the enemy's attack
                    playerDamage = (enemyHp * 0.7 * enemy.getAttack()) / 10;
                    playerItems.setDurability(playerItems.getDurability() - 1);
                } else {
                    playerDamage = (enemyHp  * enemy.getAttack()) / 10;
                }
            } else if (playerItems.getType().contains("shield")) {
                if (playerItems.getDurability() > 0) {
                    // If player has an armour, it can defense 50% of the enemy's attack
                    playerDamage = (enemyHp * 0.5 * enemy.getAttack()) / 10;
                    playerItems.setDurability(playerItems.getDurability() - 1);
                } else {
                    playerDamage = (enemyHp  * enemy.getAttack()) / 10;

                }
            } else if (playerItems.getType().contains("sword")) {
                if (playerItems.getDurability() > 0) {
                    // If player has an sword, it can doubles the player's damage
                    playerDamage = (enemyHp * 2.0 * enemy.getAttack()) / 10;
                    playerItems.setDurability(playerItems.getDurability() - 1);
                } else {
                    playerDamage = (enemyHp  * enemy.getAttack()) / 10;

                }
            }
        } else {
            playerDamage = (enemyHp * enemyDamage) / 10;
        }
    }
}

