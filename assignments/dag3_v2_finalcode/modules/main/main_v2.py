class main_v2:
    def setDependencies(self, modules):
        self.maze = modules.getModule("mparser")
        self.astar = modules.getModule("astar")
        self.visu = modules.getModule("visualization")

    def start(self):
        self.visu.init()
    
        e, v = self.maze.parseMaze()
        self.maze.prettyPrint(e)
        start = (0,0)
        finish = (0,3)
        pathdata = self.astar.findShortestPath(start, finish, v, e)
        print str(pathdata[2])
        self.visu.visualize(e, pathdata[2], False, start, finish)

        
        
        