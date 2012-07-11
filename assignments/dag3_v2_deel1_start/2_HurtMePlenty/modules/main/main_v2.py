class main_v2:
    def setDependencies(self, modules):
        self.maze = modules.getModule("mparser")
        self.astar = modules.getModule("astar")
        self.visu = modules.getModule("visualization")

    def start(self):
        self.visu.init()