#############################################
# ReadMe for module-framework               #
#    Date    : May 8th 2012                 #
#    Author  : Hessel van der Molen         #
#    Email   : hmolen.science@gmail.com     #
#############################################

## MODULE-FRAMEWORK
#################

This framework enables system design in modules.
Modules can easily be swapped, updated, removed or replaced without changing the system.


## QUICKSTART
#################
run 'config.py' and the system will start.


## SYSTEM/FILE DEFINITION
#################

#### CONFIG.PY ####

This is the main file of the system. It holds data of all modules available. Each time a new module is made,
it should be registrated in this file. 'config.py' consists mainly of a dictionary. This dictionary is aranged
as follow (the dictionary is called 'moduledict'):

moduledict['<systemNameOfModule>'] = [loadModuleYesOrNo, '<moduleFileName>']
- <systemNameOfModule>  : Is the name of the module in the system. 
                          Referencing to a specific module throughout the system is done using this name
- loadModuleYesOrNo     : Integer, 0 or 1. It defines if a module has to be loaded (1) or not (0)
- <moduleFileName>      : The filename which contains the module. 

Using this setup one can easily replace a module, without adjusting all references in the complete system.
Simply define a different '<moduleFileName>' and a module is swapped/replaced/updated.

A special case in the dictionary is the first entry:
moduledict["main"] = ['<moduleFileName>', '<systemNameOfModule>']
- <systemNameOfModule>  : Is the name of the module in the system. 
                          Referencing to a specific module throughout the system is done using this name
- <moduleFileName>      : The filename which contains the module. 

The module, loaded as "main" is the main file of the system. The module which is defined as "main" is the module
which starts and executes the user defined modules. The framework calls the main module once. After this call
the main-module should do execute the rest.

After the dictionary definitions the framework is started.
With the 'PRINT' parameter the framework prints can be turned on (1) and off (0).


#### MLOADER.PY, MFRAMEWORK.PY (in 'framework/') ####

These files load all modules, they check if the defined modules exist and verify dependencies among modules.
If a module is corrupt, these files will return an exception and terminate the complete framework.
There is no need in adjusting these files. 


#### files in the directory 'modules/' ####

These files are the modules. Modules can be placed in folders to keep overview. The framework checks recursivly if 
folders are defined in the 'modules' directory and will automaticly include these paths.

A modules is a single '.py'-file which contains a class, holding different functions. 
A module in the frame is bound to the following restrictions:

- The name of the '.py'-file should be equal to the class-name of the module
- A module should contain a function called: 'def setDependencies(self, modules):'
    This function is called to set references to other modules, needed by this specific module
    If no dependencies are needed (the module does not need functionality defined elsewhere) the 
    function call is followed by a 'pass' :
    
 ----- module1.py ----- [no dependencies]
class module1():
    def setDependencies(self, modules):
        pass
 ----------------------
 
    If there are dependencies, they should be set in the following way:
    
 ----- module2.py ----- [with dependencies]
class module2():
    moduleA = None
    moduleB = None
    
    def setDependencies(self, modules):
        self.moduleA = modules.getModule('<systemNameOfModuleA>')
        self.moduleB = modules.getModule('<systemNameOfModuleB>')
 ----------------------
 
    the 'modules' class which is passed to 'setDependencies' supports multiple functions to load a module:
    
 ----------------------
        #return list with the names loaded modules (strings)
        #modules.getModules()

        #return pointer to the main module
        #modules.getMainModule()
         
        #return true if module <module> is loaded in dictionary
        #modules.isLoaded(module)

        #return pointer to module with name <module>, throw error if module is not loaded
        #modules.getModule(module)

        #return pointer to module with name <module> or (if not loaded) return None
        #modules.getModuleNone(module)
 ---------------------- 
 
    Calls to a function of a different module are made in the same way when a 'normal' python import
    is done (e.g: 'import moduleA'):
    
 ----------------------
    returndata = self.moduleA.function()
 ----------------------

- The "main"-module should contain a function called "start". This function should start and run the sytem
    build by the user. A main-module thus looks like:
    
 ---- mainmodule.py ---- 
class mainmodule():
    moduleA = None
    moduleB = None
    
    def setDependencies(self, modules):
        self.moduleA = modules.getModule('<systemNameOfModuleA>')
        self.moduleB = modules.getModule('<systemNameOfModuleB>')
        
    def start(self):
        #running system...
        while (bar = true):
            foo = self.moduleA.doBar()
            bar = self.moduleB.getFancyThings(foo)
            x = bar*2 + foo
        # system done...
        
 ----------------------    
 

!!!NOTE!!!!
    Each module is included only once. This means that there is only one copy of each module, which means
        that when some data in moduleA is changed by an moduleB, each module which uses moduleA 
        loses the old data in moduleA. e.g;
        
---- moduleA.py ---- 
class moduleA():
    data = "foo"
    
    def setDependencies(self, modules):
        pass
        
    def getData(self):
        return self.data
    
    def setData(self, data):
        self.data = data
 ----------------------     
    
    moduleC calls 'moduleA.getData()'
            --> return is "foo"
    moduleB calls 'moduleA.setData("bar")
    moduleC calls 'moduleA.getData()' [result is "bar"]
            --> return is "bar"
   
    
## CONTACT
#################

If you found bugs, incorrect coding or if you have questions regarding the described framework and 
its functionality, feel free to contact me:
    
        Hessel van der Molen
        hmolen.science@gmail.com
        
If you have ideas for improvents, need extra features of have other ideas, you can also contact me.

