////////////////////////////////////////////////////////////////////////
// COMP2521 20T2 ... the Fury of Dracula
// GameView.c: GameView ADT implementation
//
// 2014-07-01   v1.0    Team Dracula <cs2521@cse.unsw.edu.au>
// 2017-12-01   v1.1    Team Dracula <cs2521@cse.unsw.edu.au>
// 2018-12-31   v2.0    Team Dracula <cs2521@cse.unsw.edu.au>
// 2020-07-10   v3.0    Team Dracula <cs2521@cse.unsw.edu.au>
//
////////////////////////////////////////////////////////////////////////

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "Game.h"
#include "GameView.h"
#include "Map.h"
#include "Places.h"
// add your own #includes here
#include "string.h"
//#include "Queue.h"
//#include "list.h"
//#include "list.c"

struct gameView {
	int num_turn;
	int score;
	int *playerHealth;
	PlaceId **MoveH;
	//Map map;
	PlaceId vampireLocation;
	PlaceId trapLocations[TRAIL_SIZE]; // Traps information
	int trapNums;
};

void initializeGameview(GameView gv);
void addTrap(GameView gv, int currPlayer, int round);
void addVampire(GameView gv, int currPlayer, int round);
void vampireMature(GameView gv);
void trapBoom(GameView gv);
void isSpacialLocs(GameView gv, int round);
void checkHunterHealth(GameView gv, Player currPlayer);
void encounterD(GameView gv, Player currPlayer);
void encounterV(GameView gv);
void encounterT(GameView gv, int currPlayer, int round);
void checkHHealthEnd(GameView gv, int currPlayer, int round);
int findLastRound(GameView gv, Player player);
int isSpecMove(PlaceId currmove);
int findCurrPlayer(char currtype);
PlaceId findPlayerLoc(PlaceId *MoveH, int des_loc);
int diffLastDes(GameView gv, Player player);
int findStart(GameView gv, Player player, int numMoves);
void hunterRest(GameView gv, int round, int currPlayer);
//List getLocList(GameView gv, Player player, Round round, PlaceId from);
//List getLocListByType(GameView gv, Player player, Round round, PlaceId from, bool road, bool rail, bool boat);


////////////////////////////////////////////////////////////////////////
// Constructor/Destructor

GameView GvNew(char *pastPlays, Message messages[])
{
	
	GameView new = malloc(sizeof(*new));
	if (new == NULL) {
		fprintf(stderr, "Couldn't allocate GameView!\n");
		exit(EXIT_FAILURE);
	}
    
    new->num_turn = (strlen(pastPlays) + 1) / 8; 
    initializeGameview(new);
    
	int len = strlen(pastPlays);
	// pos: To locate the index in the pastPlay[]
    for (int pos = 0; pos < len; pos += 8) {
        Player currPlayer = findCurrPlayer(pastPlays[pos]);
        int round = pos / (NUM_PLAYERS * 8);
        char abbre[3] = "";
        strncpy(abbre, pastPlays + pos + 1, 2);
        new->MoveH[currPlayer][round] = placeAbbrevToId(abbre);

        //  =============================================  //
		//  ========        DRACULA's turn       ========  //
		//  =============================================  //  
		if(currPlayer == PLAYER_DRACULA) {

			/** The game score lost when Dracula makes a turn. */
			new->score -= SCORE_LOSS_DRACULA_TURN;

			/* if dracula add trap */
            char trapFlag = pastPlays[pos + 3];
			if(trapFlag == 'T') addTrap(new, currPlayer, round);
            /* if dracula add vampire */
			char vampireFlag = pastPlays[pos + 4];
			if(vampireFlag == 'V') addVampire(new, currPlayer, round);
			/* if vampire or trap after 6 round*/	
			char actionFlag = pastPlays[pos + 5];
            if(actionFlag == 'V') vampireMature(new);
			else if(actionFlag == 'M') trapBoom(new);      

            // Current Location is Special Situations: CASTLE, SEA....//
			isSpacialLocs(new, round);
		} else {
		
		//  =============================================  //
		//  ========        Hunter's turn        ========  //
		//  =============================================  //
		    // if player health is zero, restore the health 
		    
		    checkHunterHealth(new, currPlayer);
		   // 
	        
	        // Skip the fisrt 3 chars -> name(1) + LocationID(2)
	        for(int actPos = 3; actPos < 7; actPos++) {
	            char actFlag = pastPlays[pos + actPos];
	            //printf("....................%d ==== player %d\n", new->playerHealth[0], currPlayer);
	            if(actFlag == 'D') encounterD(new, currPlayer);
			    else if(actFlag == 'V') encounterV(new);
				else if(actFlag == 'T') encounterT(new, currPlayer, round);
				else if(actFlag == '.') break;
				
			}
			// if hunter rest
			hunterRest(new, round, currPlayer);
			checkHHealthEnd(new, currPlayer, round);
        }
        
    }

    
    
    
	return new;
}

void GvFree(GameView gv)
{
	for (int player = PLAYER_LORD_GODALMING; player < NUM_PLAYERS; player++) {
        free(gv->MoveH[player]);
    }
    free(gv->MoveH);
    free(gv->playerHealth);
    free(gv);
}

////////////////////////////////////////////////////////////////////////
// Game State Information

Round GvGetRound(GameView gv)
{
	return gv->num_turn / NUM_PLAYERS;
}

Player GvGetPlayer(GameView gv)
{
	int turn = gv->num_turn % NUM_PLAYERS;
	if (turn == 0) return PLAYER_LORD_GODALMING;
	else if (turn == 1) return PLAYER_DR_SEWARD;
	else if (turn == 2) return PLAYER_VAN_HELSING;
	else if (turn == 3) return PLAYER_MINA_HARKER;
	else return PLAYER_DRACULA;

}

int GvGetScore(GameView gv)
{
	return gv->score;
}

int GvGetHealth(GameView gv, Player player)
{
	return gv->playerHealth[player];
}

PlaceId GvGetPlayerLocation(GameView gv, Player player)
{
    // find player's last move 
    int round = findLastRound(gv, player);
    if (player != PLAYER_DRACULA) return gv->MoveH[player][round];
    assert(player == PLAYER_DRACULA);
    return findPlayerLoc(gv->MoveH[player], round);
}

// dracula's job
PlaceId GvGetVampireLocation(GameView gv)
{
	return gv->vampireLocation;
}

// dracula's job
PlaceId *GvGetTrapLocations(GameView gv, int *numTraps)
{
	
	*numTraps = gv->trapNums;
	PlaceId *trapLocations = malloc(sizeof(PlaceId) * TRAIL_SIZE);
	// Store the gv->trapLocations -> trapLocations and return it.
	memcpy(trapLocations, gv->trapLocations, sizeof(PlaceId) * TRAIL_SIZE);
	return trapLocations;
}

////////////////////////////////////////////////////////////////////////
// Game History

PlaceId *GvGetMoveHistory(GameView gv, Player player,
                          int *numReturnedMoves, bool *canFree)
{
	int round = findLastRound(gv, player) + 1;
	PlaceId *move = malloc(round * sizeof(PlaceId));
	memcpy(move, gv->MoveH[player], round * sizeof(PlaceId));
	*numReturnedMoves = round;
	*canFree = true;
	return move;
}

PlaceId *GvGetLastMoves(GameView gv, Player player, int numMoves,
                        int *numReturnedMoves, bool *canFree)
{
	int round = findLastRound(gv, player) + 1;
	
	PlaceId *nummove = malloc(numMoves * sizeof(PlaceId));
	int start_move = round - numMoves;
	if (start_move < 0) start_move = 0;
	int move_num = 0;
	for (int i = start_move; i < round; i++, move_num++) {
	    nummove[move_num] = gv->MoveH[player][i];
	}
	*numReturnedMoves = move_num;
	*canFree = true;
    return nummove;
}

PlaceId *GvGetLocationHistory(GameView gv, Player player,
                              int *numReturnedLocs, bool *canFree)
{
	int round = findLastRound(gv, player);
	round++;
	PlaceId *locs = malloc((gv->num_turn / NUM_PLAYERS + 1) * sizeof(PlaceId));
	int locs_num = 0;
	for (locs_num = 0; locs_num < round; locs_num++) {
	    locs[locs_num] = findPlayerLoc(gv->MoveH[player], locs_num);
	}
	*numReturnedLocs = locs_num;
	*canFree = true;
	return locs;
}

PlaceId *GvGetLastLocations(GameView gv, Player player, int numLocs,
                            int *numReturnedLocs, bool *canFree)
{
	int round = findLastRound(gv, player);
	round++;
	PlaceId *numlocs = malloc(numLocs * sizeof(PlaceId));
	int start_locs = round - numLocs;
	int locs_num = 0;
	for (int i = start_locs; i < round; i++, locs_num++) {
	    numlocs[locs_num] = findPlayerLoc(gv->MoveH[player], i);
	}
	*numReturnedLocs = locs_num;
	*canFree = true;
    return numlocs;
}

////////////////////////////////////////////////////////////////////////
// Making a Move

PlaceId *GvGetReachable(GameView gv, Player player, Round round,
                        PlaceId from, int *numReturnedLocs)
{

#if 0
    List list =  getLocList(gv,player,round,from);
    *numReturnedLocs = ListLength(list);

    // copy locations in the list to a new array
    PlaceId *locArray = malloc((list->size)*sizeof(PlaceId));
    int i = 0;
    for (ListNode *node = list->first; node != NULL; node = node->next)
    {
        locArray[i] = node->value;
        i++;
    }

    dropList(list);
    return locArray;
#else
    *numReturnedLocs = 0;
	return NULL;

#endif
}

PlaceId *GvGetReachableByType(GameView gv, Player player, Round round,
                              PlaceId from, bool road, bool rail,
                              bool boat, int *numReturnedLocs)
{
#if 0
    List list =  getLocListByType(gv,player,round,from,road,rail,boat);
    *numReturnedLocs = ListLength(list);

    // copy locations in the list to a new array
    PlaceId *locArray = malloc((list->size)*sizeof(PlaceId));
    int i = 0;
    for (ListNode *node = list->first; node != NULL; node = node->next)
    {
        locArray[i] = node->value;
        i++;
    }

    dropList(list);
    return locArray;

#else
    *numReturnedLocs = 0;
	return NULL;
#endif
}

////////////////////////////////////////////////////////////////////////
// initialized all structure
void initializeGameview(GameView gv)
{
    // initialized the move history structure
    PlaceId **MoveH = malloc(NUM_PLAYERS * sizeof(PlaceId *));
    int currround = gv->num_turn + 1;
    for (int player = PLAYER_LORD_GODALMING; player < NUM_PLAYERS; player++) {
        MoveH[player] = calloc(currround, sizeof(PlaceId));
        assert(MoveH[player] != NULL);
            for (int move_num = 0; move_num < currround; move_num++) {
                // initialize all move history to nowhere
                MoveH[player][move_num] = placeAbbrevToId("NW");
            }
    }
    
    // initialized every player's health
    int *playerHealth = malloc(NUM_PLAYERS * sizeof(int));
    for(int i = 0; i < NUM_PLAYERS - 1; i++) {
        playerHealth[i] = GAME_START_HUNTER_LIFE_POINTS;
    }
    playerHealth[PLAYER_DRACULA] = GAME_START_BLOOD_POINTS ;
    //Map map = MapNew();
    // initialized other infomation
    gv->vampireLocation = NOWHERE;
    gv->score = GAME_START_SCORE;
    gv->trapNums = 0;
    gv->playerHealth = playerHealth;
    gv->MoveH = MoveH;
    //gv->map = map;
}

// when dracula want to add a trap
void addTrap(GameView gv, int currPlayer, int round)
{
    gv->trapLocations[gv->trapNums] = gv->MoveH[currPlayer][round];
	gv->trapNums++;
}
// when dracula want to add a vampire

void addVampire(GameView gv, int currPlayer, int round)
{
    gv->vampireLocation = gv->MoveH[currPlayer][round];
}

// when vampire matures
void vampireMature(GameView gv)
{
    gv->score -= SCORE_LOSS_VAMPIRE_MATURES;
	gv->vampireLocation = NOWHERE;
}

void trapBoom(GameView gv)
{
    int trapIdx = 0;
    while (trapIdx < gv->trapNums - 1) {
        gv->trapLocations[trapIdx] = gv->trapLocations[trapIdx + 1];
        trapIdx ++;
    }
	gv->trapNums --;
}

void isSpacialLocs(GameView gv, int round)
{
    PlaceId placeDracula = findPlayerLoc(gv->MoveH[PLAYER_DRACULA], round);
	if(placeDracula == CASTLE_DRACULA) {
    	/** Blood points gained when Dracula is at Castle Dracula. */
	    gv->playerHealth[PLAYER_DRACULA] += LIFE_GAIN_CASTLE_DRACULA;
	} else if(placeIdToType(placeDracula) == SEA) {
		/** Blood points lost when Dracula is at sea. */
		gv->playerHealth[PLAYER_DRACULA] -= LIFE_LOSS_SEA;
	}
}

void checkHunterHealth(GameView gv, Player currPlayer)
{
    if (gv->playerHealth[currPlayer] == 0) 
        gv->playerHealth[currPlayer] = GAME_START_HUNTER_LIFE_POINTS;
}

void encounterD(GameView gv, Player currPlayer)
{
    /** Life points lost when hunter encounters Dracula. */
	gv->playerHealth[currPlayer] -= LIFE_LOSS_DRACULA_ENCOUNTER;
	/** Blood points lost when Dracula encounters a hunter. */
	gv->playerHealth[PLAYER_DRACULA] -= LIFE_LOSS_HUNTER_ENCOUNTER;
}

void encounterV(GameView gv)
{
    gv->vampireLocation = NOWHERE;
}

void encounterT(GameView gv, int currPlayer, int round)
{
    //printf(">>>>>>%d ==== player %d\n", gv->playerHealth[currPlayer], currPlayer);
    // If a trap is encountered, the hunter loses 2 life points
	gv->playerHealth[currPlayer] -= LIFE_LOSS_TRAP_ENCOUNTER;
	//printf("**%d ==== player %d\n", gv->playerHealth[currPlayer], currPlayer);
    // Update TRAP information
	int trapIdx = 0;
	while (trapIdx < gv->trapNums) {
    // boom!
	    if(gv->trapLocations[trapIdx] == gv->MoveH[currPlayer][round]) {
			break;
		}
		trapIdx++;
	}
    while (trapIdx < gv->trapNums - 1) {
        // If a trap is encountered, curent gone...move to the next trap
        gv->trapLocations[trapIdx] = gv->trapLocations[trapIdx + 1];
        trapIdx++;
    }
    // If a trap is encountered, the trap is destroyed.
    gv->trapNums --;
}

void checkHHealthEnd(GameView gv, int currPlayer, int round)
{
    if(gv->playerHealth[currPlayer] <= 0) {
       	//playerLocation[PLAYER_DRACULA] = playerLocation[currPlayer]; //?
		gv->MoveH[currPlayer][round] = HOSPITAL_PLACE;
		gv->playerHealth[currPlayer] = 0;
		/** The game score lost when a hunter 'dies',
		*  and is teleported to the hospital. */
	    gv->score -= SCORE_LOSS_HUNTER_HOSPITAL;
	}
}

void hunterRest(GameView gv, int round, int currPlayer)
{
    if (round > 1) {
	int pLocationLast = gv->MoveH[currPlayer][round - 1];
	int pLocationCurrent = gv->MoveH[currPlayer][round];

	    if (pLocationCurrent == pLocationLast) {
		    // Hunter Rest        
	        if (gv->playerHealth[currPlayer] < 9) {
                gv->playerHealth[currPlayer] += LIFE_GAIN_REST;
                if (gv->playerHealth[currPlayer] >= 9) {
                    gv->playerHealth[currPlayer] = GAME_START_HUNTER_LIFE_POINTS;
                }
            }    
	    }
    }
}

// find player's last move round number
int findLastRound(GameView gv, Player player)
{
    int round = GvGetRound(gv);
    if (gv->num_turn < 5) return round;
    if ((gv->num_turn % NUM_PLAYERS) == 0) return round - 1;
    // if player's last move round number
    if (player > GvGetPlayer(gv) - 1) round = round - 1;
    return round;
}

// find the player from trail
int findCurrPlayer(char currtype)
{
    int currPlayer = -1;
    if (currtype == 'G') currPlayer = PLAYER_LORD_GODALMING;
    if (currtype == 'S') currPlayer = PLAYER_DR_SEWARD;
    if (currtype == 'H') currPlayer = PLAYER_VAN_HELSING;
    if (currtype == 'M') currPlayer = PLAYER_MINA_HARKER;
    if (currtype == 'D') currPlayer = PLAYER_DRACULA;
    return currPlayer;
}

// check whether the move is special
int isSpecMove(PlaceId currmove)
{
    return currmove == placeAbbrevToId("HI") || 
           currmove == placeAbbrevToId("D1") || 
           currmove == placeAbbrevToId("D2") ||
           currmove == placeAbbrevToId("D3") ||
           currmove == placeAbbrevToId("D4") || 
           currmove == placeAbbrevToId("D5") || 
           currmove == placeAbbrevToId("TP");
}

// find the playerloc from the move (recursively)
PlaceId findPlayerLoc(PlaceId *playerMoveH, int des_loc)
{
    
    PlaceId currmove = playerMoveH[des_loc];
    if (!isSpecMove(currmove)) {
        return currmove;
    } else if (currmove ==  placeAbbrevToId("TP")) {
        return placeAbbrevToId("CD");
    } else if (currmove == placeAbbrevToId("HI") || currmove ==  placeAbbrevToId("D1")) {
        assert(des_loc - 1 >= 0);
        if (isSpecMove(playerMoveH[des_loc - 1]))
            return findPlayerLoc(playerMoveH, des_loc - 1);
        else
            return playerMoveH[des_loc - 1];
    } else if (currmove ==  placeAbbrevToId("D2")) {
        assert(des_loc - 2  >= 0);
        if (isSpecMove(playerMoveH[des_loc - 2])) 
            return findPlayerLoc(playerMoveH, des_loc - 2);
        else
            return playerMoveH[des_loc - 2];
    } else if (currmove ==  placeAbbrevToId("D3")) {
        assert(des_loc - 3 >= 0);
        if (isSpecMove(playerMoveH[des_loc - 3])) 
            return findPlayerLoc(playerMoveH, des_loc - 3);
        else
            return playerMoveH[des_loc - 3];
    } else if (currmove ==  placeAbbrevToId("D4")) {
        assert(des_loc - 4 >= 0);
        if (isSpecMove(playerMoveH[des_loc - 4])) 
            return findPlayerLoc(playerMoveH, des_loc - 4);
        else
            return playerMoveH[des_loc - 4];
    } else if (currmove ==  placeAbbrevToId("D5")) {
        assert(des_loc - 5 >= 0);
        if (isSpecMove(playerMoveH[des_loc - 5])) 
            return findPlayerLoc(playerMoveH, des_loc - 5);
        else
            return playerMoveH[des_loc - 5];
    } 
    return NOWHERE;
}

#if 0
List getLocList(GameView gv, Player player, Round round, PlaceId from)
{
    List list = newList();
    ListInsert(list,from);

    ConnList connections = MapGetConnections(gv->map, from);

    int railDist = 0;
        railDist = ((player + round) % 4);

    if (player == PLAYER_DRACULA)
    {
        if (ListSearch(list, ST_JOSEPH_AND_ST_MARY) != NULL)
        ListDelete(list, ST_JOSEPH_AND_ST_MARY);
        
        for (ListNode *node = list->first; node != NULL; node = node->next)
        {
            if (connections->type = RAIL) ListDelete(list, connections->p);
        }
    }

    // implementation specified to rail 
    if (player != PLAYER_DRACULA) 
    {
        if (railDist == 0)      // same return as dracula
        {
            insertReachable(list,from);
        }
        else if (railDist >= 1) 
        {
            while (connections != NULL)
            {
                insertReachable(list,connections->p);
                connections = connections->next;
            }
            if (railDist >= 2) 
            {
                List railList = newList();
                findRailList(gv,railList, from);
                List railList2 = newList();
                for (ListNode *curr = railList->first; curr != NULL; curr = curr->next) 
                {
                    findRailList(gv,railList2, curr);
                }
                while (railList2->railBranch != NULL)
                {
                insertReachable(list, railList2->railBranch->value);
                railList2->railBranch = railList2->railBranch->next;
                }
            }
            if (railDist == 3) 
            {
                List railList3 = newList();
                for (ListNode *curr = railList3->first; curr != NULL; curr = curr->next) 
                {
                    findRailList(gv,railList3, curr->value);
                }
                while (railList3->railBranch != NULL)
                {
                insertReachable(list, railList3->railBranch->value);
                railList3->railBranch = railList3->railBranch->next;
                }
            }
        }
    }
    return list;
    /*
    int railDist = 0;
    railDist = ((player + round) % 4);
    switch (from)
    {
		case CITY_UNKNOWN:  
		case SEA_UNKNOWN:   
		case HIDE:         
		case DOUBLE_BACK_1: 
		case DOUBLE_BACK_2: 
		case DOUBLE_BACK_3: 
		case DOUBLE_BACK_4: 
		case DOUBLE_BACK_5: 
		case TELEPORT:                
        return list;
    }
    insertReachable(list, from);
    if (connections->type = RAIL) // cannot use above function due to rail distance limit 
    {
        List railList = newList();
        ListInsert(railList,from);
        PlaceId *railArray;
        int railNum = 1;
        for (int i = 0; i < railDist; i++)
        {
            railNum = ListLength(railList);
            railArray = listToArray(railList);
            for (int j = 0; j < railNum; j++)
            {
                insertReachable(list, railArray[j]);
            }
            free(railArray);
        }
        railArray = listToArray(railList);
        for (int k = 0; k < ListLength(railList); k++) ListInsert(list, railArray[k]);
        dropList(railList);
    }
    if (player = PLAYER_DRACULA)
    {
        if (ListSearch(list, ST_JOSEPH_AND_ST_MARY) != NULL)
        ListDelete(list, ST_JOSEPH_AND_ST_MARY);
    }
    */

}

List getLocListByType(GameView gv, Player player, Round round, PlaceId from, bool road, bool rail, bool boat)
{
    List list = newList();
    ListInsert(list,from);

    int railDist = 0;
    if (rail)   railDist = ((player + round) % 4);

    switch (from) {
		case CITY_UNKNOWN:  
		case SEA_UNKNOWN:   
		case HIDE:         
		case DOUBLE_BACK_1: 
		case DOUBLE_BACK_2: 
		case DOUBLE_BACK_3: 
		case DOUBLE_BACK_4: 
		case DOUBLE_BACK_5: 
		case TELEPORT:                
        return list;

    if (road) insertByType(list, ROAD, from);
    if (boat) insertByType(list, BOAT, from);

    if (rail) // cannot use above function due to rail distance limit 
    {
        List railList = newList();
        ListInsert(railList,from);

        PlaceId *railArray;
        int railNum = 1;
        for (int i = 0; i < railDist; i++)
        {
            railNum = ListLength(railList);
            railArray = listToArray(railList);
            for (int j = 0; j < railNum; j++)
            {
                insertByType(list,rail,railArray[j]);
            }
            free(railArray);
        }
        railArray = listToArray(railList);

        for (int k = 0; k < ListLength(railList); k++) ListInsert(list, railArray[k]);
        dropList(railList);
    }

    if (player = PLAYER_DRACULA)
    {
        if (ListSearch(list, ST_JOSEPH_AND_ST_MARY) != NULL)
        ListDelete(list, ST_JOSEPH_AND_ST_MARY);
    }

    return list;
}

void findRailList(GameView gv, List railList, PlaceId from)
{
    ConnList connections = MapGetConnections(gv->map,from);
    for (ConnList curr = connections; curr != NULL; curr = curr->next) {
        if (curr->type == RAIL) {
            Listinsert(railList, curr->p);
        }
    }
}
#endif
