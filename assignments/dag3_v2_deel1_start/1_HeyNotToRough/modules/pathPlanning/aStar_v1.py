import sys
import math
import bisect

class aStar:
    def setDependencies(self, modules):
        pass
    
    #a-star main-loop
    def findShortestPath(self, start, end, validMoves):
        '''
        Input:
            - start         : start-position(x,y)
            - end           : end-position (x,y)
            - validMoves    : dictionary with valid-mocves
        Output:
            - list with path [(x1,y1), (x2,y2), ..., (xn,yn)]
        '''
        pass
    
    # expand the path with a neighbour
    def getNewPaths(self, estimatedCost, costSoFar, path, lastNode, end, neighbours):
        '''
        Input:
            - estimatedCost : cost to reach end
            - costSoFar     : cost made sofar
            - path          : List of paths walked sofar [path1, path2, ..., pathn]
            - lastNode      : node of current position (x,y)
            - end           : goal position (x,y)
            - neighbours    : list with neighbours of current node [(x,y), (x,y), ..., (x,y)]
        Output:
            - List of paths, extended with current node.
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
        Return:
            - True if path has reached its goal, False otherwise
        '''
        pass

    # Calculate cost to travel between 2 nodes
    def getCost(self, node1, node2):
        '''
        Input:
            - node1         : a node (startnode)
            - node2         : a node (endnode) 
        Output:
            - cost to get from node 'node1' to 'node2'
        '''
        pass
    
    #OPTIONAL:
    # Insert the new paths into the priority queue
    def addToQueue(self, queue, newPaths):
        for path in newPaths:
            bisect.insort(queue, path)