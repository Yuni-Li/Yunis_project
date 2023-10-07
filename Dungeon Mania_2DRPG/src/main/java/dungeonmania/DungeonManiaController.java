package dungeonmania;

import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.json.JSONArray;
import org.json.JSONObject;

import dungeonmania.BuildableEntities.Sceptre;
import dungeonmania.CollectableEntities.Armour;
import dungeonmania.CollectableEntities.Arrow;
import dungeonmania.CollectableEntities.Bomb;
import dungeonmania.CollectableEntities.HealthPotion;
import dungeonmania.CollectableEntities.InvincibilityPotion;
import dungeonmania.CollectableEntities.InvisibilityPotion;
import dungeonmania.CollectableEntities.Key;
import dungeonmania.CollectableEntities.SunStone;
import dungeonmania.CollectableEntities.Sword;
import dungeonmania.CollectableEntities.TheOneRing;
import dungeonmania.CollectableEntities.Treasure;
import dungeonmania.CollectableEntities.Wood;
import dungeonmania.Dijkstra.Edge;
import dungeonmania.Dijkstra.Graph;
import dungeonmania.Dijkstra.Vertex;
import dungeonmania.Goals.BouldersGoal;
import dungeonmania.Goals.EnemiesGoal;
import dungeonmania.Goals.ExitGoal;
import dungeonmania.Goals.Goal;
import dungeonmania.Goals.GoalComponent;
import dungeonmania.Goals.GoalLeaf;
import dungeonmania.Goals.TreasureGoal;
import dungeonmania.MovingEntities.Assassin;
import dungeonmania.MovingEntities.Hydra;
import dungeonmania.MovingEntities.Mercenary;
import dungeonmania.MovingEntities.MovingEntity;
import dungeonmania.MovingEntities.Npc;
import dungeonmania.MovingEntities.Player;
import dungeonmania.MovingEntities.Spider;
import dungeonmania.MovingEntities.ZombieToast;
import dungeonmania.StaticEntities.Boulder;
import dungeonmania.StaticEntities.ClosedDoor;
import dungeonmania.StaticEntities.Exit;
import dungeonmania.StaticEntities.FloorSwitch;
import dungeonmania.StaticEntities.HardSpawn;
import dungeonmania.StaticEntities.OpenDoor;
import dungeonmania.StaticEntities.Portal;
import dungeonmania.StaticEntities.StandardSpawn;
import dungeonmania.StaticEntities.Swamp;
import dungeonmania.StaticEntities.Wall;
import dungeonmania.StaticEntities.ZombieToastSpawner;
import dungeonmania.exceptions.InvalidActionException;
import dungeonmania.response.models.DungeonResponse;
import dungeonmania.response.models.EntityResponse;
import dungeonmania.response.models.ItemResponse;
import dungeonmania.util.Direction;
import dungeonmania.util.FileLoader;
import dungeonmania.util.Position;


public class DungeonManiaController {
    private GameMap gameMap;
    private Graph dijkstraGraph;
    private Position entryPosition;
    private Position playerPosition;
    private Player player;
    private String dungeonName;
    private int tickCounter;
    private Goal goal;
    private ArrayList<GoalLeaf> leafObservers;
    private String gameMode;
    private JSONObject goalCondition;
    private Sceptre activeSceptre;

    // maps for active enemies
    private Map<String, Mercenary> mercMap = new HashMap<>();
    private Map<String, Assassin> assassinMap = new HashMap<>();
    private Map<String, Spider> spiderMap = new HashMap<>();
    private Map<String, ZombieToast> zombMap = new HashMap<>();
    private Map<String, Hydra> hydraMap = new HashMap<>();
    

    // list of zombie toast spawners
    private List<ZombieToastSpawner> zombieSpawnList = new ArrayList<>();


    public DungeonManiaController() {
    }

    public String getSkin() {
        return "default";
    }

    public String getLocalisation() {
        return "en_US";
    }

    public List<String> getGameModes() {
        return Arrays.asList("standard", "peaceful", "hard");
    }

    /**
     * /dungeons
     * 
     * Done for you.
     */
    public static List<String> dungeons() {
        try {
            return FileLoader.listFileNamesInResourceDirectory("/dungeons");
        } catch (IOException e) {
            return new ArrayList<>();
        }
    }

    /**
     * Extracts entities out of a .json file and populates the gameMap.
     * @param dungeonName the name of the dungeon (named after the .json file) 
     * @param gameMode the game difficulty (peaceful, standard or hard)
     * @return returns a dungeon response object for the dungeon that was made
     * @throws IllegalArgumentException Throws if dungeonName or gameMode aren't strings, or if the dungeon given isn't in the dungeons list.
     */
    public DungeonResponse newGame(String dungeonName, String gameMode) throws IllegalArgumentException {
        if (!dungeonName.getClass().getSimpleName().equals("String") || !gameMode.getClass().getSimpleName().equals("String")
            || !dungeons().contains(dungeonName)) {
            throw new IllegalArgumentException();
        }

        
        this.activeSceptre = null;
        this.tickCounter = 1;
        this.dungeonName = dungeonName;
        this.gameMode = gameMode;

        String dungeonFilePath = "dungeons/" + dungeonName + ".json";
        JSONObject dungeonInfo = null;

        try {
            dungeonInfo = new JSONObject(FileLoader.loadResourceFile(dungeonFilePath));  
        } catch (IOException e) {
            e.printStackTrace();
        }

        List<EntityResponse> entityResponseList = new ArrayList<>();
        JSONArray entities = dungeonInfo.getJSONArray("entities");

        gameMap = makeGameMap(entities);

        // create player first, because mercenary needs the player's position
        for (int i = 0; i < entities.length(); i++) {
            JSONObject currEntity = entities.getJSONObject(i);

            int x = currEntity.getInt("x");
            int y = currEntity.getInt("y");
            String type = currEntity.getString("type");

            if (type.startsWith("player")) {
                entryPosition = new Position(x, y, 100);
                playerPosition = new Position(x, y, 100);

                Entity newEntity = new Player("player", type, playerPosition, gameMap);
                player = (Player) newEntity;
                gameMap.addEntity(newEntity, x, y, 100);
                entityResponseList.add(new EntityResponse("player", type, playerPosition, false));
            }

        }

        // create entity objects and entityResponses (except mercenaries)
        for (int i = 0; i < entities.length(); i++) {
            JSONObject currEntity = entities.getJSONObject(i);

            int x = currEntity.getInt("x");
            int y = currEntity.getInt("y");
            String type = currEntity.getString("type");
            
            // if currEntity is a wall or door, get their "key" value.
            int keyPairId = 0;
            if (type.startsWith("door") || type.startsWith("key")) {
                keyPairId = currEntity.getInt("key");
            }

            // if currEntity is a swamp tile, get their movement factor
            int movementFactor = 0;
            if (type.startsWith("swamp")) {
                movementFactor = currEntity.getInt("movement_factor");
            }

            // skip if entity is mercenary or assassin (we want to create mercenaries after other entites due to dijkstra algorithm)
            if (type.startsWith("mercenary") || type.startsWith("assassin")) {
                continue;
            }

            // helper function to create entities and add to them to gameMap, as well as create and add their EntityResponse
            // objects to entityResponseList
            entityResponseList = createEntity(entityResponseList, x, y, type, keyPairId, movementFactor, Integer.toString(i));
        }
        

        // create dijkstraGraph and mercenaries and assassins
        dijkstraGraph = makeDijkstraGraph();
        for (int i = 0; i < entities.length(); i++) {
            JSONObject currEntity = entities.getJSONObject(i);

            int x = currEntity.getInt("x");
            int y = currEntity.getInt("y");
            String type = currEntity.getString("type");

            if (type.startsWith("mercenary")) {
                EntityResponse mercResponse = addMercToHashMap(x, y);
                entityResponseList.add(mercResponse);
            }
            if (type.startsWith("assassin")) {
                EntityResponse assResponse = addAssassinToHashMap(x, y);
                entityResponseList.add(assResponse);
            }
        }


        initialiseGoals(dungeonInfo);

        return makeDungeonResponse();
    }

    

    public GameMap makeGameMap(JSONArray entities) {

        int width = 0;
        int length = 0;
        int height = 0;
        leafObservers = new ArrayList<>();
        generateMercMap();
        generateAssassinMap();
        generateSpiderMap();
        generateZombMap();
        generateHydraMap();

        for (int i = 0; i < entities.length(); i++) {
            JSONObject currEntity = entities.getJSONObject(i);
            if (width < currEntity.getInt("x")) {
                width = currEntity.getInt("x");
            }
            if (length < currEntity.getInt("y")) {
                length = currEntity.getInt("y");
            }
            height = i;
        }

        return new GameMap(width + 5, length + 5, height + 100);
    }

    /**
     * This method initialises the observer/subject lists of all boulder and floorswitch entities on the map.
     */
    private void initialiseSwitchBoulderObservers(ArrayList<Boulder> boulders, ArrayList<FloorSwitch> switches) {
        
        for (int i = 0; i < gameMap.getWidth(); i++) {
            for (int j = 0; j < gameMap.getLength(); j++) {
                Entity currentSwitch = gameMap.getEntity(i, j, 1);
                if ((currentSwitch instanceof FloorSwitch)) {
                    switches.add( (FloorSwitch) currentSwitch);
                }
                Entity currentBoulder = gameMap.getEntity(i, j, 0);
                if ((currentBoulder instanceof Boulder)) {
                    boulders.add( (Boulder) currentBoulder);
                }
            }
        }
        
        // initialisation
        for (Boulder boulder : boulders) {
            for (FloorSwitch floorSwitch : switches) {
                floorSwitch.boulderInitialise(boulder);
            }
        }
    }

    /**
     * initialises the switches, boulders and the bouldersGoal for the switches.
     * @param boulders
     * @param switches
     */
    private void initialiseSwitchBoulderGoals(ArrayList<Boulder> boulders, ArrayList<FloorSwitch> switches) {
        GoalLeaf leafObserver = null;
        for (GoalLeaf leaf : leafObservers) {
            if (leaf instanceof BouldersGoal) {
                leafObserver = leaf;
            }
        }
        for (Boulder boulder : boulders) {
            for (FloorSwitch floorSwitch : switches) {
                floorSwitch.addBoulderSubject(boulder);
                boulder.addSwitchObserver(floorSwitch);
                floorSwitch.addBoulderGoal((BouldersGoal) leafObserver);
            }
        }
    }

    public void initialiseGoals(JSONObject dungeonInfo) {
        ArrayList<FloorSwitch> switches = new ArrayList<FloorSwitch>();
        ArrayList<Boulder> boulders = new ArrayList<Boulder>();
        initialiseSwitchBoulderObservers(boulders, switches);

        goalCondition = dungeonInfo.getJSONObject("goal-condition");
        goal = new Goal(goalCondition, gameMap, leafObservers);
        
        initialiseSwitchBoulderGoals(boulders, switches);
    }

    /**
     * Creating DijkstraGraph
     * @return
     */
    public Graph makeDijkstraGraph(){
        List<Vertex> nodes = new ArrayList<Vertex>();
        List<Edge> edges = new ArrayList<Edge>();

        //Creating all vertices
        int totalVertices = 0;
        for (int i = 0; i < gameMap.getWidth(); i++) {
            for (int j = 0; j < gameMap.getLength(); j++) {
                Vertex location = new Vertex("Node_" + totalVertices, new Position(i,j));
                nodes.add(location);
                totalVertices += 1;
            }
        }

        //Creating edges
        int totalEdges = 0;
        int vertexIndex = 0;
        for (Vertex node : nodes){
            List<Position> adjPositions = new ArrayList<>();
            adjPositions.add(node.getPosition().translateBy(0, -1));    //Up
            adjPositions.add(node.getPosition().translateBy(0, 1));     //Down
            adjPositions.add(node.getPosition().translateBy(1, 0));     //Right
            adjPositions.add(node.getPosition().translateBy(-1, 0));    //Left

            for (Position adj : adjPositions){
                int x = adj.getX();
                int y = adj.getY();
                if(x >= 0 && x < gameMap.getWidth() && y >= 0 && y < gameMap.getLength()){
                    //Node is within the map
                    Position adjPos = new Position(x, y);                    
                    int weight = createWeight(adjPos);
                    
                    Edge edge = new Edge("Edge_" + totalEdges, nodes.get(vertexIndex), findVertexFromPosition(nodes, adjPos), weight);
                    edges.add(edge);
                    totalEdges += 1;
                }
            }
            vertexIndex += 1;
        }
        
        
        Graph graph = new Graph(nodes, edges);

        return graph;
    }

    /**
     * Creates a weight for an edge depending on entities present at the destination node
     * 
     * If obstructions such as walls or doors are present, the weight is set to 999999999. 
     * If swamp_tiles are present their weights are set to their movementFactor
     * @param pos
     * @return
     */
    public int createWeight(Position pos){
        Entity entity = gameMap.getEntity(pos.getX(), pos.getY(), 1);
        if(entity != null){
            if(entity.getType().equals("swamp_tile")){
                Swamp swamp = (Swamp) entity;
                return swamp.getMovementFactor();
            }
        }

        if(gameMap.getEntity(pos.getX(), pos.getY(), 0) != null){
            //There is an obstruction
            return 999999999;
        }
        
        // No obstruction
        return 1;
    }

    public Vertex findVertexFromPosition(List<Vertex> nodes, Position pos){
        for (Vertex node : nodes){
            if (node.getPosition().equals(pos)){
                return node;
            }
        }
        throw new RuntimeException("Node not found, this shouldn't happen");
    }
    /**
     * Helper function for newGame
     * @param element a goal component to pretty-print from
     * @return String of pretty-printed goals
     */
    public String prettyPrintGoals(GoalComponent element) {
        return element.prettyPrint();
    }

    /**
     * Fills the spiderMap with 5 unique spider ids as keys and null for their values.
     * Used in addSpiderToHashMap
     */
    public void generateSpiderMap() {
        spiderMap.clear();

        for (int i = 0; i < 5; i++) {
            spiderMap.put("spider" + i, null);
        }
    }

    /**
     * Adds a spider to the hashmap, the gameMap, and creates an entityResponse
     * @param x x-coordinate of where spider is being created
     * @param y y-coordinate of where spider is being created
     * @return returns entityResponse of newly created spider, or null if spiderMap is full
     */
    public EntityResponse addSpiderToHashMap(int x, int y) {
        EntityResponse spiderRes = null;
        boolean spiderAdded = false;
        
        // Spider's spawn point must not cause it's cicular path to go off the map
        if (x < 2 || (x > gameMap.getWidth() - 2) || y < 2 ||( y > gameMap.getLength() - 2)) {
            return spiderRes;
        }
        
        for (String spiderId : spiderMap.keySet()) {
            
            if (spiderMap.get(spiderId) == null) {
                // calculate layer
                int layer = 11 + Integer.parseInt(spiderId.substring(6, spiderId.length()));

                // create spider and its EntityResponse
                Spider spider = new Spider(spiderId, "spider", new Position(x, y, layer), gameMap);
                spiderMap.put(spiderId, spider);
                spiderRes = new EntityResponse(spiderId, "spider", new Position(x, y, layer), false);

                // add spider to gameMap
                gameMap.addEntity(spider, x, y, layer);

                spiderAdded = true;

                break;
            }
        }

        for (GoalLeaf goal : leafObservers) {
            if (goal instanceof EnemiesGoal && spiderAdded) {
                ((EnemiesGoal) goal).incrementEnemyCount();
            }
        }

        return spiderRes;
    }

    /**
     * Fills the mercMap with 20 unique mercenary ids as keys and null for their values.
     * Used in addMercToHashMap
     */
    public void generateMercMap() {
        mercMap.clear();

        for (int i = 0; i < 20; i++) {
            mercMap.put("mercenary" + i, null);
        }
    }

    /**
     * Adds a mercenary to the hashmap, the gameMap, and creates an entityResponse
     * @param x x-coordinate of where mercenary is being created
     * @param y y-coordinate of where mercenary is being created
     * @return returns entityResponse of newly created mercenary, or null if mercMap is full
     */
    public EntityResponse addMercToHashMap(int x, int y) {
        EntityResponse mercRes = null;
        boolean mercAdded = false;
        for (String mercId : mercMap.keySet()) {
            
            if (mercMap.get(mercId) == null) {
                // calculate layer
                int layer = 16 + Integer.parseInt(mercId.substring(9, mercId.length()));

                // create mercenary and its EntityResponse
                Mercenary merc = new Mercenary(mercId, "mercenary", new Position(x, y, layer), player, gameMap, dijkstraGraph);
                mercMap.put(mercId, merc);
                mercRes = new EntityResponse(mercId, "mercenary", new Position(x, y, layer), true);

                // add mercenary to gameMap
                gameMap.addEntity(merc, x, y, layer);

                mercAdded = true;

                break;
            }
        }
        for (GoalLeaf goal : leafObservers) {
            if (goal instanceof EnemiesGoal && mercAdded) {
                ((EnemiesGoal) goal).incrementEnemyCount();
            }
        }

        return mercRes;
    }

    /**
     * Fills the assassinMap with 5 unique asassin ids as keys and null for their values.
     * Used in addAssassinToHashMap
     */
    public void generateAssassinMap(){
        assassinMap.clear();

        for (int i = 0; i < 5; i++) {
            assassinMap.put("assassin" + i, null);
        }
    }
    
    /**
     * Adds a assassin to the hashmap, the gameMap, and creates an entityResponse
     * @param x x-coordinate of where assassin is being created
     * @param y y-coordinate of where assassin is being created
     * @return returns entityResponse of newly created assassin, or null if assassinMap is full
     */
    public EntityResponse addAssassinToHashMap(int x, int y){
        EntityResponse assassinRes = null;
        boolean assAdded = false;

        for(String assId : assassinMap.keySet()) {
            if(assassinMap.get(assId) == null){
                //calculate layer
                int layer = 56 + Integer.parseInt(assId.substring(8, assId.length()));

                //create assassin and its EntityResponse
                Assassin ass = new Assassin(assId, "assassin", new Position(x, y, layer), player, gameMap, dijkstraGraph);
                assassinMap.put(assId, ass);
                assassinRes = new EntityResponse(assId, "assassin", new Position(x, y, layer), true);

                //add assassin to gameMap
                gameMap.addEntity(ass, x, y, layer);
                assAdded = true;
                break;
            }
        }

        for (GoalLeaf goal : leafObservers) {
            if (goal instanceof EnemiesGoal && assAdded) {
                ((EnemiesGoal) goal).incrementEnemyCount();
            }
        }
        return assassinRes;
    }

    /**
     * Fills the zombMap with 20 unique zombieToast ids as keys and null for their values.
     * Used in addZombToHashMap
     */
    public void generateZombMap() {
        zombMap.clear();

        for (int i = 0; i < 20; i++) {
            zombMap.put("zombie" + i, null);
        }
    }

    /**
     * Adds a zombieToast to the hashmap, the gameMap, and creates an entityResponse
     * @param x x-coordinate of where zombieToast is being created
     * @param y y-coordinate of where zombieToast is being created
     * @return returns entityResponse of newly created zombieToast, or null if zombMap is full
     */
    public EntityResponse addZombToHashMap(int x, int y) {
        EntityResponse zombRes = null;
        boolean zombAdded = false;
        for (String zombId : zombMap.keySet()) {
            
            if (zombMap.get(zombId) == null) {
                // calculate layer
                int layer = 36 + Integer.parseInt(zombId.substring(6, zombId.length()));

                // create zombieToast and its EntityResponse
                ZombieToast zomb = new ZombieToast(zombId, "zombie_toast", new Position(x, y, layer), gameMap);
                zombMap.put(zombId, zomb);
                zombRes = new EntityResponse(zombId, "zombie_toast", new Position(x, y, layer), false);

                // add zombieToast to gameMap
                gameMap.addEntity(zomb, x, y, layer);

                zombAdded = true;

                break;
            }
        }
        for (GoalLeaf goal : leafObservers) {
            if (goal instanceof EnemiesGoal && zombAdded) {
                ((EnemiesGoal) goal).incrementEnemyCount();
            }
        }

        return zombRes;
    }

    /**
     * Fills the hydraMap with 5 unique hydra ids as keys and null for their values.
     * Used in addToHydraHashMap
     */
    public void generateHydraMap(){
        hydraMap.clear();

        for (int i = 0; i < 5; i++) {
            hydraMap.put("hydra" + i, null);
        }
    
    }

    /**
     * Adds a hydra to the hashmap, the gameMap, and creates an entityResponse
     * @param x x-coordinate of where hydra is being created
     * @param y y-coordinate of where hydra is being created
     * @return returns entityResponse of newly created hydra, or null if hydraMap is full
     */
    public EntityResponse addHydraToHashMap(int x, int y){
        EntityResponse hydraRes = null;
        boolean hydraAdded = false;

        for (String hydraId : hydraMap.keySet()) {
            
            if (hydraMap.get(hydraId) == null) {
                // calculate layer
                int layer = 61 + Integer.parseInt(hydraId.substring(5, hydraId.length()));

                // create Hydra and its EntityResponse
                Hydra hydra = new Hydra(hydraId, "hydra", new Position(x, y, layer), gameMap);
                hydraMap.put(hydraId, hydra);
                hydraRes = new EntityResponse(hydraId, "hydra", new Position(x, y, layer), true);

                // add Hydra to gameMap
                gameMap.addEntity(hydra, x, y, layer);

                hydraAdded = true;
                break;
            }
        }

        for (GoalLeaf goal : leafObservers) {
            if (goal instanceof EnemiesGoal && hydraAdded) {
                ((EnemiesGoal) goal).incrementEnemyCount();
            }
        }

        return hydraRes;
    }
    /**
     * Helper function for newGame and LoadGame to create an entity. It also creates an entity response and adds
     * it to the entity response list.
     * @param entityResponseList list of entity responses that will go in a DungeonResponse
     * @param x x-coordinate of the entity being created
     * @param y y-coordinate of the entity being created
     * @param type the type of object being created
     * @param assignedId the id of the object being created
     * @return returns an updated list of entity responses
     */
    public List<EntityResponse> createEntity(List<EntityResponse> entityResponseList, int x, int y, String type, int keyPairId, int movementFactor, String assignedId) {
        int layer = 0;
        Entity newEntity = null;

        // create entities and add to gameMap.
        // static entities
        if (type.startsWith("wall")) {
            layer = 0;
            newEntity = new Wall(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("exit")) {
            layer = 1;
            newEntity = new Exit(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("boulder")) {
            layer = 0;
            newEntity = new Boulder(assignedId, type, new Position(x, y, layer));
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("switch")) {
            layer = 1;
            newEntity = new FloorSwitch(assignedId, type, new Position(x, y, layer));
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("door") && !type.contains("Open")) {
            layer = 0;
            newEntity = new ClosedDoor(assignedId, type, keyPairId);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("door") && type.contains("Open")) {
            layer = 1;
            newEntity = new OpenDoor(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("portal")) {
            layer = 1;
            newEntity = new Portal(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.equals("zombie_toast_spawner")) {
            layer = 2;
            Position spawnerPos = new Position(x, y, layer);
            
            if (gameMode.equals("hard")) {
                newEntity = new ZombieToastSpawner(assignedId, type, spawnerPos, gameMap, new HardSpawn());
            } else {
                newEntity = new ZombieToastSpawner(assignedId, type, spawnerPos, gameMap, new StandardSpawn());
            }
            
            gameMap.addEntity(newEntity, x, y, layer);

            // add to zombieSpawnList
            zombieSpawnList.add((ZombieToastSpawner)newEntity);
        }

        if (type.startsWith("swamp_tile")) {
            layer = 1;
            newEntity = new Swamp(assignedId, type, movementFactor);
            gameMap.addEntity(newEntity, x, y, layer);
        }


        // moving entities
        if (type.startsWith("spider")) {
            // add to spiders map
            EntityResponse spiderResponse = addSpiderToHashMap(x, y);
            if (spiderResponse != null) {
                entityResponseList.add(spiderResponse);
            }

            return entityResponseList;
        }

        if (type.startsWith("zombie_toast") && !type.equals("zombie_toast_spawner")) {
            // add to zombies map
            EntityResponse zombieResponse= addZombToHashMap(x, y);
            if (zombieResponse != null) {
                entityResponseList.add(zombieResponse);
            }

            return entityResponseList;
        }

        if (type.startsWith("assassin")) {
            // add to assassins map
            EntityResponse assassinResponse = addAssassinToHashMap(x, y);
            if (assassinResponse != null) {
                entityResponseList.add(assassinResponse);
            }

            return entityResponseList;
        }

        if (type.startsWith("hydra")) {
            // add to hydra map
            EntityResponse hydraResponse = addHydraToHashMap(x, y);
            if (hydraResponse != null) {
                entityResponseList.add(hydraResponse);
            }

            return entityResponseList;
        }

    
        // collectable entities (incl. the one ring)
        if (type.startsWith("treasure")) {
            layer = 3;
            newEntity = new Treasure(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        // need to be able to create door-key pairs. 
        if (type.startsWith("key")) {
            layer = 3;
            newEntity = new Key(assignedId, type, keyPairId);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("health_potion")) {
            layer = 3;
            newEntity = new HealthPotion(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("invincibility_potion")) {
            layer = 3;
            newEntity = new InvincibilityPotion(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("invisibility_potion")) {
            layer = 3;
            newEntity = new InvisibilityPotion(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("wood")) {
            layer = 3;
            newEntity = new Wood(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("arrow")) {
            layer = 3;
            newEntity = new Arrow(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("bomb")) {
            layer = 3;
            newEntity = new Bomb(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("sword")) {
            layer = 3;
            newEntity = new Sword(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("armour")) {
            layer = 3;
            newEntity = new Armour(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("one_ring")) {
            layer = 3;
            newEntity = new TheOneRing(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        if (type.startsWith("sun_stone")) {
            layer = 3;
            newEntity = new TheOneRing(assignedId, type);
            gameMap.addEntity(newEntity, x, y, layer);
        }

        
        // create EntityResponse and add to entityResponseList
        Boolean interactable = (type.equals("mercenary") || type.equals("zombie_toast_spawner"));
        entityResponseList.add(new EntityResponse(assignedId, type, new Position(x, y, layer), interactable));

        return entityResponseList;
    }

    /**
     * Saves current game instance as a .json file in src/main/resources/savedGames
     * @param name name of the save file
     * @return returns a dungeonResponse of the current isntance.
     * @throws IllegalArgumentException Shouldn't throw anything (spec was updated to show no exceptions)
     */
    public DungeonResponse saveGame(String name) throws IllegalArgumentException {

        // create JSON object to save game in
        JSONObject gameSave = new JSONObject();
        JSONArray entities = new JSONArray();

        // create EntityResponse list
        List<EntityResponse> entityResponseList = new ArrayList<>();
        int idGenerator = 1;

        // loop through all entities on map and save as json objects
        for(int i = 0 ; i < gameMap.getWidth() ; i++){
            for(int j = 0 ; j < gameMap.getLength() ; j++){
                for(int k=0 ; k < gameMap.getHeight() ; k++){
            
                    if (gameMap.getEntity(i, j, k) != null) {
                        entityResponseList = saveEntity(entityResponseList, entities, gameMap.getEntity(i, j, k), i, j, k, Integer.toString(idGenerator));
                        idGenerator++;
                    }

                }
            }
        }

        // put entities jsonArray in gameSave json object
        gameSave.put("entities", entities);

        // put gameMode in gameSave json object
        gameSave.put("gameMode", this.gameMode);
        
        // put goal-conditions in.
        gameSave.put("goal-condition", goalCondition);

        // check if savedGames folder exists, if not, create it
        try {
            Files.createDirectories(Paths.get("savedGames"));
        } catch (IOException e1) {
            e1.printStackTrace();
        }


        // write gameSave to json file in savedGames 
        try {
            FileWriter file = new FileWriter(Paths.get("savedGames/" + name + ".json").toString());
            file.write(gameSave.toString());
            file.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        
        return makeDungeonResponse();
    }

    /**
     * Helper function for saveGame. Saves an entity as a jsonobject in a jsonArray. Also creates and saves an entityresponse in an entityresponseList
     * @param entityResponseList List of entity responses
     * @param savedEntities JSONArray of Entities as JSONObjects
     * @param entity the current entity being saved
     * @param x the x-coordinate of the entity being saved
     * @param y the y-coordinate of the entity being saved
     * @param layer the layer that the entity is on (the z-coordinate essentially)
     * @param assignedId the id of the entity being saved
     * @return returns an updated entityResponseList
     */
    public List<EntityResponse> saveEntity(List<EntityResponse> entityResponseList, JSONArray savedEntities, Entity entity,  int x, int y, int layer, String assignedId) {
        
        // create JSONObject to store entity info in
        JSONObject savedEntity = new JSONObject();
        savedEntity.put("x", x);
        savedEntity.put("y", y);
        
        String type = null;
        Boolean interactable = false;

        
        // if static entity
        if (entity instanceof Wall) {
            type = "wall";
            savedEntity.put("type", type);
        }

        if (entity instanceof Exit) {
            type = "exit";
            savedEntity.put("type", type);
        }

        if (entity instanceof Boulder) {
            type = "boulder";
            savedEntity.put("type", type);
        }

        if (entity instanceof FloorSwitch) {
            type = "switch";
            savedEntity.put("type", type);
        }

        if (entity instanceof ClosedDoor) {
            type = "door";
            savedEntity.put("type", type);
            savedEntity.put("key", ((ClosedDoor)entity).getKeyPairId());
        }

        if (entity instanceof OpenDoor) {
            type = "doorOpen";
            savedEntity.put("type", type);
        }

        if (entity instanceof Portal) {
            type = "portal";
            savedEntity.put("type", type);
        }

        if (entity instanceof ZombieToastSpawner) {
            interactable = true;

            type = "zombie_toast_spawner";
            savedEntity.put("type", type);
        }

        if (entity instanceof Swamp) {
            type = "swamp_tile";
            savedEntity.put("type", type);
            savedEntity.put("movement_factor", ((Swamp)entity).getMovementFactor());
        }


        // if moving entity
        if (entity instanceof Player) {
            type = "player";
            savedEntity.put("type", type);
        }

        if (entity instanceof Spider) {
            type = "spider";
            savedEntity.put("type", type);
        }

        if (entity instanceof ZombieToast) {
            type = "zombie_toast";
            savedEntity.put("type", type);
        }

        if (entity instanceof Mercenary) {
            interactable = true;

            if (entity instanceof Assassin) {
                type = "assassin";
                savedEntity.put("type", type);
            } else {
               type = "mercenary";
                savedEntity.put("type", type); 
            }

            
        }

        if (entity instanceof Hydra) {
            type = "hydra";
            savedEntity.put("type", type);
        }


        // if collectable entity
        if (entity instanceof Treasure) {
            type = "treasure";
            savedEntity.put("type", type);
        }

        if (entity instanceof Key) {
            type = "key";
            savedEntity.put("type", type);
            savedEntity.put("key", ((Key)entity).getKeyPairId());
        }

        if (entity instanceof HealthPotion) {
            type = "health_potion";
            savedEntity.put("type", type);
        }

        if (entity instanceof InvincibilityPotion) {
            type = "invincibility_potion";
            savedEntity.put("type", type);
        }

        if (entity instanceof InvisibilityPotion) {
            type = "invisibility_potion";
            savedEntity.put("type", type);
        }

        if (entity instanceof Wood) {
            type = "wood";
            savedEntity.put("type", type);
        }

        if (entity instanceof Arrow) {
            type = "arrow";
            savedEntity.put("type", type);
        }

        if (entity instanceof Bomb) {
            type = "bomb";
            savedEntity.put("type", type);
        }

        if (entity instanceof Sword) {
            type = "sword";
            savedEntity.put("type", type);
        }

        if (entity instanceof Armour) {
            type = "armour";
            savedEntity.put("type", type);
        }

        if (entity instanceof TheOneRing) {
            type = "one_ring";
            savedEntity.put("type", type);
        }

        if (entity instanceof SunStone) {
            type = "sun_stone";
            savedEntity.put("type", type);
        }

        entityResponseList.add(new EntityResponse(assignedId, type, new Position(x, y, layer), interactable));
        savedEntities.put(savedEntity);

        return entityResponseList;
    }

    /**
     * Loads a game from savedGames. Works similarly to newGame but extracts json object from savedGames
     * instead of dungeons.
     * @param name The name of the savefile
     * @return returns a dungeonResponse of the new game instance
     * @throws IllegalArgumentException throws if name isn't in list of saved games.
     */
    public DungeonResponse loadGame(String name) throws IllegalArgumentException {
        if (!allGames().contains(name)) {
            throw new IllegalArgumentException();
        }

        this.tickCounter = 1;
        
        String dungeonFilePath = "savedGames/" + name + ".json";
        JSONObject dungeonInfo = null;

        
        try {
            dungeonInfo = new JSONObject(new String(Files.readAllBytes((Paths.get("savedGames", name + ".json")))));
        } catch (IOException e) {
            e.printStackTrace();
        }

        // set gameMode
        this.gameMode = dungeonInfo.getString("gameMode");

        List<EntityResponse> entityResponseList = new ArrayList<>();
        JSONArray entities = dungeonInfo.getJSONArray("entities");
        gameMap = makeGameMap(entities);

        // create player first, because mercenary needs the player's position
        for (int i = 0; i < entities.length(); i++) {
            JSONObject currEntity = entities.getJSONObject(i);

            int x = currEntity.getInt("x");
            int y = currEntity.getInt("y");
            String type = currEntity.getString("type");

            if (type.startsWith("player")) {
                entryPosition = new Position(x, y, 100);
                playerPosition = new Position(x, y, 100);

                Entity newEntity = new Player("player", type, playerPosition, gameMap);
                gameMap.addEntity(newEntity, x, y, 100);
                player = (Player) newEntity;
                entityResponseList.add(new EntityResponse("player", type, playerPosition, false));
            }

        }

        // create entity objects and entityResponses (except mercenaries)
        for (int i = 0; i < entities.length(); i++) {
            JSONObject currEntity = entities.getJSONObject(i);

            int x = currEntity.getInt("x");
            int y = currEntity.getInt("y");
            String type = currEntity.getString("type");
            
            // if current Entity is a wall or door, get their "key" value.
            int keyPairId = 0;
            if (type.startsWith("door") || type.startsWith("key")) {
                keyPairId = currEntity.getInt("key");
            }

            // if currEntity is a swamp tile, get their movement factor
            int movementFactor = 0;
            if (type.startsWith("swamp")) {
                movementFactor = currEntity.getInt("movement_factor");
            }

            // skip if entity is mercenary or assasin (we want to create mercenaries after other entites due to dijkstra algorithm)
            if (type.startsWith("mercenary") || type.startsWith("assassin")) {
                continue;
            }

            // helper function to create entities and add to them to gameMap, as well as create and add their EntityResponse
            // objects to entityResponseList
            entityResponseList = createEntity(entityResponseList, x, y, type, keyPairId, movementFactor, Integer.toString(i));
        }

        // create dijkstraGraph and mercenaries
        dijkstraGraph = makeDijkstraGraph();
        for (int i = 0; i < entities.length(); i++) {
            JSONObject currEntity = entities.getJSONObject(i);

            int x = currEntity.getInt("x");
            int y = currEntity.getInt("y");
            String type = currEntity.getString("type");

            if (type.startsWith("mercenary")) {
                EntityResponse mercResponse = addMercToHashMap(x, y);
                entityResponseList.add(mercResponse);
            }
            if (type.startsWith("assassin")) {
                EntityResponse assResponse = addAssassinToHashMap(x, y);
                entityResponseList.add(assResponse);
            }
        }

        initialiseGoals(dungeonInfo);

        return makeDungeonResponse();
    }

    /**
     * shows all the currently saved games
     * @return returns a list of all saveFile names
     */
    public List<String> allGames() {
        try {
            return FileLoader.listFileNamesInDirectoryOutsideOfResources("savedGames");
        } catch (IOException e) {
            return new ArrayList<>();
        }
    }


    /**
     * Performs 1 tick on the front end
     * 
     * @param itemUsed the id of the item being used
     * @param movementDirection the direction the player is moving in
     * @param buildables the list of currently buildable entity's types
     * @return returns dungeon response of the map after the player has moved
     * @throws IllegalArgumentException
     * @throws InvalidActionException
     */
    public DungeonResponse tick(String itemUsed, Direction movementDirection) throws IllegalArgumentException, InvalidActionException {
        
        if(this.activeSceptre != null) {
            setMindControl(true);
            this.activeSceptre.dischargingSceptre();
        }
        
      
        else if(player.getSceptre(itemUsed) != null){
            Sceptre sceptre = player.getSceptre(itemUsed);
            sceptre.setActive(true);
            this.activeSceptre = sceptre;
            
            setMindControl(true);
            sceptre.dischargingSceptre();
        }

        player.move(movementDirection);
        playerPosition = player.getPosition();

        updateMoveGoals();
        collectItem();

        preparingForBattle();
        createRandomEnemy();
        moveMovingEntities();
        preparingForBattle();
        // spawn zombies from zombie toast spawners
        for (ZombieToastSpawner spawner : zombieSpawnList) {
            Position spawnPoint = spawner.spawnZombie(tickCounter);
            if (spawnPoint != null) {
                addZombToHashMap(spawnPoint.getX(), spawnPoint.getY());
            }
        }
        tickCounter += 1;



        if(this.activeSceptre != null) {
            if (this.activeSceptre.getTicksLeft() <= 0){
                this.activeSceptre.setActive(false);
                this.activeSceptre = null;
                setMindControl(false);
            }
            
            player.rechargeAllSceptresExceptFor(this.activeSceptre.getId());
        }
        return makeDungeonResponse();
    }

    private void setMindControl(boolean isControlled){
        // Mind control all merc on map
        for (Mercenary merc : mercMap.values()){
            merc.setUnderSpectreInfluence(isControlled);
        }
        // Mind control all assassin on map
        for (Assassin assassin : assassinMap.values()){
            assassin.setUnderSpectreInfluence(isControlled);
        }
    }
    /**
     * Updates movement based goals, treasure and exit. updates before item collection to ensure treasure is updated correctly.
     */
    private void updateMoveGoals() {
        // update treasureObserver.
        Entity currentCollectible = gameMap.getEntity(playerPosition.getX(), playerPosition.getY(), 3);
        
        for (GoalLeaf observer : leafObservers) {
            if ((currentCollectible instanceof Treasure || currentCollectible instanceof SunStone) && observer instanceof TreasureGoal) {
                ((TreasureGoal) observer).decrementTreasure();
            } else if (playerOnExit() && observer instanceof ExitGoal) {
                ((ExitGoal) observer).setOnExit(true);
            } else if (!playerOnExit() && observer instanceof ExitGoal) {
                ((ExitGoal) observer).setOnExit(false);
            }
        }

    }

    private DungeonResponse makeDungeonResponse() {
        return new DungeonResponse(
            "dungeon-id", 
            dungeonName, 
            gameMap.makeEntityResponseList(), 
            player.getInventory().getItemResponseList(), 
            player.getInventory().getBuildables(hasZombies()), 
            goal.getGoalString()
            );
    }

    private boolean playerOnExit() {
        return gameMap.getEntity(playerPosition.getX(), playerPosition.getY(), 1) instanceof Exit;
    }


    /**
     * helper method to collect items.
     */
    private void collectItem() {
        Entity currentCollectible = gameMap.getEntity(playerPosition.getX(), playerPosition.getY(), 3);
        // check if on item.
        if (currentCollectible != null) {

            player.getInventory().addItem(gameMap.getEntity(playerPosition.getX(),playerPosition.getY(), 3));
            gameMap.removeEntity(playerPosition.getX(), playerPosition.getY(), 3);
        }
    }
    
    /**
     * Searches for enemies to battle
     */
    private void preparingForBattle(){
        int additionalDamage = 0;
        //Searching for mercenary allies
        for (Mercenary merc : mercMap.values()){
            if(merc!=null){
                if(!merc.isEnemy() || merc.isUnderSpectreInfluence()){
                    additionalDamage += merc.getAttack();
                }
                
            }
        }
        
        for(Assassin assassin : assassinMap.values()){
            if(assassin != null){
                if(!assassin.isEnemy() || assassin.isUnderSpectreInfluence()){
                    additionalDamage += assassin.getAttack();
                }
            }
        }

        // Searching for enemies in same cell as player
        for (int i = 11; i < 66; i++){
            Npc enemy = (Npc) gameMap.getEntity(player.getPosition().getX(), player.getPosition().getY(), i);
            if(enemy instanceof ZombieToast || enemy instanceof Spider|| enemy instanceof Mercenary && enemy.isEnemy()) {
                if (enemy instanceof Mercenary) {
                    Mercenary merc = (Mercenary) enemy;
                    merc.isUnderSpectreInfluence();
                }                
                boolean doBattle = true;
                while (doBattle == true){
                    doBattle = battle(enemy, additionalDamage);
                }
                
            }
        }
    }
    
    /**
     * Executes a single round of battle
     * @param enemy
     * @return
     */
    private boolean battle(MovingEntity enemy, int additionalDamage){
        //Doesn't account for sword or bow yet
        int enemyAttackStat = enemy.getAttack();
        int playerAttackStat = player.getAttack();
        //Check if:
            // Sword/ bow
                //if enemy has: enemyAttackStat = enemyAttackStat + buff
                //if player has: playerAttackStat = playerAttackStat + buff
            // Note: don't need to check for armour. If entity is wearing armour, their health gets buffed

        enemy.loseHealth(playerAttackStat);
        enemy.loseHealth(additionalDamage);
        player.loseHealth(enemyAttackStat);

        // check enemy and player health
            // if player health <= 0: game over
        if (player.getHealth() <= 0){
            gameMap.removeEntity(player.getPosition().getX(), player.getPosition().getY(), player.getPosition().getLayer());
        }
            // if enemy health <= 0: gameMap.removeEntity
        if (enemy.getHealth() <= 0){
            if(enemy instanceof Mercenary) {
                mercMap.put(enemy.getId(), null);
            }
            else if(enemy instanceof Assassin){
                assassinMap.put(enemy.getId(), null);
            }
            else if(enemy instanceof Hydra){
                hydraMap.put(enemy.getId(), null);
            }
            else if(enemy instanceof ZombieToast){
                zombMap.put(enemy.getId(), null);
            }
            else if(enemy instanceof Spider){
                spiderMap.put(enemy.getId(), null);
            }
            gameMap.removeEntity(enemy.getPosition().getX(), enemy.getPosition().getY(), enemy.getPosition().getLayer());

            for (GoalLeaf enemyGoal : leafObservers) {
                if (enemyGoal instanceof EnemiesGoal) {
                    ((EnemiesGoal) enemyGoal).decrementEnemyCount();
                }
            }

            return false;
        }

        return true;
    }

    /**
     * creates a random enemy: Spider, Mercenary, Assassin, Hydra
     */
    private void createRandomEnemy(){
        //Note: the enemies might spawn onto other enemies. CHECK!!! will fix this

        int chooseEnemy = chooseEnemy();
        
        if (chooseEnemy == 2){
             
            //Max of 4 Spiders
            //15,16,17,18
            /*if(spiderMap.size() < 5) {
                String spiderId = "spider" + spiderMap.size();
                Position spawnPoint = new Position(randomPosition(), randomPosition(), 15 + spiderMap.size());
                Spider spider = new Spider(spiderId, "spider", spawnPoint, gameMap);

                spiderMap.put(spiderId, spider);
                gameMap.addEntity(spider, spawnPoint.getX(), spawnPoint.getY(), spawnPoint.getLayer());
            }*/
            Position spawnPoint = new Position(randomPosition(player.getPosition().getX()), randomPosition(player.getPosition().getY()), 15 + spiderMap.size());

            addSpiderToHashMap(spawnPoint.getX(), spawnPoint.getY());

        }

        //String id, String type, Position position, Position player, GameMap gameMap
        else if (chooseEnemy == 3){
            //Spawn Mecenary
            //String mercId = "mercenary" + mercMap.size();
            //layers 10-14 inclusive
            /*Position mercPos = new Position(entryPosition.getX(), entryPosition.getY(), 10 + mercMap.size());

            Mercenary merc = new Mercenary(mercId, "mercenary", mercPos, player, gameMap, dijkstraGraph);
            mercMap.put(mercId, merc);
            gameMap.addEntity(merc, entryPosition.getX(), entryPosition.getY(), entryPosition.getLayer());*/

            addMercToHashMap(entryPosition.getX(), entryPosition.getY());
            
        }

        else if (chooseEnemy == 4){
            //Assassin spawn
            addAssassinToHashMap(entryPosition.getX(), entryPosition.getY());
        }

        else if (chooseEnemy == 5){
            Position spawnPoint = new Position(randomPosition(player.getPosition().getX()), randomPosition(player.getPosition().getY()), 15 + spiderMap.size());
            
            addHydraToHashMap(spawnPoint.getX(), spawnPoint.getY());
        }

        
    }

    /**
     * Chooses an enemy based on preset probability
     * @return 2:Spider, 3:Mecenary, 4: Assassin, 5:Hydra
     */
    private int chooseEnemy(){
        //Hydra will spawn every 50 ticks after the 15th tick
        if (tickCounter >= 15 && (tickCounter-15)%50 == 0 && gameMode.equals("hard")){
            return 5;
        }

        //Mercenary has 10% (1 in 10) chance of spawning
        if (randomIntBetween(1,10) == 1 ) {
            //Assassin has 20% chance of spawning in place of mercenary
            if (randomIntBetween(1,5) == 1 ) {
                return 4;
            }
            return 3;
        }

        //Spider has 18% chance of spawning = 6% + 6% + 6% chance
        if (randomIntBetween(1,6) == 1 || randomIntBetween(1,6) == 1 || randomIntBetween(1,6) == 1) {
            return 2;
        }

        return -1;
    }

    private int randomIntBetween(int min, int max){         
        return (int)Math.floor(Math.random()*(max-min+1)+min);
    }

    /**
     * Gets a random position that is at most 8 units away from a given coordinate
     * @param coordinate
     * @return
     */
    private int randomPosition(int coordinate){
        //Map is bigger than the bouding walls. Maps is offset by 5 cells
        int min = (coordinate - 8) < 5 ? 0 : coordinate - 8;    
        int longestMapSide =(gameMap.getLength() > gameMap.getWidth() ? gameMap.getWidth() : gameMap.getLength()) - 10;
        int max = (coordinate + 8) >= longestMapSide ? longestMapSide : coordinate + 8;
        
        int random_int = (int)Math.floor(Math.random()*(max-min+1)+min);
        return random_int;
    }

    private void moveMovingEntities(){
        moveMercenaries();
        moveAssassins();
        moveSpiders();
        moveHydras();

        moveZombieToasts();

    }

    private void moveMercenaries(){
        for(Mercenary merc : mercMap.values()){
            if (merc != null) {
                gameMap.removeEntity(merc.getPosition().getX(), merc.getPosition().getY(), merc.getPosition().getLayer());
                merc.tryMove();
                gameMap.addEntity(merc,merc.getPosition().getX(), merc.getPosition().getY(), merc.getPosition().getLayer());
            }
        }
    }

    private void moveAssassins(){
        for(Assassin ass : assassinMap.values()){
            if (ass != null) {
                gameMap.removeEntity(ass.getPosition().getX(), ass.getPosition().getY(), ass.getPosition().getLayer());
                ass.tryMove();
                gameMap.addEntity(ass,ass.getPosition().getX(), ass.getPosition().getY(), ass.getPosition().getLayer());
            }
        }
    }

    private void moveSpiders(){
        for(Spider spider : spiderMap.values()){
            if (spider != null) {
                gameMap.removeEntity(spider.getPosition().getX(), spider.getPosition().getY(), spider.getPosition().getLayer());
                spider.tryMove();
                gameMap.addEntity(spider,spider.getPosition().getX(), spider.getPosition().getY(), spider.getPosition().getLayer());
            }
        }
    }

    private void moveHydras(){
        for(Hydra hydra : hydraMap.values()){
            if(hydra != null){
                gameMap.removeEntity(hydra.getPosition().getX(), hydra.getPosition().getY(), hydra.getPosition().getLayer());
                hydra.tryMove();
                gameMap.addEntity(hydra,hydra.getPosition().getX(), hydra.getPosition().getY(), hydra.getPosition().getLayer());
            }
        }
    }

    private void moveZombieToasts(){
        for (ZombieToast zombie : zombMap.values()) {
            if (zombie != null) {
                gameMap.removeEntity(zombie.getPosition().getX(), zombie.getPosition().getY(), zombie.getPosition().getLayer());
                zombie.tryMove();
                gameMap.addEntity(zombie, zombie.getPosition().getX(), zombie.getPosition().getY(), zombie.getPosition().getLayer());
            }
        }
    }

    /**
     * check whether the player has a weapon
     * @return true if the player has a weapon and false if not
     */
    public boolean hasWeapon() {
        if (player.getInventory().numberOfItem("bow") > 0 || player.getInventory().numberOfItem("sword") > 0
            || player.getInventory().numberOfItem("anduril") > 0) {
            return true;
        }
        return false;
    }

    /**
     * can bribe a mercenary/assassin or destroy a zombieToastSpawner
     * @param entityId the id of the item being interacted
     * @param checkValidId check if id is belongs to an interactable entity
     * @param mercenary get the mercenery from the mercMap based on entityId
     * @param assassin get the assasin from the assasinMap based on entityId
     * @param giveOneRing using the_one_ring to bribe a mernary, only true if player doesnot have any treasure
     * @param distanceVector the position vector of mercenary/assassin relative to the player
     * @param distanceBetween the distance between the mercenary/assassin and the player
     * @param isAdjacent check if player is cardinally adjacent to the spawner
     * @return returns dungeon response of the map after the interact is done
     * @throws IllegalArgumentException if id is belongs to none of mercenary, assassin and zombieToastSpawner
     * @throws InvalidActionException Case1. Mercenary is still an enemy (bribe failed)
                                      Case2. If the player is not within 2 cardinal tiles to the mercenary, if they are bribing
                                      Case3. Assassin is still an enemy (bribe failed)
                                      Case4. If the player is not within 2 cardinal tiles to the assassin, if they are bribing
                                      Case5. If the player does not have a weapon and attempts to destroy a spawner
                                      Case6. If the player is not cardinally adjacent to the spawner, if they are destroying a spawner
     */
    public DungeonResponse interact(String entityId) throws IllegalArgumentException, InvalidActionException {

        boolean checkValidId = false;
        Position distanceVector = null;
        double distanceBetween = 0;

        // Interact with mercenary
        Mercenary mercenary = mercMap.get(entityId);
        boolean giveOneRing = false;

        if (player.getInventory().numberOfItem("treasure") == 0) giveOneRing = true;
        
        if(mercenary != null){
            checkValidId = true;
            if (mercenary.isEnemy()) {
                mercenary.bribe(player.getInventory().numberOfItem("treasure"), giveOneRing);
            }
    
            distanceVector = Position.calculatePositionBetween(player.getPosition(), mercenary.getPosition());
            distanceBetween = Math.pow((Math.pow(distanceVector.getX(), 2) + Math.pow(distanceVector.getY(), 2)), 0.5);

            
            if (distanceBetween > 2) {
                throw new InvalidActionException("It's too far from the mercenary!");
            } else if (mercenary.isEnemy()) {
                throw new InvalidActionException("Don't have enough treasure!");
            } else {
                ArrayList<ItemResponse> items = player.getInventory().getItemResponseList();
    
                int numTreasure = 0;
                for (ItemResponse item: items) {
                    if (item.getType().equals("treasure") && numTreasure < 1) {
                        player.getInventory().removeItem(item.getId());
                        numTreasure++;
                    }
                }
            }
        }

        // Interact with assassin
        Assassin assassin = assassinMap.get(entityId);
        if(assassin != null) {
            if (assassin.isEnemy()) {
                assassin.bribe(player.getInventory().numberOfItem("treasure"), true);
            }

            distanceVector = Position.calculatePositionBetween(player.getPosition(), assassin.getPosition());
            distanceBetween = Math.pow((Math.pow(distanceVector.getX(), 2) + Math.pow(distanceVector.getY(), 2)), 0.5);

            if (distanceBetween > 2) {
                throw new InvalidActionException("It's too far from the assassin!");
            } else if (assassin.isEnemy()) {
                if (player.getInventory().numberOfItem("one_ring") > 0) {
                    throw new InvalidActionException("Don't have enough treasure!");
                } else {
                    throw new InvalidActionException("Don't have one ring!");
                }
                
            } else {
                ArrayList<ItemResponse> items = player.getInventory().getItemResponseList();
    
                int numTreasure = 0;
                for (ItemResponse item: items) {
                    if (item.getType().equals("treasure") && numTreasure < 1) {
                        player.getInventory().removeItem(item.getId());
                        numTreasure++;
                    }
                }
            }
        }

        // Interact with zombieToastSpawner
        for (ZombieToastSpawner spawner : zombieSpawnList){
            if (spawner.getId().equals(entityId)) {
                checkValidId = true;
                boolean isAdjacent = false;

                List<Position> adjacent = spawner.getSpawnerPosition().getAdjacentPositions();
                for (Position adjaPosition: adjacent) {
                    if (adjaPosition.equals(playerPosition)) {
                        isAdjacent = true;
                        break;
                    }
                }
                
                if (!isAdjacent){
                    throw new InvalidActionException("It's too far from the spawner!");
                } else if (!hasWeapon()) {
                    throw new InvalidActionException("Can't attack zombie toast spawners without weapons");
                } else {
                    gameMap.removeEntity(spawner.getSpawnerPosition().getX(), spawner.getSpawnerPosition().getY(), spawner.getSpawnerPosition().getLayer());
                    zombieSpawnList.remove(spawner);
                }
                break;
            }
        }
        
        if (!checkValidId) throw new IllegalArgumentException("Entity is not interactable!");

        return makeDungeonResponse();
    }

    /**
     * 
     * @param buildable the type of the item being builded
     * @param buildList current buildable entities list
     * @param newBuild new item being builded as a buildableEntity
     * @param newItem new item being builded as an entity
     * @return returns dungeon response of the map after the new item is builded
     * @throws IllegalArgumentException If buildable is not a bow/shield/sceptre/midnight_armour
     * @throws InvalidActionException If don't have sufficient items to craft the new item
     */
    public DungeonResponse build(String buildable) throws IllegalArgumentException, InvalidActionException {
        
        if (!(buildable.equals("bow") || 
        buildable.equals("shield") || 
        buildable.equals("sceptre") || 
        buildable.equals("midnight_armour"))) {
            throw new IllegalArgumentException(buildable + "Cannot be built!");
        }


        Inventory playerInventory = player.getInventory();

        if (playerInventory.canBuild(buildable, hasZombies())) {
            playerInventory.build(buildable);
        }
        
        return makeDungeonResponse();
    }

    /**
     * should be an observer but helper method for buildables because of lack of time.
     * @return if there are any zombies
     */
    private boolean hasZombies() {
        int counter = 0;
        for (ZombieToast zombie : zombMap.values()) {
            if (zombie != null) counter++;
        }
        return counter > 0;
    }
    
}
