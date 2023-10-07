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
#include "list.h"
#define abbreLEN  2

// TODO: ADD YOUR OWN STRUCTS HERE
typedef struct locationAbbre{
    char *abbre;
}LocationAbbre;

struct gameView {
	int num_turn;
	//Round round;
	//Player player;
	int score;
	int *playerHealth;
	//int visit;
	LocationAbbre *MoveH;
	Map map;
};



int isSpecMove(char *abbrev);
int findCurrPlayer(char currtype);
PlaceId findPlayerLoc(GameView gv, int des_loc);
int diffLastDes(GameView gv, Player player);
int findStart(GameView gv, Player player, int numMoves);
bool vampireOrHunter(GameView gv, Player player, bool rail, Queue queue);
List getLocList(GameView gv, Player player, Round round, PlaceId from, bool road, bool rail, bool boat);
////////////////////////////////////////////////////////////////////////
// Constructor/Destructor

GameView GvNew(char *pastPlays, Message messages[])
{
	
	GameView new = malloc(sizeof(*new));
	if (new == NULL) {
		fprintf(stderr, "Couldn't allocate GameView!\n");
		exit(EXIT_FAILURE);
	}
    
    // initialized the move matrix
    new->num_turn = (strlen(pastPlays) + 1) / 8; 
    int Num_Move = new->num_turn;
    //example: len(pastPlays) = 8 * numturn - 1 (doesn't have " " in last turn)
    Locationabbre *MoveH = malloc(Num_Move * sizeof(Locationabbre));
    for(int i = 0; i < Num_Move; i++) {
        char *abbre = malloc(sizeof(char *));
        MoveH[i].abbre = abbre;
        //strcpy(MoveH[i].abbre, placeIdToAbbrev(NOWHERE));
    }
    
    int *playerHealth = malloc(NUM_PLAYERS * sizeof(int));
    for(int i = 0; i < NUM_PLAYERS; i++) {
        if (i != PLAYER_DRACULA) 
            playerHealth[i] = GAME_START_HUNTER_LIFE_POINTS;
        else
            playerHealth[i] = GAME_START_BLOOD_POINTS ;
    }
    
    // enter the places
    //int currPlayer = -1;
    //Locationabbre *currPlace;
    for (int i = 0; pastPlays[i] != '\0'; i++) {
        /*if (i % 8 == 0) currPlayer = findCurrPlayer(pastPlays[i]);
        else */
        if (i % 8 == 1)  MoveH[i / 8].abbre[0] = pastPlays[i];
        else if (i % 8 == 2)  MoveH[i / 8].abbre[1] = pastPlays[i];
        /*else if (i % 8 == 3) 
        else if (i % 8 == 4) 
        else if (i % 8 == 5) 
        else if (i % 8 == 6) */
        else continue;
        
    }
    new->score = GAME_START_SCORE;
    new->playerHealth = playerHealth;
    new->MoveH = MoveH;
	return new;
}

void GvFree(GameView gv)
{
	
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
    // if player is not start moving
    if (gv->num_turn <= player) return NOWHERE;
    
    //find the destination point in the location array
    int diff = diffLastDes(gv, player);
    if (diff < 0) diff = diff + NUM_PLAYERS;
    int des_loc = gv->num_turn - diff - 1;
    
    // if hunter is reduced to 0 or fewer life points
    if (player != PLAYER_DRACULA) {
        if (GvGetHealth(gv, player) < 0) {
            strcpy(gv->MoveH[des_loc].abbre, "JM");
            return HOSPITAL_PLACE;
        }
    }
    return findPlayerLoc(gv, des_loc);
}

// dracula's job
PlaceId GvGetVampireLocation(GameView gv)
{
	
	return NOWHERE;
}

// dracula's job
PlaceId *GvGetTrapLocations(GameView gv, int *numTraps)
{
	// TODO: REPLACE THIS WITH YOUR OWN IMPLEMENTATION
	*numTraps = 0;
	return NULL;
}

////////////////////////////////////////////////////////////////////////
// Game History

PlaceId *GvGetMoveHistory(GameView gv, Player player,
                          int *numReturnedMoves, bool *canFree)
{
	
	PlaceId *move = malloc((gv->num_turn / NUM_PLAYERS + 1) * sizeof(PlaceId));
	int move_num = 0;
	for (int i = player; i < gv->num_turn; i += 5, move_num++) {
	    move[move_num] = placeAbbrevToId(gv->MoveH[i].abbre);
	}
	*numReturnedMoves = move_num;
	*canFree = true;
	return move;
}

PlaceId *GvGetLastMoves(GameView gv, Player player, int numMoves,
                        int *numReturnedMoves, bool *canFree)
{
	PlaceId *nummove = malloc(numMoves * sizeof(PlaceId));
	int start_move = findStart(gv, player, numMoves);
	int move_num = 0;
	for (int i = start_move; i < gv->num_turn; i += 5, move_num++) {
	    nummove[move_num] = placeAbbrevToId(gv->MoveH[i].abbre);
	}
	*numReturnedMoves = move_num;
	*canFree = true;
    return nummove;
}

PlaceId *GvGetLocationHistory(GameView gv, Player player,
                              int *numReturnedLocs, bool *canFree)
{
	PlaceId *locs = malloc((gv->num_turn / NUM_PLAYERS + 1) * sizeof(PlaceId));
	int locs_num = 0;
	for (int i = player; i < gv->num_turn; i += 5, locs_num++) {
	    locs[locs_num] = findPlayerLoc(gv, i);
	}
	*numReturnedLocs = locs_num;
	*canFree = true;
	return locs;
}

PlaceId *GvGetLastLocations(GameView gv, Player player, int numLocs,
                            int *numReturnedLocs, bool *canFree)
{
	PlaceId *numlocs = malloc(numLocs * sizeof(PlaceId));
	int start_locs = findStart(gv, player, numLocs);
	int locs_num = 0;
	for (int i = start_locs; i < gv->num_turn; i += 5, locs_num++) {
	    numlocs[locs_num] = findPlayerLoc(gv, i);
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
	int depth = 0;
    int j = 0;
    Queue queue = newQueue();
    QueueJoin(queue, from);
    int *visited = malloc(gv->num_turn * sizeof(int));
    for (int i = 0; i < gv->num_turn; i++) visited[i] = UNKNOWN;

    int railDist = 0;
    if (RAIL) railDist = ((player + round) % 4);

    while (depth < round) {
        //array of neighbour
        while (!QueueIsEmpty(queue)) {
            PlaceId currentPlaceId = QueueLeave(queue);
            ConnList connections = MapGetConnections(gv->map, currentPlaceId);
            while (connections != NULL) {
                if (visited[connections->p] == UNKNOWN) {
                    visited[j] = currentPlaceId;
                    j++;
                }
                connections = connections->next;
            }

        }
        // array of neighbour add queue;
        QueueJoin(queue, *visited);
        depth++;
    }

    //return queue;
    return numReturnedLocs;
}

PlaceId *GvGetReachableByType(GameView gv, Player player, Round round,
                              PlaceId from, bool road, bool rail,
                              bool boat, int *numReturnedLocs)
{
    /*
	int depth = 0 ;
    int j = 0 ;
    int move_num = 0;
    Queue queue = newQueue();
    QueueJoin(queue, from);
    int *visited = malloc(gv->num_turn * sizeof(int));
    for (int i = 0; i < gv->num_turn; i++) visited[i] = UNKNOWN;

    int railDist = 0;
    if (RAIL) railDist = ((player + round) % 4);

    while (depth < round) {
        //array of neighbour
        while (!QueueIsEmpty(queue)) {
            PlaceId currentPlaceId = QueueLeave(queue);
            ConnList connections = MapGetConnections(gv->map, currentPlaceId);
            while (connections != NULL) {
                if (visited[connections->p] == UNKNOWN) {
                    if (vampireOrHunter(gv, player, rail, queue)) {
                        visited[j] = currentPlaceId;
                        j++;
                        move_num++;
                    }
                }                
                connections = connections->next;
            }
        }
        // array of neighbour add queue;
        QueueJoin(queue, *visited);
        depth++;
    }

    *numReturnedLocs = move_num;
    //return queue;
    return numReturnedLocs;
    */
   List list =  getLocList();
   *numReturnedLocs = ListLength(list);

   // copy locations in the list to a new array
   placeId *locArray = malloc((List->size)*sizeof(placeId));
   int i = 0;
   for (ListNode node = List->head; node != NULL, node = node->next)
   {
       locArray[i] = node->value;
       i++;
   }

   dropList(list);
   return locArray;

}

////////////////////////////////////////////////////////////////////////

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
int isSpecMove(char *abbrev)
{
    return strcmp("HI", abbrev) == 0 || 
           strcmp("D1", abbrev) == 0 || 
           strcmp("D2", abbrev) == 0 || 
           strcmp("D3", abbrev) == 0 ||
           strcmp("D4", abbrev) == 0 || 
           strcmp("D5", abbrev) == 0 || 
           strcmp("TP", abbrev) == 0;
}

// find the playerloc from the move (recursively)
PlaceId findPlayerLoc(GameView gv, int des_loc)
{
    
    char *currmove = gv->MoveH[des_loc].abbre;
    if (strcmp("HI", currmove) == 0 || strcmp("D1", currmove) == 0) {
        assert(des_loc - 1 >= 0);
        if (isSpecMove(gv->MoveH[des_loc - NUM_PLAYERS].abbre)) 
            return findPlayerLoc(gv, des_loc - NUM_PLAYERS);
        else
            return placeAbbrevToId(gv->MoveH[des_loc - NUM_PLAYERS].abbre);
    } else if (strcmp("D2", currmove) == 0) {
        assert(des_loc - 2  >= 0);
        if (isSpecMove(gv->MoveH[des_loc - 2 * NUM_PLAYERS].abbre)) 
            return findPlayerLoc(gv, des_loc - 2 * NUM_PLAYERS);
        else
            return placeAbbrevToId(gv->MoveH[des_loc - 2 * NUM_PLAYERS].abbre);
    } else if (strcmp("D3", currmove) == 0) {
        assert(des_loc - 3 >= 0);
        if (isSpecMove(gv->MoveH[des_loc - 3 * NUM_PLAYERS].abbre)) 
            return findPlayerLoc(gv, des_loc - 3 * NUM_PLAYERS);
        else
            return placeAbbrevToId(gv->MoveH[des_loc - 3 * NUM_PLAYERS].abbre);
    } else if (strcmp("D4", currmove) == 0) {
        assert(des_loc - 4 >= 0);
        if (isSpecMove(gv->MoveH[des_loc - 4 * NUM_PLAYERS].abbre)) 
            return findPlayerLoc(gv, des_loc - 4 * NUM_PLAYERS);
        else
            return placeAbbrevToId(gv->MoveH[des_loc - 4 * NUM_PLAYERS].abbre);
    } else if (strcmp("D5", currmove) == 0) {
        assert(des_loc - 5 >= 0);
        if (isSpecMove(gv->MoveH[des_loc - 5 * NUM_PLAYERS].abbre)) 
            return findPlayerLoc(gv, des_loc - 5 * NUM_PLAYERS);
        else
            return placeAbbrevToId(gv->MoveH[des_loc - 5 * NUM_PLAYERS].abbre);
    } else if (strcmp("TP", currmove) == 0) {
        return placeAbbrevToId("CD");
    } else {
        return placeAbbrevToId(currmove);
    }

}

// get the diff between last player and the score player
int diffLastDes(GameView gv, Player player)
{
    int lastplayer = GvGetPlayer(gv) - 1;
    if (lastplayer < 0) lastplayer = PLAYER_DRACULA;
    return lastplayer - player;
}

// get the start point for the numMoves or numLocs
int findStart(GameView gv, Player player, int numMoves)
{
    int start_move = gv->num_turn / NUM_PLAYERS - numMoves;
	int diff = diffLastDes(gv, player);
	if (diff >= 0) start_move++;
	return NUM_PLAYERS * start_move + player;
}

bool vampireOrHunter(GameView gv, Player player, bool rail, Queue queue) 
{

    PlaceId currentPlaceId = QueueLeave(queue);
    ConnList connections = MapGetConnections(gv->map, currentPlaceId);
    PlaceId currLocate = GvGetPlayerLocation(gv, player);

    if (
        player == PLAYER_LORD_GODALMING || player == PLAYER_DR_SEWARD ||
        player == PLAYER_VAN_HELSING || player == PLAYER_MINA_HARKER
        ) {
        if (rail && connections->type == RAIL) return true;
    }
    else if (player == PLAYER_DRACULA) {
        if (
            !rail && connections->type != RAIL && 
            currLocate != ST_JOSEPH_AND_ST_MARY
        )  return true;
    }
    return false;
}

List getLocList(GameView gv, Player player, Round round, PlaceId from, bool road, bool rail, bool boat)
{
    List list = newList();
    ListInsert(list,from);

    int railDist = 0;
    if (rail) railDist = ((player + round)) % 4);

    if ((from <= 108 && from >= 100) || from = -1 || from = -2)
    return list;

    if (road) 


}