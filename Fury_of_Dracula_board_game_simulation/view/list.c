// List.c ... implementation of List ADT as linked-list
// Written by John Shepherd, March 2013

#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include "list.h"

typedef struct ListNode {
	PlaceId value;
	ListNode *next;
} ListNode;

struct List {
	ListNode *first;  // ptr to first node
	ListNode *last;   // ptr to last node
	ListNode *railBranch;
    int size;
};

// create new empty list
List newList()
{
	List L;
	L = malloc(sizeof(List));
	assert(L != NULL);
	L->first = NULL;
	L->last = NULL;
	return L;
}

// free memory used by list
void dropList(List L)
{
	assert(L != NULL);
	ListNode *next;
	while (L->first != NULL) {
		next = L->first->next;
		dropItem(L->first->value);
		free(L->first);
		L->first = next;
	}
	free(L);
}

// display as [1,2,3,4...]
void showList(List L)
{
	assert(L != NULL);
	ListNode *curr = L->first;
	printf("[");
	while (curr != NULL) {
		showItem(curr->value);
		if (curr->next != NULL)
			printf(",");
	}
	printf("]");
}

// add item into list
// no check for duplicates
void ListInsert(List L, PlaceId location)
{
	assert(L != NULL);
	ListNode *new = malloc(sizeof(ListNode));
	assert(new != NULL);
	new->value = itemCopy(location);
	new->next = NULL;
	if (L->last != NULL)
		L->last->next = new;
	else
		L->first = L->last = new;
}

// remove item(s)
// assumes no duplicates
void ListDelete(List L, PlaceId location)
{
	assert(L != NULL);
	ListNode *prev, *curr;
	prev = NULL; curr = L->first;
	while (curr != NULL) {
		if (eq(location, key(curr->value)))
			break;
		prev = curr;
		curr = curr->next;
	}
	if (curr != NULL) {
		if (prev == NULL)
			L->first = curr->next;
		else
			prev->next = curr->next;
		free(curr);
		if (L->first == NULL)
			L->last = NULL;
	}
}

// return item with key
PlaceId *ListSearch(List L, PlaceId location)
{
	assert(L != NULL);
	ListNode *curr = L->first;
	while (curr != NULL) {
		if (eq(location, key(curr->value)))
			return &(curr->value);
		else
			curr = curr->next;
	}
	return NULL; // key not found
}

// # items in list
int ListLength(List L)
{
	int n = 0;
	ListNode *curr = L->first; 
	while (curr != NULL) {
		n++;
		curr = curr->next;
	}
	return n;
}

PlaceId *listToArray (List list)
{
	PlaceId *newArray = malloc(list->size * sizeof(PlaceId));
	int i = 0;
	
	for (ListNode *node = list->first; node != NULL; node = node->next)
	{
		newArray[i] = node->value;
		i++;
	}
	return newArray;
}

void removeDuplicate (List list)
{
	ListNode *prev = NULL;
	ListNode *curr = list->railBranch;

	// waiting for loops implementation to get # of duplicates - counter
	// if counter > 1, remove node
	// cannot use  ListSearch without modification, it will count in the value itself 
	while (curr != NULL)
	{
		int counter = 0;
		for (ListNode *traversal = list->first; traversal != NULL; traversal = traversal->next)
		{
			if () 
			{
				counter++;
			}
		}
		if (counter > 1)
		{
			prev->next = curr->next;
		}
	}
}
