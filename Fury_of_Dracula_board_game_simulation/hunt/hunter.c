////////////////////////////////////////////////////////////////////////
// COMP2521 20T2 ... the Fury of Dracula
// hunter.c: your "Fury of Dracula" hunter AI.
//
// 2014-07-01	v1.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2017-12-01	v1.1	Team Dracula <cs2521@cse.unsw.edu.au>
// 2018-12-31	v2.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2020-07-10	v3.0	Team Dracula <cs2521@cse.unsw.edu.au>
//
////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <assert.h>
#include "Game.h"
#include "hunter.h"
#include "HunterView.h"

struct hunterDecide {
	PlaceId *hmoves;
	int *locscore;
	int hmovesLen;
};

typedef struct hunterDecide *HunterDecide;

void initialHD(int numMoves, HunterDecide hd);
PlaceId initialHunterLoc(Player player);
PlaceId *pathToLastKnown (HunterView hv, Player player, HunterDecide hd, 
						  Round round, int numMoves);
void initialOrStay (HunterView hv, Player player, Round round, int stay);
PlaceId *predictDNextMove (HunterView hv, PlaceId lastDLoc, PlaceId *path,
						   Player player, HunterDecide hd, int numMoves);
PlaceId findBestMove(HunterDecide hd);

void decideHunterMove(HunterView hv)
{
	Player currH = HvGetPlayer(hv);
	Round round = HvGetRound(hv);

	char *best;
	int numMoves = -1;
	int stay = 0;

	// initialize
	HunterDecide hd = malloc(sizeof(hv));
	if (hd == NULL) {
		fprintf(stderr, "Couldn't allocate HunterDecide!\n");
		exit(EXIT_FAILURE);
	}
	
	initialHD(numMoves, hd);
		    
	PlaceId *path = pathToLastKnown(hv, currH, hd, round, numMoves);
	hd->hmoves = path;
	hd->hmovesLen = numMoves;

	// initialize or stay
    initialOrStay (hv, currH, round, stay); 

	// if never
    if (stay == 1 || hd->hmoves == NULL) {
    	PlaceId initial = initialHunterLoc(currH);
    	best = placeIdToAbbrev(initial);
    }
    else {
    	int next = findBestMove(hd);
    	best = placeIdToAbbrev(hd->hmoves[next]);
    }
    
	registerBestPlay(best, "Have we nothing Toulouse?");
}

// initialize
void initialHD(int numMoves, HunterDecide hd)
{
	hd->hmovesLen = numMoves - 1;
	hd->hmoves = malloc(NUM_REAL_PLACES * sizeof(PlaceId));
	int *score = malloc(NUM_REAL_PLACES * sizeof(int));
	hd->locscore = score;
	for (int i = 0; i < NUM_REAL_PLACES; i++)
	    hd->locscore[i] = 100;
}

// initialize starting loc
PlaceId initialHunterLoc(Player player)
{
	assert(player != PLAYER_DRACULA);

	switch (player) {
		case PLAYER_LORD_GODALMING: return GALATZ;
		case PLAYER_DR_SEWARD:      return KLAUSENBURG;
		case PLAYER_VAN_HELSING:    return MANCHESTER;
		case PLAYER_MINA_HARKER:    return STRASBOURG;
		default:            		assert(0);
	}
}

// find path to last known dracula location
PlaceId *pathToLastKnown (HunterView hv, Player player, HunterDecide hd, 
						  Round round, int numMoves)
{
	int numReturnedLocs1 = -1;
	int numReturnedLocs2 = -1;
	int k = 0;
	// new path
	PlaceId *path = malloc(NUM_REAL_PLACES * sizeof(PlaceId));
	// dracula last known location
	PlaceId lastDLoc = HvGetLastKnownDraculaLocation(hv, &round);
    
	if (lastDLoc == NOWHERE || lastDLoc == CITY_UNKNOWN || lastDLoc == SEA_UNKNOWN) {
		// if dracula has not made a move yet
		path = predictDNextMove(hv, lastDLoc, path, player, hd, numMoves);
	}
	else {
		// shortest path from currloc to dracula last known
		PlaceId *shortest = HvGetShortestPathTo(hv, player, lastDLoc, &numReturnedLocs1);
		PlaceId *next = HvWhereCanIGo(hv, &numReturnedLocs2);

		if (numReturnedLocs1 == 0) return next;

		for (int i = 0; i < numReturnedLocs1; i++) {
			// currloc is in shortest path list
			for (int j = 0; j < numReturnedLocs2; j++) {
			    
				if (next[j] == shortest[i]) {
				    
					path[k] = next[j];
					hd->locscore[k] += 10;
					numMoves++;
					k++;
					break;
				}
			}
		}
		
	}
	return path;
}

// initialize or stay
void initialOrStay (HunterView hv, Player player, Round round, int stay) 
{
	// hunter curr location
	PlaceId currLoc = HvGetPlayerLocation(hv, player);
	// dracula last known location
	PlaceId lastDLoc = HvGetLastKnownDraculaLocation(hv, &round);

	// if dracula never reveald in the play string
	// or has not started yet
	if (lastDLoc == NOWHERE || currLoc == NOWHERE) stay = 1;
}

// predict dracula's next move
PlaceId *predictDNextMove (HunterView hv, PlaceId lastDLoc, PlaceId *path,
						   Player player, HunterDecide hd, int numMoves)
{
	int numReturnedLocs1 = -1;
	int numReturnedLocs2 = -1;
	int moved = 0;
	// new path
	PlaceId *dPath = malloc(NUM_REAL_PLACES * sizeof(PlaceId));
	PlaceId *hPath = malloc(NUM_REAL_PLACES * sizeof(PlaceId));
	if (lastDLoc == CITY_UNKNOWN) {
		// city unknown
		dPath = HvWhereCanTheyGoByType(hv, PLAYER_DRACULA, true, false, false, &numReturnedLocs1);
		hPath = HvWhereCanIGoByType(hv, true, true, false, &numReturnedLocs2);
		moved = 1;
	}
	else if (lastDLoc == SEA_UNKNOWN) {
		// sea unknown
		dPath = HvWhereCanTheyGoByType(hv, PLAYER_DRACULA, false, false, true, &numReturnedLocs1);
		hPath = HvWhereCanIGoByType(hv, false, true, true, &numReturnedLocs2);
		moved = 1;
	}
	else {
		// NOWHERE
		hPath = HvWhereCanIGo(hv, &numReturnedLocs1);
	}

	// add same locs to path[]
	int k = 0;
	bool same = false;
	if (moved != 0) {
		for (int i = 0; i < numReturnedLocs1; i++) {
			for (int j = 0; j < numReturnedLocs2; j++) {
				if (hPath[j] == dPath[i]) {
					path[k] = hPath[j];
					numMoves++;
					hd->locscore[k] += 10;
					k++;
					same = true;
				}
			}
		}
	}

	// if there is no same locs or dracula has not made a move yet
    if (same || moved == 0) path= hPath;
	return path;
}

// find the place where has the heightest score
int findBestMove(HunterDecide hd)
{
	int biggest = 0;
    for (int i = 1; i < hd->hmovesLen; i++) {
        if (hd->locscore[biggest] < hd->locscore[i]) 
            biggest = i;
    }
    return biggest;
}
