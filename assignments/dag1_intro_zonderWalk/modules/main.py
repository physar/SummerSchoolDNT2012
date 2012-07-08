class main:
    def setDependencies(self, modules):
        self.globals = modules.getModule("globals")
        self.motion = modules.getModule("motion")

    def start(self):
        self.globals.setProxies()
        self.globals.speechProxy.say("Hello World")
        self.motion.init()
        self.motion.walkTo(0.5,0,0)