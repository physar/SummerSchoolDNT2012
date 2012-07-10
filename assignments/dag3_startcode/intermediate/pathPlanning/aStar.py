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
        
    def findShortestPath(self):
        pass    # implement A*
        
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
    path = aStar.findShortestPath()
    print path
    # visualize the path
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    screen.fill(white)
    aStar.visualize(screen, edges, path)
    print "finished visualization" 
    
