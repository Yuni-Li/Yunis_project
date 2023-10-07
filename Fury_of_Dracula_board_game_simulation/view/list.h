// List.h ... interface to List GADT
// Written by John Shepherd, March 2013

#include <stdlib.h>
#include "Places.h"

typedef struct List *List;
typedef struct ListNode ListNode;

List newList(); // create new empty list
void dropList(List); // free memory used by list
void showList(List); // display as [1,2,3...]
void ListInsert(List,PlaceId); // add item into list
void ListDelete(List,PlaceId); // remove item
PlaceId *ListSearch(List,PlaceId); // return item with key
int  ListLength(List); // # items in list
PlaceId *listToArray (List list); // copy the items in list to array
