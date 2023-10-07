////////////////////////////////////////////////////////////////////////
// COMP2521 20T2 ... the Fury of Dracula
// testGameView.c: test the GameView ADT
//
// As supplied, these are very simple tests.  You should write more!
// Don't forget to be rigorous and thorough while writing tests.
//
// 2014-07-01	v1.0	Team Dracula <cs2521@cse.unsw.edu.au>
// 2017-12-01	v1.1	Team Dracula <cs2521@cse.unsw.edu.au>
// 2018-12-31	v1.1	Team Dracula <cs2521@cse.unsw.edu.au>
// 2020-07-10	v1.2	Team Dracula <cs2521@cse.unsw.edu.au>
//
////////////////////////////////////////////////////////////////////////

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "Game.h"
#include "GameView.h"
#include "Places.h"
#include "testUtils.h"

int main(void)
{
	{///////////////////////////////////////////////////////////////////
	
		printf("Basic initialisation\n");

		char *trail = "";
		Message messages[] = {};
		GameView gv = GvNew(trail, messages);

		assert(GvGetRound(gv) == 0);
		assert(GvGetPlayer(gv) == PLAYER_LORD_GODALMING);
		assert(GvGetScore(gv) == GAME_START_SCORE);
		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) == GAME_START_HUNTER_LIFE_POINTS);
		assert(GvGetHealth(gv, PLAYER_DRACULA) == GAME_START_BLOOD_POINTS);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == NOWHERE);
		assert(GvGetVampireLocation(gv) == NOWHERE);

		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("After Lord Godalming's turn\n");

		char *trail =
			"GST....";
		
		Message messages[1] = {};
		GameView gv = GvNew(trail, messages);

		assert(GvGetRound(gv) == 0);
		assert(GvGetPlayer(gv) == PLAYER_DR_SEWARD);
		assert(GvGetScore(gv) == GAME_START_SCORE);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == STRASBOURG);
		assert(GvGetPlayerLocation(gv, PLAYER_DR_SEWARD) == NOWHERE);

		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("After Mina Harker's turn\n");

		char *trail =
			"GST.... SAO.... HZU.... MBB....";
		
		Message messages[4] = {};
		GameView gv = GvNew(trail, messages);

		assert(GvGetRound(gv) == 0);
		assert(GvGetPlayer(gv) == PLAYER_DRACULA);
		assert(GvGetScore(gv) == GAME_START_SCORE);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == STRASBOURG);
		assert(GvGetPlayerLocation(gv, PLAYER_DR_SEWARD) == ATLANTIC_OCEAN);
		assert(GvGetPlayerLocation(gv, PLAYER_VAN_HELSING) == ZURICH);
		assert(GvGetPlayerLocation(gv, PLAYER_MINA_HARKER) == BAY_OF_BISCAY);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == NOWHERE);

		GvFree(gv);
		printf("Test passed!\n");
	}

	{///////////////////////////////////////////////////////////////////
	
		printf("After Dracula's turn\n");

		char *trail =
			"GST.... SAO.... HZU.... MBB.... DC?.V..";
		
		Message messages[] = {
			"Hello", "Goodbye", "Stuff", "...", "Mwahahahaha"
		};
		
		GameView gv = GvNew(trail, messages);

		assert(GvGetRound(gv) == 1);
		assert(GvGetPlayer(gv) == PLAYER_LORD_GODALMING);
		assert(GvGetScore(gv) == GAME_START_SCORE - SCORE_LOSS_DRACULA_TURN);
		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) == GAME_START_HUNTER_LIFE_POINTS);
		assert(GvGetHealth(gv, PLAYER_DRACULA) == GAME_START_BLOOD_POINTS);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == STRASBOURG);
		assert(GvGetPlayerLocation(gv, PLAYER_DR_SEWARD) == ATLANTIC_OCEAN);
		assert(GvGetPlayerLocation(gv, PLAYER_VAN_HELSING) == ZURICH);
		assert(GvGetPlayerLocation(gv, PLAYER_MINA_HARKER) == BAY_OF_BISCAY);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == CITY_UNKNOWN);
		assert(GvGetVampireLocation(gv) == CITY_UNKNOWN);

		GvFree(gv);
		printf("Test passed!\n");
	}

	{///////////////////////////////////////////////////////////////////
	
		printf("Encountering Dracula\n");

		char *trail =
			"GST.... SAO.... HCD.... MAO.... DGE.V.. "
			"GGEVD..";
		
		Message messages[] = {
			"Hello", "Goodbye", "Stuff", "...", "Mwahahahaha",
			"Aha!"
		};
		
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) ==
				GAME_START_HUNTER_LIFE_POINTS - LIFE_LOSS_DRACULA_ENCOUNTER);
		assert(GvGetHealth(gv, PLAYER_DRACULA) ==
				GAME_START_BLOOD_POINTS - LIFE_LOSS_HUNTER_ENCOUNTER);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == GENEVA);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == GENEVA);
		assert(GvGetVampireLocation(gv) == NOWHERE);

		GvFree(gv);
		printf("Test passed\n");
	}

	{///////////////////////////////////////////////////////////////////
	
		printf("Test for Dracula doubling back at sea, "
		       "and losing blood points (Hunter View)\n");

		char *trail =
			"GGE.... SGE.... HGE.... MGE.... DS?.... "
			"GST.... SST.... HST.... MST.... DD1....";
		
		Message messages[] = {
			"Party at Geneva", "Okay", "Sure", "Let's go", "Mwahahahaha",
			"", "", "", "", "Back I go"
		};
		
		GameView gv = GvNew(trail, messages);

		assert(GvGetRound(gv) == 2);
		assert(GvGetPlayer(gv) == PLAYER_LORD_GODALMING);
		assert(GvGetScore(gv) == GAME_START_SCORE - 2 * SCORE_LOSS_DRACULA_TURN);
		assert(GvGetHealth(gv, PLAYER_DRACULA) ==
				GAME_START_BLOOD_POINTS - (2 * LIFE_LOSS_SEA));
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == SEA_UNKNOWN);

		GvFree(gv);
		printf("Test passed!\n");
	}


	{///////////////////////////////////////////////////////////////////
	
		printf("Test for Dracula doubling back at sea, "
			   "and losing blood points (Dracula View)\n");

		char *trail =
			"GGE.... SGE.... HGE.... MGE.... DEC.... "
			"GST.... SST.... HST.... MST.... DD1.... "
			"GFR.... SFR.... HFR.... MFR....";
		
		Message messages[14] = {
			"Hello", "Rubbish", "Stuff", "", "Mwahahah",
			"Aha!", "", "", "", "Back I go"};
		
		GameView gv = GvNew(trail, messages);

		assert(GvGetRound(gv) == 2);
		assert(GvGetPlayer(gv) == PLAYER_DRACULA);
		assert(GvGetScore(gv) == GAME_START_SCORE - 2 * SCORE_LOSS_DRACULA_TURN);
		assert(GvGetHealth(gv, PLAYER_DRACULA) ==
				GAME_START_BLOOD_POINTS - (2 * LIFE_LOSS_SEA));
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == ENGLISH_CHANNEL);

		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("Checking that hunters' health points are capped\n");
		
		char *trail =
			"GGE.... SGE.... HGE.... MGE.... DC?.V.. "
			"GGE....";
	
		Message messages[6] = {};
		GameView gv = GvNew(trail, messages);
	
		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) == GAME_START_HUNTER_LIFE_POINTS);
		
		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("Testing a hunter 'dying'\n");
		
		char *trail =
			"GGE.... SGE.... HGE.... MGE.... DC?.V.. "
			"GGE.... SGE.... HGE.... MGE.... DSTT... "
			"GGE.... SGE.... HGE.... MGE.... DHIT... "
			"GGE.... SGE.... HGE.... MGE.... DD1T... "
			"GSTTTTD";
		
		Message messages[21] = {};
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetScore(gv) == GAME_START_SCORE
		                         - 4 * SCORE_LOSS_DRACULA_TURN
		                         - SCORE_LOSS_HUNTER_HOSPITAL);
		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) == 0);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == HOSPITAL_PLACE);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == STRASBOURG);
		
		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("Testing Dracula doubling back to Castle Dracula\n");
		
		char *trail =
			"GGE.... SGE.... HGE.... MGE.... DCD.V.. "
			"GGE.... SGE.... HGE.... MGE.... DD1T...";
		
		Message messages[10] = {};
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetHealth(gv, PLAYER_DRACULA) ==
				GAME_START_BLOOD_POINTS + (2 * LIFE_GAIN_CASTLE_DRACULA));
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == CASTLE_DRACULA);
		
		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("Testing vampire/trap locations\n");
		
		char *trail =
			"GVI.... SGE.... HGE.... MGE.... DCD.V.. "
			"GBD.... SGE.... HGE.... MGE.... DKLT... "
			"GSZ.... SGE.... HGE.... MGE.... DGAT... "
			"GSZ.... SGE.... HGE.... MGE....";
		
		Message messages[19] = {};
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == GALATZ);
		assert(GvGetVampireLocation(gv) == CASTLE_DRACULA);
		int numTraps = 0;
		PlaceId *traps = GvGetTrapLocations(gv, &numTraps);
		assert(numTraps == 2);
		sortPlaces(traps, numTraps);
		assert(traps[0] == GALATZ && traps[1] == KLAUSENBURG);
		free(traps);
		
		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("Testing trap locations after one is destroyed\n");
		
		char *trail =
			"GVI.... SGE.... HGE.... MGE.... DBC.V.. "
			"GBD.... SGE.... HGE.... MGE.... DKLT... "
			"GSZ.... SGE.... HGE.... MGE.... DGAT... "
			"GBE.... SGE.... HGE.... MGE.... DCNT... "
			"GKLT... SGE.... HGE.... MGE....";
		
		Message messages[24] = {};
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) ==
				GAME_START_HUNTER_LIFE_POINTS - LIFE_LOSS_TRAP_ENCOUNTER);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == KLAUSENBURG);
		assert(GvGetVampireLocation(gv) == BUCHAREST);
		int numTraps = 0;
		PlaceId *traps = GvGetTrapLocations(gv, &numTraps);
		assert(numTraps == 2);
		sortPlaces(traps, numTraps);
		assert(traps[0] == CONSTANTA && traps[1] == GALATZ);
		free(traps);
		
		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("Testing a vampire maturing\n");
		
		char *trail =
			"GGE.... SGE.... HGE.... MGE.... DC?.V.. "
			"GGE.... SGE.... HGE.... MGE.... DC?T... "
			"GGE.... SGE.... HGE.... MGE.... DC?T... "
			"GGE.... SGE.... HGE.... MGE.... DC?T... "
			"GGE.... SGE.... HGE.... MGE.... DC?T... "
			"GGE.... SGE.... HGE.... MGE.... DC?T... "
			"GGE.... SGE.... HGE.... MGE.... DC?T.V.";
		
		Message messages[35] = {};
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetScore(gv) == GAME_START_SCORE
		                         - 7 * SCORE_LOSS_DRACULA_TURN
		                         - SCORE_LOSS_VAMPIRE_MATURES);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == CITY_UNKNOWN);
		assert(GvGetVampireLocation(gv) == NOWHERE);
		
		GvFree(gv);
		printf("Test passed!\n");
	}
	
	{///////////////////////////////////////////////////////////////////
	
		printf("Testing move/location history\n");
		
		char *trail =
			"GLS.... SGE.... HGE.... MGE.... DST.V.. "
			"GCA.... SGE.... HGE.... MGE.... DC?T... "
			"GGR.... SGE.... HGE.... MGE.... DC?T... "
			"GAL.... SGE.... HGE.... MGE.... DD3T... "
			"GSR.... SGE.... HGE.... MGE.... DHIT... "
			"GSN.... SGE.... HGE.... MGE.... DC?T... "
			"GMA.... SSTTTV.";
		
		Message messages[32] = {};
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetHealth(gv, PLAYER_DR_SEWARD) ==
				GAME_START_HUNTER_LIFE_POINTS - 2 * LIFE_LOSS_TRAP_ENCOUNTER);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == CITY_UNKNOWN);
		assert(GvGetVampireLocation(gv) == NOWHERE);
		
		// Lord Godalming's move/location history
		{
			int numMoves = 0; bool canFree = false;
			PlaceId *moves = GvGetMoveHistory(gv, PLAYER_LORD_GODALMING,
			                                  &numMoves, &canFree);
			assert(numMoves == 7);
			assert(moves[0] == LISBON);
			assert(moves[1] == CADIZ);
			assert(moves[2] == GRANADA);
			assert(moves[3] == ALICANTE);
			assert(moves[4] == SARAGOSSA);
			assert(moves[5] == SANTANDER);
			assert(moves[6] == MADRID);
			if (canFree) free(moves);
		}
		
		// Dracula's move/location history
		{
			int numMoves = 0; bool canFree = false;
			PlaceId *moves = GvGetMoveHistory(gv, PLAYER_DRACULA,
			                                  &numMoves, &canFree);
			assert(numMoves == 6);
			assert(moves[0] == STRASBOURG);
			assert(moves[1] == CITY_UNKNOWN);
			assert(moves[2] == CITY_UNKNOWN);
			assert(moves[3] == DOUBLE_BACK_3);
			assert(moves[4] == HIDE);
			assert(moves[5] == CITY_UNKNOWN);
			if (canFree) free(moves);
		}
		
		{
			int numLocs = 0; bool canFree = false;
			PlaceId *locs = GvGetLocationHistory(gv, PLAYER_DRACULA,
			                                     &numLocs, &canFree);
			assert(numLocs == 6);
			assert(locs[0] == STRASBOURG);
			assert(locs[1] == CITY_UNKNOWN);
			assert(locs[2] == CITY_UNKNOWN);
			assert(locs[3] == STRASBOURG);
			assert(locs[4] == STRASBOURG);
			assert(locs[5] == CITY_UNKNOWN);
			if (canFree) free(locs);
		}
		
		GvFree(gv);
		printf("Test passed!\n");
	}

/*
	{///////////////////////////////////////////////////////////////////
	
		printf("Testing connections\n");
		
		char *trail = "";
		Message messages[] = {};
		GameView gv = GvNew(trail, messages);

		{
			printf("\tChecking Galatz road connections "
			       "(Lord Godalming, Round 1)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachableByType(gv, PLAYER_LORD_GODALMING,
			                                     1, GALATZ, true, false,
			                                     false, &numLocs);

			assert(numLocs == 5);
			sortPlaces(locs, numLocs);
			assert(locs[0] == BUCHAREST);
			assert(locs[1] == CASTLE_DRACULA);
			assert(locs[2] == CONSTANTA);
			assert(locs[3] == GALATZ);
			assert(locs[4] == KLAUSENBURG);
			free(locs);
		}

		{
			printf("\tChecking Ionian Sea boat connections "
			       "(Lord Godalming, Round 1)\n");
			
			int numLocs = -1;
			PlaceId *locs = GvGetReachableByType(gv, PLAYER_LORD_GODALMING,
			                                     1, IONIAN_SEA, false, false,
			                                     true, &numLocs);
			
			assert(numLocs == 7);
			sortPlaces(locs, numLocs);
			assert(locs[0] == ADRIATIC_SEA);
			assert(locs[1] == ATHENS);
			assert(locs[2] == BLACK_SEA);
			assert(locs[3] == IONIAN_SEA);
			assert(locs[4] == SALONICA);
			assert(locs[5] == TYRRHENIAN_SEA);
			assert(locs[6] == VALONA);
			free(locs);
		}

		{
			printf("\tChecking Paris rail connections "
			       "(Lord Godalming, Round 2)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachableByType(gv, PLAYER_LORD_GODALMING,
			                                     2, PARIS, false, true,
			                                     false, &numLocs);
			
			assert(numLocs == 7);
			sortPlaces(locs, numLocs);
			assert(locs[0] == BORDEAUX);
			assert(locs[1] == BRUSSELS);
			assert(locs[2] == COLOGNE);
			assert(locs[3] == LE_HAVRE);
			assert(locs[4] == MARSEILLES);
			assert(locs[5] == PARIS);
			assert(locs[6] == SARAGOSSA);
			free(locs);
		}
		
		{
			printf("\tChecking Athens rail connections (none)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachableByType(gv, PLAYER_LORD_GODALMING,
			                                     1, ATHENS, false, true,
			                                     false, &numLocs);
			
			assert(numLocs == 1);
			assert(locs[0] == ATHENS);
			free(locs);
		}

		GvFree(gv);
		printf("Test passed!\n");
	}*/
	





	
////////////////////////////////////////////////////////////////////////
//////////////////           MY TEST            ////////////////////////
////////////////////////////////////////////////////////////////////////

	{///////////////////////////////////////////////////////////////////
	 // -------->>>>>>>>        TEST CASE[1]         <<<<<<<<-------- //
	 // No Hunters encountered any trap                               //
	 // And the change the no. of trap should -1 in this case since   //
	 // if a trap has left the trail -> vanishes without a trace.     //
	 ///////////////////////////////////////////////////////////////////
		printf("==========================================================\n");
		printf("========== No Hunters encountered -> Trap Boom! ==========\n");
		printf("==========================================================\n");
        // Testing trapLocations
		char *trail =
		    "GSW.... SLS.... HMR.... MHA.... DSJ.V.. "
		    "GLO.... SAL.... HCO.... MBR.... DBET... " 
		    "GED.... SBO.... HLI.... MPR.... DKLT... "
		    "GLV.... SNA.... HNU.... MBD.... DCDT... "
		    "GIR.... SPA.... HPR.... MKL.... DBOT... "
		    "GAO.... SST.... HSZ.... MCD.... DGAT... "
		    "GMS.... SFL.... HKL.... MSZ.... DCNT.V. "
		    "GTS.... SRO.... HBC.... MCN.... DBS..M. ";

		Message messages[40] = {};
		GameView gv = GvNew(trail, messages);
		int numTraps = 0;
		PlaceId *traps = GvGetTrapLocations(gv, &numTraps);

		assert(GvGetScore(gv) == GAME_START_SCORE
		                         - 8 * SCORE_LOSS_DRACULA_TURN
		                         - SCORE_LOSS_VAMPIRE_MATURES);
 		assert(GvGetHealth(gv, PLAYER_DRACULA) == GAME_START_BLOOD_POINTS 
 		                     + LIFE_GAIN_CASTLE_DRACULA - LIFE_LOSS_SEA);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == BLACK_SEA);
        assert(GvGetVampireLocation(gv) == NOWHERE);

		assert(numTraps == 5);
		sortPlaces(traps, numTraps);

		assert(traps[1] == CASTLE_DRACULA && traps[4] == KLAUSENBURG);
		free(traps);
		
		GvFree(gv);
		printf("Test passed!\n");
	}

	{///////////////////////////////////////////////////////////////////
	 // -------->>>>>>>>        TEST CASE[2]         <<<<<<<<-------- //
	 // Hunters encountered trap                                      //
	 // And the change the no. of trap should -2 in this case since   //
	 // if a Hunters encountered a Trap - > Boom!                     //
	 ///////////////////////////////////////////////////////////////////
		printf("=======================================================\n");
		printf("========== Hunters encountered -> Trap Boom! ==========\n");
		printf("=======================================================\n");
        // Testing trapLocations
		char *trail =
			"GVI.... SGE.... HGE.... MGE.... DBC.V.. "
			"GBD.... SGE.... HGE.... MGE.... DKLT... "
			"GSZ.... SGE.... HGE.... MGE.... DGAT... "
			"GBE.... SGE.... HGE.... MGE.... DCNT... "
			"GKLT... SGE.... HGE.... MGAT...";

		Message messages[19] = {};
		GameView gv = GvNew(trail, messages);
		int numTraps = 0;
		PlaceId *traps = GvGetTrapLocations(gv, &numTraps);

		assert(GvGetScore(gv) == GAME_START_SCORE 
		                         - 4 * SCORE_LOSS_DRACULA_TURN);
 		assert(GvGetHealth(gv, PLAYER_MINA_HARKER) == 
 		        GAME_START_HUNTER_LIFE_POINTS - LIFE_LOSS_TRAP_ENCOUNTER);
		assert(GvGetPlayerLocation(gv, PLAYER_MINA_HARKER) == GALATZ);
        assert(GvGetVampireLocation(gv) == BUCHAREST);

		assert(numTraps == 1);
		sortPlaces(traps, numTraps);
		assert(traps[0] == CONSTANTA);
		free(traps);
		
		GvFree(gv);
		printf("Test passed!\n");
	}

    {///////////////////////////////////////////////////////////////////
	 // -------->>>>>>>>        TEST CASE[3]         <<<<<<<<-------- //
	 // If a Hunters encountered an immature Vampire                  //
	 //                     before a vampire has matured -> Boom!     //
	 ///////////////////////////////////////////////////////////////////
		printf("==========================================================\n");
		printf("== Encounter immature Vampire -> Immature Vampire Boom! ==\n");
		printf("==========================================================\n");
        // Testing vampireLocation
		char *trail =
			"GVI.... SGE.... HGE.... MGE.... DCD.V.. "
			"GBD.... SGE.... HGE.... MGE.... DKLT... "
			"GSZ.... SGE.... HGE.... MGE.... DGAT... "
			"GSZ.... SGE.... HGE.... MCDV...";

		Message messages[19] = {};
		GameView gv = GvNew(trail, messages);
		assert(GvGetScore(gv) == GAME_START_SCORE 
		                         - 3 * SCORE_LOSS_DRACULA_TURN);
 		assert(GvGetHealth(gv, PLAYER_MINA_HARKER) == 
	                    GAME_START_HUNTER_LIFE_POINTS);
		assert(GvGetPlayerLocation(gv, PLAYER_MINA_HARKER) == CASTLE_DRACULA);
        assert(GvGetVampireLocation(gv) == NOWHERE);

		GvFree(gv);
		printf("Test passed!\n");
	}

    {///////////////////////////////////////////////////////////////////
	 // -------->>>>>>>>        TEST CASE[4]         <<<<<<<<-------- //
     //             Hunters Lost Life Points and Rests >= 9           //
	 //         /** Life points gained when hunter rests. */          //
	 ///////////////////////////////////////////////////////////////////
		printf("===================================================\n");
		printf("== Hunters Resets -> Cannot exceed 9 life points ==\n");
		printf("===================================================\n");
        // Testing playHealth / trapLocations
		char *trail =
			"GVI.... SGE.... HGE.... MGE.... DBC.V.. "
			"GBD.... SGE.... HGE.... MGE.... DKLT... "
			"GKLT... SGE.... HGE.... MGE.... DGAT... "
			"GGA.... SGE.... HGE.... MGE.... DCNT... "
			"GGA.... ";

		Message messages[21] = {};
		GameView gv = GvNew(trail, messages);
		int numTraps = 0;
		PlaceId *traps = GvGetTrapLocations(gv, &numTraps);

		assert(GvGetScore(gv) == GAME_START_SCORE 
		                         - 4 * SCORE_LOSS_DRACULA_TURN);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == GALATZ);
 		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) == 
 		                    GAME_START_HUNTER_LIFE_POINTS);

		assert(numTraps == 2);
		sortPlaces(traps, numTraps);
		assert(traps[0] == CONSTANTA && traps[1] == GALATZ);
		free(traps);

		GvFree(gv);
		printf("Test passed!\n");
	}

	{///////////////////////////////////////////////////////////////////
	 // -------->>>>>>>>        TEST CASE[5]         <<<<<<<<-------- //
     //             Hunters Lost Life Points and Rests < 9            //
	 //         /** Life points gained when hunter rests. */          //
	 ///////////////////////////////////////////////////////////////////
	
		printf("===================================================\n");
		printf("== Hunters Resets -> But less than 9 life points ==\n");
		printf("===================================================\n");
        // Testing playHealth / trapLocations
		char *trail =
			"GVI.... SGE.... HGE.... MGE.... DBC.V.. "
			"GBD.... SGE.... HGE.... MGE.... DKLT... "
			"GKLT... SGE.... HGE.... MGE.... DGAT... "
			"GGAT... SGE.... HGE.... MGE.... DCNT... "
			"GGA.... ";

		Message messages[21] = {};
		GameView gv = GvNew(trail, messages);
		int numTraps = 0;
		PlaceId *traps = GvGetTrapLocations(gv, &numTraps);

		assert(GvGetScore(gv) == GAME_START_SCORE
		                         - 4 * SCORE_LOSS_DRACULA_TURN);
		assert(GvGetPlayerLocation(gv, PLAYER_LORD_GODALMING) == GALATZ);
		assert(GvGetHealth(gv, PLAYER_LORD_GODALMING) == 
		        GAME_START_HUNTER_LIFE_POINTS - 2*LIFE_LOSS_TRAP_ENCOUNTER
	                                                    + LIFE_GAIN_REST);
		
		assert(numTraps == 1);
		sortPlaces(traps, numTraps);
		assert(traps[0] == CONSTANTA);
		free(traps);

		GvFree(gv);
		printf("Test passed!\n");
	}

	{///////////////////////////////////////////////////////////////////
	
		printf("Testing Last move/location history\n");
		
		char *trail =
			"GLS.... SGE.... HGE.... MGE.... DST.V.. "
			"GCA.... SGE.... HGE.... MGE.... DC?T... "
			"GGR.... SGE.... HGE.... MGE.... DC?T... "
			"GAL.... SGE.... HGE.... MGE.... DD3T... "
			"GSR.... SGE.... HGE.... MGE.... DHIT... "
			"GSN.... SGE.... HGE.... MGE.... DC?T... "
			"GMA.... SSTTTV.";
		
		Message messages[32] = {};
		GameView gv = GvNew(trail, messages);
		
		assert(GvGetHealth(gv, PLAYER_DR_SEWARD) ==
				GAME_START_HUNTER_LIFE_POINTS - 2 * LIFE_LOSS_TRAP_ENCOUNTER);
		assert(GvGetPlayerLocation(gv, PLAYER_DRACULA) == CITY_UNKNOWN);
		assert(GvGetVampireLocation(gv) == NOWHERE);
		
	    // Lord Godalming's last 3 move/location history
		{
			int numReturnMoves = 0; bool canFree = false; int numMoves = 3;
			PlaceId *nummoves = GvGetLastMoves(gv, PLAYER_LORD_GODALMING, numMoves,
			                                  &numReturnMoves, &canFree);
			assert(numReturnMoves == 3);
			assert(nummoves[0] == SARAGOSSA);
			assert(nummoves[1] == SANTANDER);
			assert(nummoves[2] == MADRID);
			if (canFree) free(nummoves);
		}
		{
			int numReturnLocs = 0; bool canFree = false; int numLocs = 3;
			PlaceId *numlocs = GvGetLastLocations(gv, PLAYER_LORD_GODALMING, numLocs,
			                                  &numReturnLocs, &canFree);
			assert(numReturnLocs == 3);
			assert(numlocs[0] == SARAGOSSA);
			assert(numlocs[1] == SANTANDER);
			assert(numlocs[2] == MADRID);
			if (canFree) free(numlocs);
		}
		
		// Dracula's last 4 move/location history
		{
			int numReturnMoves = 0; bool canFree = false; int numMoves = 4;
			PlaceId *nummoves = GvGetLastMoves(gv, PLAYER_DRACULA, numMoves,
			                                  &numReturnMoves, &canFree);
			assert(numReturnMoves == 4);
			assert(nummoves[0] == CITY_UNKNOWN);
			assert(nummoves[1] == DOUBLE_BACK_3);
			assert(nummoves[2] == HIDE);
			assert(nummoves[3] == CITY_UNKNOWN);
			if (canFree) free(nummoves);
		}
		
		{
			int numReturnLocs = 0; bool canFree = false; int numLocs = 4;
			PlaceId *numlocs = GvGetLastLocations(gv, PLAYER_DRACULA, numLocs,
			                                     &numReturnLocs, &canFree);
			assert(numReturnLocs == 4);
			assert(numlocs[0] == CITY_UNKNOWN);
			assert(numlocs[1] == STRASBOURG);
			assert(numlocs[2] == STRASBOURG);
			assert(numlocs[3] == CITY_UNKNOWN);
			if (canFree) free(numlocs);
		}
		
		GvFree(gv);
		printf("Test passed!\n");
	}

    /*  
    printf("Testing connections reachable\n");
		
		char *trail = "";
		Message messages[] = {};
		GameView gv = GvNew(trail, messages);

		{
			printf("\tChecking SZEGED road connections "
			       "(DRACULA, Round 1)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachable(gv, PLAYER_DRACULA,
			                                     1, SZEGED, &numLocs);

			assert(numLocs == 4);
			sortPlaces(locs, numLocs);
			assert(locs[0] == BUDAPEST);
			assert(locs[1] == BELGRADE);
			assert(locs[2] == SARAJEVO);
			assert(locs[3] == KLAUSENBURG);
			free(locs);
		}
		{
			printf("\tChecking VENICE road and sea connections "
			       "(DRACULA, Round 1)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachable(gv, PLAYER_DRACULA,
			                                     1, VENICE, &numLocs);

			assert(numLocs == 5);
			sortPlaces(locs, numLocs);
			assert(locs[0] == ADRIATIC_SEA);
			assert(locs[1] == FLORENCE);
			assert(locs[2] == GENOA);
			assert(locs[3] == MILAN);
			assert(locs[4] == MUNICH);
			free(locs);
		}

		{
			printf("\tChecking SZEGED road connections "
			       "(LORD_GODALMING, Round 0)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachable(gv, PLAYER_LORD_GODALMING,
			                                     0, SZEGED, &numLocs);

			assert(numLocs == 5);
			sortPlaces(locs, numLocs);
			assert(locs[0] == BUDAPEST);
			assert(locs[1] == BELGRADE);
			assert(locs[2] == SARAJEVO);
			assert(locs[3] == KLAUSENBURG);
			assert(locs[4] == ST_JOSEPH_AND_ST_MARYS);
			free(locs);
		}
		
		{
			printf("\tChecking SZEGED road connections "
			       "(LORD_GODALMING, Round 1)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachable(gv, PLAYER_LORD_GODALMING,
			                                     1, SZEGED, &numLocs);

			assert(numLocs == 6);
			sortPlaces(locs, numLocs);
			assert(locs[0] == BUDAPEST);
			assert(locs[1] == BELGRADE);
			assert(locs[2] == SARAJEVO);
			assert(locs[3] == KLAUSENBURG);
			assert(locs[4] == ST_JOSEPH_AND_ST_MARYS);
			assert(locs[5] == BUCHAREST);
			free(locs);
		}
		
		{
			printf("\tChecking MUNICH connections "
			       "(LORD_GODALMING, Round 2)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachable(gv, PLAYER_LORD_GODALMING ,
			                                     2, MUNICH, &numLocs);

			assert(numLocs == 5);
			sortPlaces(locs, numLocs);
			assert(locs[0] == LEIPZIG);
			assert(locs[1] == MILAN);
			assert(locs[2] == NUREMBURG);
			assert(locs[3] == STRASBOURG);
			assert(locs[4] == VENICE);
			assert(locs[5] == VIENNA);
			assert(locs[6] == ZAGREB);
			assert(locs[7] == ZURICH);
			
			
			free(locs);
		}
		{
			printf("\tChecking MUNICH connections "
			       "(LORD_GODALMING, Round 3)\n");
			int numLocs = -1;
			PlaceId *locs = GvGetReachable(gv, PLAYER_LORD_GODALMING ,
			                                     3, MUNICH, &numLocs);

			assert(numLocs == 10);
			sortPlaces(locs, numLocs);
			assert(locs[0] == BERLIN);
			assert(locs[1] == FRANKFURT);
			assert(locs[2] == LEIPZIG);
			assert(locs[3] == MILAN);
			assert(locs[4] == NUREMBURG);
			assert(locs[5] == STRASBOURG);
			assert(locs[6] == VENICE);
			assert(locs[7] == VIENNA);
			assert(locs[8] == ZAGREB);
			assert(locs[9] == ZURICH);
			
			free(locs);
		}
        */

////////////////////////////////////////////////////////////////////////
//////////////////          MY TEST END         ////////////////////////
////////////////////////////////////////////////////////////////////////
	
	return EXIT_SUCCESS;
}
