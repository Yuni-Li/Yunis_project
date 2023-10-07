////////////////////////////////////////////////////////////////////////
// COMP2521 20T2 ... the Fury of Dracula
// dracula.c: your "Fury of Dracula" Dracula AI
//
// 2014-07-01	v1.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2017-12-01	v1.1	Team Dracula <cs2521@cse.unsw.edu.au>
// 2018-12-31	v2.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2020-07-10	v3.0	Team Dracula <cs2521@cse.unsw.edu.au>
//
////////////////////////////////////////////////////////////////////////

#include <stdio.h>
#include <string.h>
#include <assert.h>

#include "dracula.h"
#include "DraculaView.h"
#include "Game.h"
#include "Queue.h"
#include "utils.h"

#define numPortCity 29

struct draculadecide {
    PlaceId *dmoves;
    PlaceId *dlocs;
    int  *locscore;
    int   dmovesLen;
};

typedef struct draculadecide *DraculaDecide;

void initialDD(DraculaView dv, DraculaDecide dd, int numMoves, PlaceId *draculamoves);
void addtoDlocs(DraculaView dv, DraculaDecide dd, int i);
static bool isHide(PlaceId move);
static bool isDoubleBack(PlaceId move);
PlaceId findFirstMove(DraculaDecide dd);
bool firstMoveCond(DraculaDecide dd, PlaceId p);
bool placeIsPortCity(PlaceId pid);
void mightEnconterH(DraculaView dv, DraculaDecide dd);
void hunterFirstMove(DraculaDecide dd, PlaceId *locs, int numLocations);
void loseEnconterH(PlaceId *locs, int numLocations, DraculaDecide dd);
void isSea(DraculaDecide dd);
int findBestMove(DraculaDecide dd);

void decideDraculaMove(DraculaView dv)
{
	char best[3] = "CD";
	
	// dracula's possible move
	int numMoves = -1;
	PlaceId *draculamoves = DvGetValidMoves(dv, &numMoves);
	
	// inistialize DraculaDecide
	DraculaDecide dd = malloc(sizeof(*dd));
	if (dd == NULL) {
		fprintf(stderr, "Couldn't allocate DraculaDecide!\n");
		exit(EXIT_FAILURE);
	}

	dd->dmovesLen = numMoves;
	if (numMoves != 0)
	    initialDD(dv, dd, numMoves, draculamoves);
    
	if (DvGetPlayerLocation(dv, PLAYER_DRACULA) == NOWHERE) {	    
	    PlaceId *dmoves = malloc(NUM_REAL_PLACES * sizeof(PlaceId));
	    dd->dmoves = dmoves;
	    mightEnconterH(dv, dd);
	    if (!placesContains(dd->dmoves, dd->dmovesLen, placeAbbrevToId("CD")))
	        strcpy(best, "CD");
	    else {
	        strcpy(best, placeIdToAbbrev(findFirstMove(dd)));
	    }
	    free(dd->dmoves);
    // Nowhere To Go -> "TP"
	} else if (dd->dmoves == NULL)    
	    strcpy(best, "TP");
	else {
	    mightEnconterH(dv, dd);
	    isSea(dd);
	    // Calculate the weight(place) to find a "cost-effective" way
	    int biggest = findBestMove(dd);
	    strcpy(best, placeIdToAbbrev(dd->dmoves[biggest]));
	    free(dd->dmoves);
	    free(dd->dlocs);
	    free(dd->locscore);
	}

	// free meomery
	free(dd);
	registerBestPlay(best, "Mwahahahaha");
}

void initialDD(DraculaView dv, DraculaDecide dd, int numMoves, PlaceId *draculamoves) 
{
	// initial dmoves
	PlaceId *dmoves = malloc(dd->dmovesLen * sizeof(PlaceId));
	dmoves = draculamoves;
	dd->dmoves = dmoves;
	// initial dlocs
	PlaceId *dlocs = malloc(dd->dmovesLen * sizeof(PlaceId));
	dd->dlocs = dlocs;
	for (int i = 0; i < dd->dmovesLen; i++) {
	    addtoDlocs(dv, dd, i);
	}

	// initial score
	int *score = malloc(dd->dmovesLen * sizeof(int));
	dd->locscore = score;
	for (int i = 0; i < dd->dmovesLen; i++)
	    dd->locscore[i] = 100;
}

// Find a reasonable initial location
PlaceId findFirstMove(DraculaDecide dd) 
{
    PlaceId p = 0;
    while (!firstMoveCond(dd, p)) p++;
    assert(p <= MAX_REAL_PLACE);
    return p;
}

// Exclude the illogical/unreasonable places
bool firstMoveCond(DraculaDecide dd, PlaceId p)
{
    return !placesContains(dd->dmoves, dd->dmovesLen, p) 
            && !placeIsSea(p) && !placeIsPortCity(p);
}

// 
void addtoDlocs(DraculaView dv, DraculaDecide dd, int i)
{
    if (placeIsReal(dd->dmoves[i]))
        dd->dlocs[i] = dd->dmoves[i];
    else if (isHide(dd->dmoves[i]))
        dd->dlocs[i] = DvGetPlayerLocation(dv, PLAYER_DRACULA);
    else if (isDoubleBack(dd->dmoves[i])) {
        dd->dlocs[i] = dv->trailLocations[dd->dmoves[i] - DOUBLE_BACK_1];
    }
}

// Check if it's HIDE
static bool isHide(PlaceId move) 
{
	return move == HIDE;
}

// Check if it's DoubleBack 1...5
static bool isDoubleBack(PlaceId move) {
	return move >= DOUBLE_BACK_1 && move <= DOUBLE_BACK_5;
}

// Possible situations
void mightEnconterH(DraculaView dv, DraculaDecide dd) 
{  
    for (int player = PLAYER_LORD_GODALMING; player < PLAYER_DRACULA; player++) {
        int numReturnedLocs = -1;
        PlaceId *locs = DvWhereCanTheyGo(dv, player, &numReturnedLocs);
        locs[numReturnedLocs] = DvGetPlayerLocation(dv, player);
        numReturnedLocs++;
        if (DvGetRound(dv) == 0) hunterFirstMove(dd, locs, numReturnedLocs);
        else loseEnconterH(locs, numReturnedLocs, dd);
    }
}

// Find out the starting location for Hunters
void hunterFirstMove(DraculaDecide dd, PlaceId *locs, int numLocations)
{
    placesCopy(dd->dmoves + dd->dmovesLen, locs, numLocations);
    dd->dmovesLen += numLocations;
}

// Reduce the weight(places) if Dracula encounters a Hunter
void loseEnconterH(PlaceId *locs, int numLocations, DraculaDecide dd) 
{
    for (int i = 0; i < numLocations; i++) {
        for (int j = 0; j < dd->dmovesLen; j++) {
            if (locs[i] == dd->dlocs[j]) {
                if (i == numLocations) dd->locscore[j] -= 10; 
                dd->locscore[j] -= 10; 
                
            }
        }
    }
}

// Sea -> Adjustment of weight, reduction
void isSea(DraculaDecide dd)
{
    for (int i = 0; i < dd->dmovesLen; i++) {
        if (placeIsSea(dd->dlocs[i])) dd->locscore[i] -= 2; 
    }
}

// Calculation of final weights
int findBestMove(DraculaDecide dd)
{
    int biggest = 0;
    for (int i = 1; i < dd->dmovesLen; i++) {
        if (dd->locscore[biggest] < dd->locscore[i]) 
            biggest = i;
    }
    return biggest;
}

// Check if it's PortCity
bool placeIsPortCity(PlaceId pid)
{
    PlaceId portCity[] = {ALICANTE, AMSTERDAM, ATHENS, BARCELONA, BARI, 
                BORDEAUX, CADIZ, CAGLIARI, CONSTANTA, DUBLIN, EDINBURGH, 
                GALWAY, GENOA, HAMBURG, LE_HAVRE, LISBON, LIVERPOOL, 
                LONDON, MARSEILLES, NANTES, NAPLES, PLYMOUTH, ROME, 
                SALONICA, SANTANDER, SWANSEA, VALONA, VARNA, VENICE};
    return placesContains(portCity, numPortCity, pid);
}
