import sys
import math
import bisect

class aStar:
    def setDependencies(self, modules):
        self.visu = modules.getModule("visualization")
        
    def findShortestPath(self, start, end, validMoves, edges):
        seen = set([]) # unordered collection of distinct hashable objects
        pathQueue = [(self.getCost(start, end), 0, [start])] # initialize pathQueue
        while not self.finished(pathQueue[0], end):
            (estimatedCost, costSoFar, currentPath) = pathQueue.pop(0)  # pop from queue
            
            self.visu.visualize(edges, currentPath, True, start, end)
            
            lastNode = currentPath[len(currentPath)-1]
            seen.add(lastNode)
            neighbors = self.getUnseenNeighbors(seen, validMoves[lastNode])
            if len(neighbors)==0:   # continue if path cannot be extended
                continue
            newPaths = self.getNewPaths(estimatedCost, costSoFar, currentPath, lastNode, end, neighbors) # extend path
            self.addToQueue(pathQueue, newPaths) # add to queue        
               
        return pathQueue[0]

    # expand the path with a neighbor
    def getNewPaths(self, estimatedCost, costSoFar, path, lastNode, end, neighbors):
        newPaths = []
        for neighbor in neighbors:
            newPath = list(path)    # copy the path
            newPath.append(neighbor)
            newCostSoFar =  costSoFar + self.getCost(lastNode, neighbor)
            newEstimatedCost = newCostSoFar + self.getCost(neighbor, end)
            newPaths.append((newEstimatedCost, newCostSoFar, newPath))
        return newPaths

    # Get list of neighbors that have not already been visited    
    def getUnseenNeighbors(self, seen, neighbors):
        unseenNeighbors = []
        for node in neighbors:
            if not node in seen:
                unseenNeighbors.append(node)
        return unseenNeighbors

    # Insert the new paths into the priority queue
    def addToQueue(self, queue, newPaths):
        for path in newPaths:
            bisect.insort(queue, path)

    # A path is finished if the last node is equal to the destination node     
    def finished(self, (estimatedCost, costSoFar, path), end):
        return path[len(path)-1]==end

    # Distance between the 2 nodes
    def getCost(self, node1, node2):
        (x1, y1) = node1
        (x2, y2) = node2
        return abs(x1-x2)+abs(y1-y2) # Manhattan distance