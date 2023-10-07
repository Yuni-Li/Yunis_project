package dungeonmania;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import dungeonmania.BuildableEntities.Bow;
import dungeonmania.BuildableEntities.MidnightArmour;
import dungeonmania.BuildableEntities.Sceptre;
import dungeonmania.BuildableEntities.Shield;
import dungeonmania.CollectableEntities.Treasure;
import dungeonmania.CollectableEntities.Key;
import dungeonmania.response.models.ItemResponse;


public class Inventory{

    private HashMap<String, ArrayList<Entity>> items;

    public Inventory() {
        this.items = new HashMap<String, ArrayList<Entity>>();
    }

    /**
     * returns a list of items of the given type.
     * @param itemType
     * @return itemList
     */
    public ArrayList<Entity> getItemList(String itemType) {
        if (items.containsKey("itemType")) return items.get(itemType);
        return new ArrayList<Entity>();
    }

    public boolean hasKey(Integer keyPairId) {
        if (items.containsKey("key")) {
            ArrayList<Entity> KeyList = items.get("key");
            for (Entity key : KeyList) {
                if (((Key) key).getKeyPairId() == keyPairId) {
                    removeItem(key.getId());
                    return true;
                }
            }
        } 
        else if (items.containsKey("sun_stone")) return true;
        return false;
    }

    /**
     * adds an item to the inventory.
     * @param item
     */
    public void addItem(Entity item) {
        String itemType = item.getType();

        if (!items.containsKey(itemType)) 
        {
            ArrayList<Entity> newItemList = new ArrayList<>();
            newItemList.add(item);
            items.put(itemType, newItemList);
        }
        else 
        {
            items.get(itemType).add(item);
        }
    }
    
    /**
     * Takes in a type string e.g. "Treasure" and returns the number of this item
     * contained within the inventory.
     * @param type
     * @return number of items in the inventory
     */
    public int numberOfItem(String type) {
        for (ArrayList<Entity> i : items.values()) {
            if ( !i.isEmpty() && i.get(0).getType().equals(type) ) {
                return i.size();
            }
        }
        return 0;
    }

    /**
     * removes the item specified by id from the inventory.
     * @param id
     */
    public void removeItem(String id) {
        for (ArrayList<Entity> entityList : items.values()) {
            for (Entity item : entityList) {
                if (item.getId().equals(id)) {
                    entityList.remove(item);
                    return;
                }
            }
        }
    }

    /**
     * helper method to remove the first item encountered of a given type
     * @param itemType
     */
    private void removeItemByType(String itemType) {
        for (ArrayList<Entity> entityList : items.values()) {
            for (Entity item : entityList) {
                if (item.getType().equals(itemType)) {
                    entityList.remove(item);
                    return;
                }
            }
        }
    }

    /**
     * helper method that calls removeItemByType
     * @param itemType
     * @param numberToRemove
     */
    private void removeMultipleItemsByType(String itemType, int numberToRemove) {
        for (int i = 0; i < numberToRemove; i++) {
            removeItemByType(itemType);
        }
    }

    /**
     * returns the list of currently buildable items
     * @return list of buildables
     */
    public List<String> getBuildables(boolean hasZombies) {
        List<String> buildables = new ArrayList<String>();

        if (canBuild("bow", hasZombies)) {
            buildables.add("bow");
        }
        if (canBuild("shield", hasZombies)) {
            buildables.add("shield");
        }
        if (canBuild("sceptre", hasZombies)) {
            buildables.add("sceptre");
        }
        if (canBuild("midnight_armour", hasZombies)) {
            buildables.add("midnight_armour");
        }

        return buildables;
    }

    /**
     * checks if the player can build a given item
     * @param buildItem
     * @param hasZombies
     * @return true/false
     */
    public boolean canBuild(String buildItem, boolean hasZombies) {
        switch (buildItem) {
            case "bow": {
                return (numberOfItem("wood") >= 1 && numberOfItem("arrow") >= 3);
            }

            case "shield": {
                return (numberOfItem("wood") >= 2 && (numberOfItem("sun_stone") >= 1 || numberOfItem("treasure") >= 1 || numberOfItem("key") >= 1));
            }

            case "sceptre": {
                return (
                (numberOfItem("wood") >= 1 || numberOfItem("arrow") >= 2 ) &&
                (numberOfItem("treasure") >= 1 || numberOfItem("key") >= 1) &&
                (numberOfItem("sun_stone") >= 1)
                );
            }

            case "midnight_armour": {
                return (
                    numberOfItem("armour") >= 1 && 
                    numberOfItem("sun_stone") >= 1 &&
                    !hasZombies
                );
            }
        }

        return false;
    }

    /**
     * builds the item, removing the used resources from inventory and adds the item to the player's inventory.
     * @param buildable
     */
    public void build(String buildable) {
        switch (buildable) {
            case "bow": {
                removeItemByType("wood");
                removeMultipleItemsByType("arrow", 3);
                addItem(new Bow("bow" + numberOfItems(), "bow"));
                break;
            }
            case "shield": {
                removeMultipleItemsByType("wood", 2);

                if (numberOfItem("sun_stone") >= 1) {
                }
                else if (numberOfItem("treasure") >= 1) {
                    removeItemByType("treasure");
                }
                else {
                    removeItemByType("key");
                }
                addItem(new Shield("shield" + numberOfItems(), "shield"));
                break;
            }
            case "sceptre": {

                if (numberOfItem("wood") >= 1) {
                    removeItemByType("wood");
                } 
                else removeMultipleItemsByType("arrow", 2);

                if (numberOfItem("treasure") >= 1) {
                    removeItemByType("treasure");
                } 
                else removeItemByType("key");

                addItem(new Sceptre("sceptre" + numberOfItems(), "sceptre"));
                break;
            }
            case "midnight_armour": {
                removeItemByType("armour");
                addItem(new MidnightArmour("midnight_armour" + numberOfItems(), "midnight_armour"));
                break;
            }
        }
    }

    /**
     * helper method for getItemResponseList
     * @param item
     * @return ItemResponse
     */
    private ItemResponse getItemResponse(Entity item) {
        return new ItemResponse(item.getId(), item.getType());
    }

    /**
     * Returns an item response list of the inventory.
     * @return ItemResponseList
     */
    public ArrayList<ItemResponse> getItemResponseList() {
        ArrayList<ItemResponse> itemResponses = new ArrayList<ItemResponse>();

        for (String itemType : items.keySet()) {
            for (Entity i : items.get(itemType)) {
                itemResponses.add(getItemResponse(i));
            }
        }

        return itemResponses;
    }

    /**
     * Helper method to generate unique id's for the built entities.
     * @return number of items total within the player's inventory
     */
    private int numberOfItems() {
        int i = 0;
        for (ArrayList<Entity> entityList : items.values()) {
            i += entityList.size();
        }
        return i;
    }

}
