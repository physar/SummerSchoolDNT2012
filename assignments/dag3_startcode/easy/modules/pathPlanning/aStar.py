'''
A*
'''
import pygame
import sys
import math
import bisect
import mazeParser

white = (255,255,255)
black = (0,0,0)


class aStar:
    def setDependencies(modules):
        pass
    
    '''
    'pathQueue' is a priority queue containing all the possible paths 
    with their total estimated costs and costs so far.
    Element in queue = (estimatedCost, costSoFar, path)
    Total estimated cost = cost so far + estimated remaining costs
    Elements are sorted in ascending order by their estimated costs.
    '''
    def findShortestPath(self, start, end, validMoves):
        seen = set([]) # unordered collection of distinct hashable objects
        pathQueue = [(self.getCost(start, end), 0, [start])] # initialize pathQueue
        while not self.finished(pathQueue[0], end):        
            pass # implement astar algorithm here
        
        return pathQueue[0]

    # Returns True if the goalnode has been reached,
    # otherwise it returns False   
    def finished(self, (estimatedCost, costSoFar, path), end):
        pass

    # The cost function. Returns the cost between two nodes.
    # Can be implemented using for example Manhattan distance
    def getCost(self, node1, node2):
        pass
        
    # visualize a path
    def visualize(self, screen, edges, (estimatedCost, costSoFar, path), scale=(100,100), offset=(100,100)):
        screen.fill(white)  # reset the canvas
        pathPoints = []
        for node in path:   # draw the path
            pathPoints.append((node[0]*scale[0]+offset[0], node[1]*scale[1]+offset[1]))
        pygame.draw.lines(screen, black, False, pathPoints, 3)
        
        offset = (offset[0]-scale[0]/2, offset[1]-scale[1]/2)
        keys = edges.keys()
        for key in keys:    # draw the maze
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
    parser = mazeParser.mazeParser()
    edges, qrpos, validMoves = parser.parseMaze(filename)
    aStar = aStar()
    path = aStar.findShortestPath((0,0), (3,3), validMoves)
    print path
    # visualize the path
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    screen.fill(white)
    aStar.visualize(screen, edges, path)
    print "finished visualization" 
    
