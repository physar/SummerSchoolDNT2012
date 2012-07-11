import sys
import math
import bisect

class aStar_v1:
    def setDependencies(self, modules):
        pass
    
    #a-star main-loop
    def findShortestPath(self, start, end, validMoves):
        '''
        Input:
            - start         : start-position(x,y)
            - end           : end-position (x,y)
            - validMoves    : dictionary with valid-moves
                              each key is a node in the maze
                              each value is a list of nodes that can be reached
        Output:
            - The shortest path from 'start' to 'end' [(x1,y1), (x2,y2), ..., (xn,yn)]
            
        Tip:
            - Keep track of all the nodes that already have been visited.
        '''
        pass
    
    # expand the path with a neighbour
    def expandPath(self, estimatedCost, costSoFar, path, lastNode, end, neighbours):
        '''
        Input:
            - estimatedCost : cost made sofar + estimated cost to reach 'end'
            - costSoFar     : cost made sofar
            - path          : List of nodes visited sofar [(x1,y1), (x2,y2), ..., (xn,yn)]
            - lastNode      : last node in 'path' (x,y)
            - end           : goal position (x,y)
            - neighbours    : list with neighbours of current node [(x,y), (x,y), ..., (x,y)]
        Output:
            - List of paths that are extentions of 'path'.
            
        Tip:
            - It can be useful to extend a copy of 'path' with a neighbour.
              You can create a copy of a list with the function list/1. 
              For example: cloneList = list(originalList)
        '''
        pass

    # Get list of neighbours that have not already been visited    
    def getUnseenNeighbors(self, seen, neighbours):
        '''
        Input:
            - seen          : list of nodes already visited/seen [(x,y), (x,y), ..., (x,y)]
            - neighbours    : list with neighbours of current node [(x,y), (x,y), ..., (x,y)]
        Output:
            - List of neibours which have not yet been visited
        '''
        pass

    # A path is finished if the last node is equal to the destination node     
    def finished(self, path, end):
        '''
        Input:
            - path          : a path (a list of tuples)
            - end           : goal-position
        Output:
            - True if path has reached its goal, False otherwise
        '''
        pass

    # Calculate cost to travel between 2 nodes
    def getCost(self, node1, node2):
        '''
        Input:
            - node1         : a node (x1,y1)
            - node2         : a node (x2,y2) 
        Output:
            - Estimated cost to get from node 'node1' to 'node2'
        '''
        pass
    
    #OPTIONAL:
    # Insert the new paths into the priority queue
    def addToQueue(self, queue, newPaths):
        '''
        Input:
            - queue     : A list containing Tuples or Lists sorted in ascending order
                          by the first value of each Tuple/List.
            - newPaths  : List that contains the same datatypes as 'queue' (Tuples or Lists).
        Output:
            - None. (The queue passed to this function will be edited.)
            
        Each path in 'newPaths' is inserted into 'queue' according to its first element.
        Example:
        queue = [(1, ':D'), (3, ':P')]
        newElement = (2, '^_^')
        print 'before: ', queue
        bisect.insort(queue, newElement)
        print 'after: ', queue
        ---------
        before: [(1, ':D'), (3, ':P')]
        after: [(1, ':D'), (2, '^_^'), (3, ':P')]
        '''
        for path in newPaths:
            bisect.insort(queue, path)
            