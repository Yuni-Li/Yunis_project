////////////////////////////////////////////////////////////////////////
// COMP2521 20T2 ... the Fury of Dracula
// DraculaView.c: the DraculaView ADT implementation
//
// 2014-07-01	v1.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2017-12-01	v1.1	Team Dracula <cs2521@cse.unsw.edu.au>
// 2018-12-31	v2.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2020-07-10	v3.0	Team Dracula <cs2521@cse.unsw.edu.au>
//
////////////////////////////////////////////////////////////////////////

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "DraculaView.h"
#include "Game.h"
#include "GameView.h"
#include "Map.h"
// add your own #includes here

#define NOTRAP 0;

// TODO: ADD YOUR OWN STRUCTS HERE

struct draculaView 
{
	GameView view;
};

////////////////////////////////////////////////////////////////////////
// Constructor/Destructor

// ongoing
DraculaView DvNew(char *pastPlays, Message messages[])
{
	assert(pastPlays != NULL);
	assert(messages != NULL);

	DraculaView new_dv = malloc(sizeof(*new_dv));
	if (new_dv == NULL) {
		fprintf(stderr, "Couldn't allocate DraculaView\n");
		exit(EXIT_FAILURE);
	}

	new_dv->view = GvNew(pastPlays, messages);

	return new_dv;
}

void DvFree(DraculaView dv)
{
	assert(dv != NULL);
	return GvFree(dv->view);
}

////////////////////////////////////////////////////////////////////////
// Game State Information

// done
Round DvGetRound(DraculaView dv)
{
	assert(dv != NULL);
	return GvGetRound(dv->view);
}

// done
int DvGetScore(DraculaView dv)
{
	assert(dv != NULL);
	return GvGetScore(dv->view);
}

// done
int DvGetHealth(DraculaView dv, Player player)
{
	assert(dv != NULL);
	return GvGetHealth(dv->view, player);
}

// done
PlaceId DvGetPlayerLocation(DraculaView dv, Player player)
{
	assert(dv != NULL);
	return GvGetPlayerLocation(dv->view, player);
}

// still ongoing, associate with gv
PlaceId DvGetVampireLocation(DraculaView dv)
{
	assert(dv != NULL);
	return GvGetVampireLocation(dv->view);
}

// still ongoing, associate with gv
PlaceId *DvGetTrapLocations(DraculaView dv, int *numTraps)
{
	assert(dv != NULL && *numTraps <= 3);
	return GvGetTrapLocations(dv->view, numTraps);
}

////////////////////////////////////////////////////////////////////////
// Making a Move

PlaceId *DvGetValidMoves(DraculaView dv, int *numReturnedMoves)
{
	// TODO: REPLACE THIS WITH YOUR OWN IMPLEMENTATION
	*numReturnedMoves = 0;
	return NULL;
}

PlaceId *DvWhereCanIGo(DraculaView dv, int *numReturnedLocs)
{
	assert(dv != NULL);
	// basic initialization
 	Player player = GvGetPlayer(dv->view);
 	// this is dracula's turn, player cannot be hunter
 	assert(player != PLAYER_MINA_HARKER || player != PLAYER_LORD_GODALMING ||
 		   player != PLAYER_DR_SEWARD || player != PLAYER_VAN_HELSING);
	Round round = DvGetRound(dv);
	// set site as current dracula's location
	PlaceId site = DvGetPlayerLocation(dv, player);
	// if current player hasn't made a move yet
 	if (site == NOWHERE) {
		*numReturnedLocs = 0;
		return NULL;
	}

	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// first term of new array shold be current location
	new[0] = site;
 	
 	PlaceId *where = GvGetReachable(dv->view, player, round, site, numReturnedLocs);

 	// ***validmove
 	// assign value to new array
 	for (int i = 1; i < *numReturnedLocs; i++) {
 		new[i] = where[i - 1];
 	}

 	return new;
}

PlaceId *DvWhereCanIGoByType(DraculaView dv, bool road, bool boat,
                             int *numReturnedLocs)
{
	assert(dv != NULL);
	// basic initialization
 	Player player = GvGetPlayer(dv->view);
 	// this is dracula's turn, player cannot be hunter
 	assert(player != PLAYER_MINA_HARKER || player != PLAYER_LORD_GODALMING ||
 		   player != PLAYER_DR_SEWARD || player != PLAYER_VAN_HELSING);
	Round round = DvGetRound(dv);
	// set site as current dracula's location
	PlaceId site = DvGetPlayerLocation(dv, player);
	// if current player hasn't made a move yet
 	if (site == NOWHERE) {
		*numReturnedLocs = 0;
		return NULL;
	}
	// dracula cannot travel by rail
	bool rail = false;

	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// first term of new array shold be current location
	new[0] = site;
 	
 	PlaceId *where = GvGetReachableByType(dv->view, player, round, site, road, rail, boat, numReturnedLocs);

 	// ***validmove
 	// assign value to new array
 	for (int i = 1; i < *numReturnedLocs; i++) {
 		new[i] = where[i - 1];
 	}

 	return new;
}

PlaceId *DvWhereCanTheyGo(DraculaView dv, Player player,
                          int *numReturnedLocs)
{
	assert(dv != NULL);
	// basic initialization
	Round round = DvGetRound(dv);
	// set site as current dracula's location
	PlaceId site = DvGetPlayerLocation(dv, player);
	// if current player hasn't made a move yet
 	if (site == NOWHERE) {
		*numReturnedLocs = 0;
		return NULL;
	}

	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// first term of new array shold be current location
	new[0] = site;
 	
	PlaceId *where = GvGetReachable(dv->view, player, round, site, numReturnedLocs);
 	// assign value to new array
	if (player == PLAYER_DRACULA) {
	 	for (int i = 1; i < *numReturnedLocs; i++) {
	 		// if player is dracula
	 		// location cannot be hospital
	 		if (where[i - 1] != ST_JOSEPH_AND_ST_MARY) new[i] = where[i - 1];
	 	}
 	}
 	else {
 		for (int i = 1; i < *numReturnedLocs; i++) {
 			new[i] = where[i - 1];
 		}
 	}

 	return new;
 }

PlaceId *DvWhereCanTheyGoByType(DraculaView dv, Player player,
                                bool road, bool rail, bool boat,
                                int *numReturnedLocs)
{
	assert(dv != NULL);
	// basic initialization
	Round round = DvGetRound(dv);
	// set site as current dracula's location
	PlaceId site = DvGetPlayerLocation(dv, player);
	// if current player hasn't made a move yet
 	if (site == NOWHERE) {
		*numReturnedLocs = 0;
		return NULL;
	}

	PlaceId *new = malloc(sizeof(PlaceId) * NUM_REAL_PLACES);
	// first term of new array shold be current location
	new[0] = site;
 	
 	PlaceId *where = GvGetReachableByType(dv->view, player, round, site, road, rail, boat, numReturnedLocs);
 	// assign value to new array
	if (player == PLAYER_DRACULA) {
	 	for (int i = 1; i < *numReturnedLocs; i++) {
	 		// if player is dracula
	 		// location cannot be hospital
	 		if (where[i - 1] != ST_JOSEPH_AND_ST_MARY) new[i] = where[i - 1];
	 	}
 	}
 	else {
 		for (int i = 1; i < *numReturnedLocs; i++) {
 			new[i] = where[i - 1];
 		}
 	}

 	return new;
}

////////////////////////////////////////////////////////////////////////
// Your own interface functions

// TODO
