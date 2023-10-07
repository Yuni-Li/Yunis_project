#include "Game.h"
 #include "hunter.h"
 #include "HunterView.h"
 #include "Places.h"


 void decideHunterMove(HunterView hv)
 {
 	// TODO: Replace this with something better!
 	registerBestPlay("TO", "Have we nothing Toulouse?");
 	// fundamental stats initialisation
 	char *hunterMove; 	// the final decided location in 2 chars to be returned
 	Player hunter = HvGetPlayer(hv);
 	Round round = HvGetRound(hv);
 	PlaceId hunterLocs = HvGetPlayerLocation(hv, hunter);
 	PlaceId dracLocs = HvGetLastKnownDraculaLocation(hv, &round);
 	PlaceId hunterDecide = hunterLocs; 		// intermediate decided location from diff senarios
	PlaceId *nextMove;
	int pathlength = 100;

 	// hunters strategies to determine a target
 	if (hunter == PLAYER_LORD_GODALMING) 
 	{
 		if (dracLocs ==  CITY_UNKNOWN || dracLocs == SEA_UNKNOWN || dracLocs == HIDE || (dracLocs >= DOUBLE_BACK_1 && dracLocs <= DOUBLE_BACK_5)) 
 		{
 			hunterDecide = hunterLocs;
 		}
 		else 
 			hunterDecide = dracLocs;
 	} 
 	else if (hunter == PLAYER_DR_SEWARD) 
 	{
 		if (dracLocs ==  CITY_UNKNOWN || dracLocs == SEA_UNKNOWN || dracLocs == HIDE || (dracLocs >= DOUBLE_BACK_1 && dracLocs <= DOUBLE_BACK_5)) 
 		{
 			hunterDecide = hunterLocs;
 		}
 		else 
 			hunterDecide = dracLocs;
 	}
 	else if (hunter == PLAYER_VAN_HELSING) 
 	{
 		if (dracLocs ==  CITY_UNKNOWN || dracLocs == SEA_UNKNOWN || dracLocs == HIDE || (dracLocs >= DOUBLE_BACK_1 && dracLocs <= DOUBLE_BACK_5)) 
 		{
 			hunterDecide = hunterLocs;
 		}
 		else 
 			hunterDecide = dracLocs;
 	}
 	else if (hunter == PLAYER_MINA_HARKER)
 	{
 		if (dracLocs ==  CITY_UNKNOWN || dracLocs == SEA_UNKNOWN || dracLocs == HIDE || (dracLocs >= DOUBLE_BACK_1 && dracLocs <= DOUBLE_BACK_5)) 
 		{
 			hunterDecide = hunterLocs;
 		}
 		else 
 			hunterDecide = dracLocs;
 	}

	// determine the next move
	nextMove = HvGetShortestPathTo(hv, hunter, hunterDecide, &pathlength);

 	// location return
 	hunterMove = placeIdToAbbrev(nextMove[1]);
 	registerBestPlay(hunterMove, "hola bat");
 }

