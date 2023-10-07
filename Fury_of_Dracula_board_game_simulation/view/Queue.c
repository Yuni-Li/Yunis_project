// Queue.c ... implementation of Queue ADT

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "Queue.h"
#include "Item.h"

typedef struct QueueNode {
	PlaceId value;
	struct QueueNode *next;
} QueueNode;

typedef struct QueueRep {
	QueueNode *head; // ptr to first node
	QueueNode *tail; // ptr to last node
} QueueRep;

// create new empty Queue
Queue newQueue (void)
{
	QueueRep *new = malloc (sizeof *new);
	*new = (QueueRep){ .head = NULL, .tail = NULL };
	return new;
}

// free memory used by Queue
void dropQueue (Queue Q)
{
	assert (Q != NULL);
	for (QueueNode *curr = Q->head, *next; curr != NULL; curr = next) {
		next = curr->next;
		free (curr);
	}
	free (Q);
}

// add item at end of Queue
void QueueJoin (Queue Q, PlaceId id)
{
	assert (Q != NULL);

	QueueNode *new = malloc (sizeof *new);
	assert (new != NULL);
	*new = (QueueNode){ .value = ItemCopy (id), .next = NULL };

	if (Q->head == NULL)
		Q->head = new;
	if (Q->tail != NULL)
		Q->tail->next = new;
	Q->tail = new;
}

// remove item from front of Queue
Item QueueLeave (Queue Q)
{
	assert (Q != NULL);
	assert (Q->head != NULL);
	Item it = ItemCopy (Q->head->value);
	QueueNode *old = Q->head;
	Q->head = old->next;
	if (Q->head == NULL)
		Q->tail = NULL;
	free (old);
	return it;
}

// check for no items
int QueueIsEmpty (Queue Q)
{
	return (Q->head == NULL);
}
