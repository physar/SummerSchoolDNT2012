class main_v1:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")
        self.tools = modules.getModule("tools")

    def start(self):
        self.globals.setProxies()
        self.motion.init()
        self.tools.cSubscribe()