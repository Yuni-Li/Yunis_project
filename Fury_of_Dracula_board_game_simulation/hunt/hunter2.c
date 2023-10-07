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

void initialHD(int numMoves, PlaceId *hunterMoves, HunterDecide hd);
PlaceId initialHunterLoc(Player player);
PlaceId *pathToLastKnown (HunterView hv, Player player, HunterDecide hd, 
						  Round round, int numMoves);
void initialOrStay (HunterView hv, Player player, Round round, int stay);
PlaceId *predictDNextMove (HunterView hv, PlaceId lastDLoc, PlaceId *path,
						   Player player, HunterDecide hd, int numMoves);
PlaceId findBestMove(HunterDecide hd);
//void colResearch (HunterView hv, Player player, PlaceId dontMove);

void decideHunterMove(HunterView hv)
{
	// assert(hv != NULL);
	Player currH = HvGetPlayer(hv);
	assert(currH != PLAYER_DRACULA);
	//currH = getHunters(currH);
	Round round = HvGetRound(hv);

	char *best;
	int numMoves = -1;
	int stay = 0;
	//PlaceId *hunterMoves = HvWhereCanIGo(hv, &numMoves);

	// initialize
	HunterDecide hd = malloc(sizeof(hv));
	if (hd == NULL) {
		fprintf(stderr, "Couldn't allocate HunterDecide!\n");
		exit(EXIT_FAILURE);
	}

	PlaceId *path = pathToLastKnown(hv, currH, hd, round, numMoves);
    initialHD(numMoves, path, hd);
    initialOrStay (hv, currH, round, stay); 

	// if never
    if (stay == 1 || hd->hmoves == NULL || numMoves == -1) {
    	PlaceId initial = initialHunterLoc(currH);
    	best = placeIdToAbbrev(initial);
    }
    // do collaborative research
    else if (stay == 2) {
    	//PlaceId dontMove = NOWHERE;
    	//colResearch(hv, currH, dontMove);
    	PlaceId dontMove = HvGetPlayerLocation(hv, currH);
    	best = placeIdToAbbrev(dontMove);
    }
    else {
    	int next = findBestMove(hd);
    	best = placeIdToAbbrev(hd->hmoves[next]);
    }

	//printf("%s\n",best);
	registerBestPlay(best, "Have we nothing Toulouse?");
}

void initialHD(int numMoves, PlaceId *hunterMoves, HunterDecide hd)
{
	hd->hmovesLen = numMoves - 1;
	PlaceId *hmoves = malloc(hd->hmovesLen * sizeof(PlaceId));
	hmoves = hunterMoves;
	hd->hmoves = hmoves;
	int *score = malloc(hd->hmovesLen * sizeof(int));
	hd->locscore = score;
	for (int i = 0; i < hd->hmovesLen; i++)
	    hd->locscore[i] = 100;
}

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

PlaceId *pathToLastKnown (HunterView hv, Player player, HunterDecide hd, 
						  Round round, int numMoves)
{
	//int found = 0;
	// if other hunter in this city
	//int someoneHere = 0;
	int numReturnedLocs1 = -1;
	int numReturnedLocs2 = -1;
	int k = 0;
	// hunter curr location
	//PlaceId currLoc = HvGetPlayerLocation(hv, player);
	// new path
	PlaceId *path = malloc(numReturnedLocs1 * sizeof(PlaceId));
	// dracula last known location
	PlaceId lastDLoc = HvGetLastKnownDraculaLocation(hv, &round);

	if (lastDLoc == NOWHERE) return 0;

	if (lastDLoc == CITY_UNKNOWN || lastDLoc == SEA_UNKNOWN) {
		path = predictDNextMove(hv, lastDLoc, path, player, hd, numMoves);
	}
	else {
		// shortest path from currloc to dracula last known
		PlaceId *shortest = HvGetShortestPathTo(hv, player, lastDLoc, &numReturnedLocs1);
		PlaceId *next = HvWhereCanIGo(hv, &numReturnedLocs2);
		for (int i = 0; i < numReturnedLocs1 - 1; i++) {
			// currloc is in shortest path list
			//if (currLoc == shortest[i]) found = 1;
			for (int j = 0; j < numReturnedLocs2; j++) {
				if (next[j] == shortest[i + 1]) {
					path[k] = next[j];
					numMoves++;
					k++;
					break;
				}
			}
		}
		hd->locscore[k] += 10;
	}
	return path;
}

void initialOrStay (HunterView hv, Player player, Round round, int stay) 
{
	int checkRound = round;
	// hunter curr location
	PlaceId currLoc = HvGetPlayerLocation(hv, player);
	// dracula last known location
	PlaceId lastDLoc = HvGetLastKnownDraculaLocation(hv, &round);
	// if dracula never reveald in the play string
	// or has not started yet
	if (lastDLoc == NOWHERE || currLoc == NOWHERE) stay = 1;
	else if (checkRound > round + 5) stay = 2;

}

PlaceId *predictDNextMove (HunterView hv, PlaceId lastDLoc, PlaceId *path,
						   Player player, HunterDecide hd, int numMoves)
{
	int numReturnedLocs = -1;
	// new path
	PlaceId *dPath = malloc(numReturnedLocs * sizeof(PlaceId));
	PlaceId *hPath = malloc(numReturnedLocs * sizeof(PlaceId));
	if (lastDLoc == CITY_UNKNOWN) {
		// city unknown
		dPath = HvWhereCanTheyGoByType(hv, PLAYER_DRACULA, true, false, false, &numReturnedLocs);
		hPath = HvWhereCanIGoByType(hv, true, true, false, &numReturnedLocs);
	}
	else {
		// sea unknown
		dPath = HvWhereCanTheyGoByType(hv, PLAYER_DRACULA, false, false, true, &numReturnedLocs);
		hPath = HvWhereCanIGoByType(hv, false, true, true, &numReturnedLocs);
	}

	// add same locs to path[]
	int k = 0;
	for (int i = 0; i < numReturnedLocs; i++) {
		for (int j = 0; j < numReturnedLocs; j++) {
			if (hPath[j] == dPath[i]) {
				path[k] = hPath[j];
				numMoves++;
				hd->locscore[k] += 10;
				k++;
			}
		}
	}

	return path;
}

int findBestMove(HunterDecide hd)
{
	/*int next = 0;
	for (int i = 0; i < numReturnedLocs; i++)
	if (path[i+1] != CITY_UNKNOWN && path[i+1] != SEA_UNKNOWN) {
		next = i + 1;
		break;
	}
	return next;*/
	int biggest = 0;
    for (int i = 1; i < hd->hmovesLen; i++) {
        if (hd->locscore[biggest] < hd->locscore[i]) 
            biggest = i;
        //printf("%d*********%d\n", i, biggest);
    }
    return biggest;
}
/*
void colResearch (HunterView hv, Player player, PlaceId dontMove)
{
	while (player < PLAYER_DRACULA) {
		dontMove = HvGetPlayerLocation(hv,player);
		player++;
	}
}*/






