import pygame, time
white = (255,255,255)
black = (  0,  0,  0)
red   = (255,  0,  0)
green = (  0, 255, 0)

class visualization_v1:
    def setDependencies(self, modules):
        pass

    def init(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640,480))

    def visualize(self, edges, path, update, start, end, scale=(100,100), offset=(100,100)):
        #reset canvas
        self.screen.fill(white)
        pathPoints = []
        
        #draw path
        for node in path:
            pathPoints.append((node[0]*scale[0]+offset[0], node[1]*scale[1]+offset[1]))
        if (len(pathPoints) > 1):
            pygame.draw.lines(self.screen, black, False, pathPoints, 3)
        
        #draw start + end point
        pygame.draw.circle(self.screen, green, (start[0]*scale[0]+offset[0], start[1]*scale[1]+offset[1]), 5, 2)
        pygame.draw.circle(self.screen, red, (end[0]*scale[0]+offset[0], end[1]*scale[1]+offset[1]), 5, 2)
        
        #draw maze
        offset = (offset[0]-scale[0]/2, offset[1]-scale[1]/2)
        keys = edges.keys()
        for key in keys:
            keyPoint = (key[0]*scale[0]+offset[0], key[1]*scale[1]+offset[1])
            values = edges[key]
            for value in values:
                valuePoint = (value[0]*scale[0]+offset[0], value[1]*scale[1]+offset[1])
                pygame.draw.lines(self.screen, black, False, (keyPoint, valuePoint), 1)
        
        #update canvas
        pygame.display.update()
        
        # loop, untill screen is closed or 
        loop = True
        while loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False
                
                if (update == True) and (event.type == pygame.KEYDOWN and event.unicode == 'c'):
                    loop = False

        if (update == False):
            pygame.quit()