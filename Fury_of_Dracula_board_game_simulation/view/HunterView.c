////////////////////////////////////////////////////////////////////////
// COMP2521 20T2 ... the Fury of Dracula
// HunterView.c: the HunterView ADT implementation
//
// 2014-07-01	v1.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2017-12-01	v1.1	Team Dracula <cs2521@cse.unsw.edu.au>
// 2018-12-31	v2.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2020-07-10   v3.0    Team Dracula <cs2521@cse.unsw.edu.au>
//
////////////////////////////////////////////////////////////////////////

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "Game.h"
#include "GameView.h"
#include "HunterView.h"
#include "Map.h"
#include "Places.h"

// add your own #includes here
#include "Queue.h"

struct hunterView {
	GameView g;
};

////////////////////////////////////////////////////////////////////////
// Constructor/Destructor

// initialize
HunterView HvNew(char *pastPlays, Message messages[])
{
	assert(pastPlays != NULL);
	assert(messages != NULL);

	HunterView new = malloc(sizeof(*new));
	if (new == NULL) {
		fprintf(stderr, "Couldn't allocate HunterView!\n");
		exit(EXIT_FAILURE);
	}

	new->g = GvNew(pastPlays, messages);

	return new;
}
// free
void HvFree(HunterView hv)
{
	assert(hv != NULL);
   	return GvFree(hv->g);
}

////////////////////////////////////////////////////////////////////////
// Game State Information

// get round
Round HvGetRound(HunterView hv)
{
	assert(hv != NULL);
	return GvGetRound(hv->g);
}

// get player
Player HvGetPlayer(HunterView hv)
{
	assert(hv != NULL);
	return GvGetPlayer(hv->g);
}

// get score
int HvGetScore(HunterView hv)
{
	assert(hv != NULL);
	return GvGetScore(hv->g);
}

// get health
int HvGetHealth(HunterView hv, Player player)
{
	assert(hv != NULL);
	return GvGetHealth(hv->g, player);
}

// get given player's location
PlaceId HvGetPlayerLocation(HunterView hv, Player player)
{
	assert(hv != NULL);
	return GvGetPlayerLocation(hv->g, player);
}

// get vampire location
PlaceId HvGetVampireLocation(HunterView hv)
{
	assert(hv != NULL);
	return GvGetVampireLocation(hv->g);
}

////////////////////////////////////////////////////////////////////////
// Utility Functions

// get dracula's last known location
PlaceId HvGetLastKnownDraculaLocation(HunterView hv, Round *round)
{
	assert(hv != NULL);
	// basic initialization
	PlaceId site = NOWHERE;
	int numReturnedLocs = -1;
	bool canFree = false;
	*round = HvGetRound(hv);

	// get trail that is dracula's location history
	PlaceId *trail = malloc((*round + 1) * sizeof(PlaceId));
	trail = GvGetLocationHistory(hv->g, PLAYER_DRACULA, &numReturnedLocs, &canFree);

	// iterate through trail and find last real revaled location
	for (int i = 0; i < numReturnedLocs; i++) {
		// exclude CITY_UNKNOWN and SEA_UNKNOWN 
		if (trail[i] != CITY_UNKNOWN && trail[i] != SEA_UNKNOWN) {
			site = trail[i];
			*round = i % 5;
		}
	}
	
	return site;
}

PlaceId *HvGetShortestPathTo(HunterView hv, Player hunter, PlaceId dest,
                             int *pathLength)
{
	assert(hv != NULL);
	// playter cannot be dracula
	assert(hunter != PLAYER_DRACULA);

	// basic initialization
	Round round = HvGetRound(hv);
	int numReturnedLocs = -1;
	PlaceId *path = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// mark current location as src
	PlaceId src = HvGetPlayerLocation(hv, hunter);

	// find pathLength and path that includes current location
	pathLength = findPath (hv, src, dest, numReturnedLocs, path, round, hunter);

	// find final path array
	PlaceId *Path = finalPath(path, *pathLength);
	
	return Path;
}

////////////////////////////////////////////////////////////////////////
// Making a Move

PlaceId *HvWhereCanIGo(HunterView hv, int *numReturnedLocs)
{
	
	assert(hv != NULL);
	// basic initialization
 	Player player = HvGetPlayer(hv);
 	// this is hunter's turn, player cannot be dracula
 	assert(player != PLAYER_DRACULA);
	Round round = HvGetRound(hv);
	// set site as current hunter's location
	PlaceId site = HvGetPlayerLocation(hv, player);
	// if current player hasn't made a move yet
 	if (site == NOWHERE) {
		*numReturnedLocs = 0;
		return NULL;
	}
 
	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// first term of new array shold be current location
	new[0] = site;
 	
 	PlaceId *where = GvGetReachable(hv->g, player, round, site, numReturnedLocs);
 	
 	// assign value to new array
 	for (int i = 1; i < *numReturnedLocs; i++) {
 		new[i] = where[i - 1];
 	}

 	return new;
	
}

PlaceId *HvWhereCanIGoByType(HunterView hv, bool road, bool rail,
                             bool boat, int *numReturnedLocs)
{
	assert(hv != NULL);
	// basic initialization
 	Player player = HvGetPlayer(hv);
 	// this is hunter's turn, player cannot be dracula
 	assert(player != PLAYER_DRACULA);
 	Round round = HvGetRound(hv);
 	// set site as current hunter's location
 	PlaceId site = HvGetPlayerLocation(hv, player);
 	// if current player hasn't made a move yet
 	if (site == NOWHERE) {
		*numReturnedLocs = 0;
		return NULL;
	}

 	PlaceId *where = GvGetReachableByType(hv->g, player, round, site, road, rail, boat, numReturnedLocs);
 	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
 	// first term of new array shold be current location
 	new[0] = site;

 	// assign value to new array
 	for (int i = 1; i < *numReturnedLocs; i++) {
 		new[i] = where[i - 1];
 	}

	return new;
}

PlaceId *HvWhereCanTheyGo(HunterView hv, Player player,
                          int *numReturnedLocs)
{
	
	assert(hv != NULL);
	// basic initialization
 	Round round = HvGetRound(hv);
 	// set site as current hunter's location
 	PlaceId site = HvGetPlayerLocation(hv, player);
 	// if current player hasn't made a move yet
 	// or if player is dracula and current location is not revealed
 	if (site == NOWHERE || site == CITY_UNKNOWN || site == SEA_UNKNOWN) {
		*numReturnedLocs = 0;
		return NULL;
	}

	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// first term of new array shold be current location
 	new[0] = site;

 	// assign value to new array
	if (player == PLAYER_DRACULA) {
		PlaceId *where = GvGetReachable(hv->g, player, round, site, numReturnedLocs);
	 	for (int i = 1; i < *numReturnedLocs; i++) {
	 		// if player is dracula
	 		// location cannot be hospital
	 		if (where[i - 1] != ST_JOSEPH_AND_ST_MARY) new[i] = where[i - 1];
	 	}
 	}
 	else {
 		round++;
 		PlaceId *where = GvGetReachable(hv->g, player, round, site, numReturnedLocs);
 		// assign value to new array
 		for (int i = 1; i < *numReturnedLocs; i++) {
 			new[i] = where[i - 1];
 		}
 	}

 	return new;
}

PlaceId *HvWhereCanTheyGoByType(HunterView hv, Player player,
                                bool road, bool rail, bool boat,
                                int *numReturnedLocs)
{
	assert(hv != NULL);
	// basic initialization
 	Round round = HvGetRound(hv);
 	// set site as current hunter's location
 	PlaceId site = HvGetPlayerLocation(hv, player);
 	// if current player hasn't made a move yet
 	// or if player is dracula and current location is not revealed
 	if (site == NOWHERE || site == CITY_UNKNOWN || site == SEA_UNKNOWN) {
		*numReturnedLocs = 0;
		return NULL;
	}

 	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
 	// first term of new array shold be current location
 	new[0] = site;

 	// assign value to new array
 	if (player == PLAYER_DRACULA) {
 		PlaceId *where = GvGetReachableByType(hv->g, player, round, site, road, rail, boat, numReturnedLocs);
	 	for (int i = 1; i < *numReturnedLocs; i++) {
	 		// if player is dracula
	 		// location cannot be hospital
	 		if (where[i - 1] != ST_JOSEPH_AND_ST_MARY) new[i] = where[i - 1];
	 	}
 	}
 	else {
		round++;
 		PlaceId *where = GvGetReachableByType(hv->g, player, round, site, road, rail, boat, numReturnedLocs);
 		// assign value to new array
 		for (int i = 1; i < *numReturnedLocs; i++) {
 			new[i] = where[i - 1];
 		}
 	}

	return new;
}

////////////////////////////////////////////////////////////////////////
// Your own interface functions

// find pathLength and path that includes src using bfs
int *findPath (HunterView hv, PlaceId src, PlaceId dest, int numReturnedLocs,
				   PlaceId *path, Round round, Player player) 
{
	assert(hv != NULL);
	// basic initialization
	Queue q = newQueue();
	QueueJoin(q, src);
	int *visited = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);

	// find source and mark it as 1
	for (int i = 0; i < numReturnedLocs; i++) {
		if (i == src) visited[i] = 0;
		else visited[i] = -1;
	}
	// previous place
	PlaceId *father= malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// check if source is reachable
	bool reachable = canReach(hv, round, player, src, numReturnedLocs);

	while (!QueueIsEmpty(q)) {
		PlaceId currPlace = QueueLeave(q);
		// check if it has been found
		if (currPlace == dest) {
			// add path
			PlaceId curr = currPlace;
			PlaceId i = visited[currPlace];
			// assign value to path
			while (i > 0) {
				// put cur to specific position in path
				path[i - 1] = curr;
				// go to pre one
				curr = father[curr];
				i--;
			}
			return &visited[currPlace];
		}
		for (int i = 0; i < numReturnedLocs; i++) {
			// if visited > -1, that means its already been added
			// src should be reachable
			if (visited[i] == -1 && reachable) {
				visited[i] = visited[currPlace] +1;
				father[i] = currPlace;
				// add it to q
				QueueJoin(q,i);
			}
		}
	}
	return 0;
}

// check if source is reachable
bool canReach (HunterView hv, Round round, Player player, PlaceId src, int numReturnedLocs)
{
	PlaceId *reach = GvGetReachable(hv->g, player, round, src, &numReturnedLocs);

	// iterate through *reach
	for (int i = 0; i < numReturnedLocs; i++) {
		// if find source, mark it as true
		// else, false
		if (reach[i] == src) return true;
	}
	return false;
}

// final path array which do not includes current location
PlaceId *finalPath (PlaceId *path, int len) 
{
	assert(path != 0);
	PlaceId *newPath = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);

	// assgin value to newPath except for current location
	for (int i = 1; i < len; i++) {
		newPath[i - 1] = path[i];
	}

	return newPath;
}
