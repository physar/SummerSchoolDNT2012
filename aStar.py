'''
A*
Michael Cabot
'''
import pygame
import sys
import math
import bisect
import mazeParser

white = (255,255,255)
black = (0,0,0)

'''
'pathQueue' is a priority queue containing all the possible paths 
with their total estimated costs and costs so far.
Element in queue = (estimatedCost, costSoFar, path)
Total estimated cost = cost so far + estimated remaining costs
Elements are sorted in ascending order by their estimated costs.
'''
def findShortestPath(start, end, validMoves):
    seen = set([]) # unordered collection of distinct hashable objects
    pathQueue = [(getCost(start, end), 0, [start])] # initialize pathQueue
    while not finished(pathQueue[0], end):
        (estimatedCost, costSoFar, currentPath) = pathQueue.pop(0)  # pop from queue
        lastNode = currentPath[len(currentPath)-1]
        seen.add(lastNode)
        neighbors = getUnseenNeighbors(seen, validMoves[lastNode])
        if len(neighbors)==0:   # continue if path cannot be extended
            continue
        newPaths = getNewPaths(estimatedCost, costSoFar, currentPath, lastNode, end, neighbors) # extend path
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

# A path is finished if the last node is equal to the destination node     
def finished((estimatedCost, costSoFar, path), end):
    return path[len(path)-1]==end

# Distance between the 2 nodes
def getCost(node1, node2):
    (x1, y1) = node1
    (x2, y2) = node2
    return abs(x1-x2)+abs(y1-y2) # Manhattan distance
    
# visualize a path
def visualize(screen, edges, (estimatedCost, costSoFar, path), scale=(100,100), offset=(100,100)):
    screen.fill(white)  # reset the canvas
    pathPoints = []
    for node in path:
        pathPoints.append((node[0]*scale[0]+offset[0], node[1]*scale[1]+offset[1]))
    pygame.draw.lines(screen, black, False, pathPoints, 3)
    
    offset = (offset[0]-50, offset[1]-50)
    keys = edges.keys()
    for key in keys:
        keyPoint = (key[0]*scale[0]+offset[0], key[1]*scale[1]+offset[1])
        values = edges[key]
        for value in values:
            valuePoint = (value[0]*scale[0]+offset[0], value[1]*scale[1]+offset[1])
            pygame.draw.lines(screen, black, False, (keyPoint, valuePoint), 1)
    
    pygame.display.update()
    
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit();
            if event.type == pygame.KEYDOWN and event.unicode == 'q':
                loop = False

if __name__=="__main__":
    # find the best path through the maze
    filename="./maze.txt"
    edges, qrpos, validMoves = mazeParser.parseMaze(filename)
    path = findShortestPath((0,0), (3,3), validMoves)
    print path
    # visualize the path
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    screen.fill(white)
    visualize(screen, edges, path)
    print "finished visualization" 
    
