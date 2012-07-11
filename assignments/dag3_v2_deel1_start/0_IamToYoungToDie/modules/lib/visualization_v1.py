import pygame
white = (255,255,255)
black = (0,0,0)

class visualization_v1:
    def setDependencies(self, modules):
        pygame.init()
        pass
        
    def visualize(self, edges, path, scale=(100,100), offset=(100,100)):
        
        #create canvas
        screen = pygame.display.set_mode((640,480))
        screen.fill(white)
        pathPoints = []
        
        #draw path
        for node in path:
            pathPoints.append((node[0]*scale[0]+offset[0], node[1]*scale[1]+offset[1]))
        pygame.draw.lines(screen, black, False, pathPoints, 3)
        
        #draw maze
        offset = (offset[0]-scale[0]/2, offset[1]-scale[1]/2)
        keys = edges.keys()
        for key in keys:
            keyPoint = (key[0]*scale[0]+offset[0], key[1]*scale[1]+offset[1])
            values = edges[key]
            for value in values:
                valuePoint = (value[0]*scale[0]+offset[0], value[1]*scale[1]+offset[1])
                pygame.draw.lines(screen, black, False, (keyPoint, valuePoint), 1)
        
        pygame.display.update()
        
        # loop, untill screen is closed
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
        
        pygame.quit();