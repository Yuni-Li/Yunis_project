# Project 21T3

[Link to specification](https://gitlab.cse.unsw.edu.au/COMP2511/21T3/project-specification)


# Project Assumtions

## Battle.java
1. At the beginning, check if 'Enemy' is hostile, if not, battle will not happen.
2. Need to check whether the player has armor or sheild. Armour and sheild will resist(decrease) some of the enemy's damge. Each time of defense will decrease the durability  by 1. 
    {armour: decrease 30%, sheild: decrease 50%(Since its hard to get)}
3. Zombie toast and mercenary might also has an armour(but not sheild). So enemy's armor can also resist 30% of play's damage. And  each time of defense will decrease the durability  by 1. 
4. If player win a battle with an armoured enemy, they have a chance to get their armor.
5. If player has a bow, it can attack the enemy twice within one round. And each time of attack will decrease the durability of the bow by 1.
6. If the durability of player's current weapon/defense is 0, equip the next weapon(if have), and update the player's/enemy's damage.
7. Players fight within the mercenary battle radius, mercenary's speed x2
    If the mercenary is an ally, it will assist the player in this battle within the radius, and attacking twice in one round
8. Check if player has the one ring if the player dies first(health is 0, and enemy's health is not 0). If so, use it and respawns with full health.
    The one ring: Each time a character wins a battle, there is a 0.8% chance of getting a "rare item". If the ring doesnot appear within 100 times of win, the player will definitely get it for the 100th win.
9. Each round needs to check the player's/enemy's damage, and health.
10. Player's health <= 0 first and don't have the one ring, enemy win and game over
    Enemy's health <=0 first, player win and remove this enemy

## Character.java:
1. Initialze: set health to 500 and attack 20
2. Cannot move:
    1. wall
    2. bouder and cannot be pushed into next square
    3. door and no corresponding key to open it
    4. zombie toast spawner
3. Update the position of the player by add current position with direction
4. Player has an inventory which includes all the collected items

## Inventory.java
1. Use an arraylist to store the id, type and all the info of collected items.
2. Initialize: id, type 
               attack/durability 0 because not every item has attack and durability attributes
3. For key, potion, treasure, bomb, arrow and wood, amount will be using(setting) as durability, and attack stays 0 with them.

## interact() in DungeonManiaController
1. Check if entityid exist
2. IllegalArgumentException if entityid doesn't exist
3. InvalidActionException if :
    1. Player is not cardinally adjacent to the given entity
    2. Player does not have any gold and attempts to bribe a mercenary
    3. Player does not have a weapon and attempts to destroy a spawner
    4. Player is not cardinally adjacent to the spawner and are destroying a spawner

## build() in DungeonManiaController
1. IllegalArgumentException if buildable is not a bow/sheild
2. InvalidActionException if the player does not have enough material to build a bow/sheild

## Tick in DungeonManiaController
1. IllegalArgumentException: throw if itemused is not in inventory
   InvalidActionException: throw if itemused is not a bomb, potion or is null
2. Update the position of player and other movingentities.
3. After position update, check if new position contains:
    1. Layer0:
        1. wall: stay
        2. boulder: push or stay if the boulder cannot be pushed
        3. door: open and move if the door is open and has corresponding key, and the door is open
                 stay if the door is closed and don't have corresponding key
    2. Layer1:
        1. switch: swith floor if it is untriggered, and move to the square if it is triggered.
        2. portal: teleports entities to a corresponding portal.
        3. exit: puzzle complete
    3. Layer2:
        1. zombie toast spawner: player can destroy it if player has weapon and are cardinally adjacent to it
    4. Layer3:
        1. treasure: can be collected by the player
        2. key: can be collected by the player and can carray only one key
        3. health_potion: can be collected by the player and can be used anytime, player will immediately regenerate to full health after use it.
        4. invincibility_potion:
        5. invisibility_potion:
        6. wood:
        7. arrow:
        8. bomb:
        9. sword:
        10. armour:
        11. one_ring:
    5. Layer5: zombie toast: battle
    6. Layer10: mercenary: bribe or battle
    7. Layer15: spider: battle
    8. Layer20: player: 


## Milestone 3
- Mercenary/assassin allies can't occupy the same cell as the player
- Sun stone is never consumed when used to build. It will take priority over treasure
- When building an item that requires treasure or keys, treasure takes priority over keys
- Sun stone goes towards treasure goal

- New Layers:
    - Layer 0: wall, door, boulder
    - Layer 1: switch, portal, exit, swamp_tile
    - Layer 2: zombie toast spawners
    - Layer 3: treasure, key, health potions, invincibility potions, invisibility potions, wood, arrow, bomb, sword, armour, one_ring
    - Layer 11-15: Spiders
    - Layer 16-35: Mercenaries
    - Layer 36-55: Zombie toasts
    - Layer 56-60: Assassins
    - Layer 61-65: Hydras
    - Layer 100: Player

