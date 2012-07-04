'''
A*
Michael Cabot
'''
import math
import bisect
import mazeParser

'''
'pathQueue' is a priority queue containing all the possible paths 
with their total estimated costs and costs so far.
Element in queue = (estimatedCost, costSoFar, path)
Total estimated cost = cost so far + estimated remaining costs
Elements are sorted by their estimated costs.
'''
def findShortestPath(start, end, validMoves):
    seen = set([]) # unordered collection of distinct hashable objects
    pathQueue = [(getCost(start, end), 0, [start])] 
    while not finished(pathQueue[0], end):
        (estimatedCost, costSoFar, currentPath) = pathQueue.pop(0)  # pop from queue
        lastNode = currentPath[len(currentPath)-1]
        seen.add(lastNode)
        neighbors = getUnseenNeighbors(seen, validMoves[lastNode])
        if len(neighbors)==0:
            continue
        newPaths = getNewPaths(estimatedCost, costSoFar, currentPath, lastNode, end, neighbors)        
        addToQueue(pathQueue, newPaths) # add to queue
        
    return pathQueue[0]

# expand the path with a neighbor
def getNewPaths(estimatedCost, costSoFar, path, lastNode, end, neighbors):
    newPaths = []
    for neighbor in neighbors:
        newPath = list(path)    # copy the path
        newPath.append(neighbor)
        newCostSoFar =  costSoFar + getCost(lastNode, neighbor)
        newEstimatedCost = newCostSoFar + getCost(neighbor, end)
        newPaths.append((newEstimatedCost, newCostSoFar, newPath))
    return newPaths

# Get list of neighbors that have not already been visited    
def getUnseenNeighbors(seen, neighbors):
    unseenNeighbors = []
    for node in neighbors:
        if not node in seen:
            unseenNeighbors.append(node)
    return unseenNeighbors

# Insert the new paths into the priority queue
def addToQueue(queue, newPaths):
    for path in newPaths:
        bisect.insort(queue, path)

# A path is finished if the last node is equal to the destination        
def finished((estimatedCost, costSoFar, path), end):
    return path[len(path)-1]==end

# Distance between the 2 nodes
def getCost(node1, node2):
    (x1, y1) = node1
    (x2, y2) = node2
    #return math.sqrt((x1-x2)**2 + (y1-y2)**2) # in Euclidean space
    return abs(x1-x2)+abs(y1-y2)

if __name__=="__main__":
    filename="./maze.txt"
    edges, qrpos, validMoves = mazeParser.parseMaze(filename)
    print findShortestPath((0,0), (3,3), validMoves)
