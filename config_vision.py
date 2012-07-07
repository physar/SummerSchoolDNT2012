# @file config.py
# @func module definitions for framework. 
#       Is used to register, define & load modules 
#       Starts the main-framework
# @auth Hessel van der Molen
#       hmolen.science@gmail.com
# @date 4 may 2012

#dictionairy for module
moduledict = {}
#show frameworks print's (1=show, 0=do not show)
VERBOSE = 1


####
## system modules, pre-defined implementations
#######

#main module:   connects all modules to each other
moduledict["main"]          = "main_vision"
#tools module:  contains some pre-defined tools which can be used
moduledict["tools"]         = [1, "tools_v1"]
#motion module: contains pre-defined motion patterns
moduledict["motion"]        = [1, "motion_v1"]
#global module: contains global data
moduledict["globals"]        = [1, "globals"]

####
## user modules, to be implemented
#######

#Definition of code:
#moduledict[<systemHandler>]   = [load(True/False), <filename>]
# - <systemHandler>     name used in system to refer to module
# - load(True/False)    load (1) or do not load (0) module in framework
# - <filename>          name of file/class (without.py)


###########################
# start & run framework
###########################
from framework import mframework
mframework.startUpFramework(moduledict, VERBOSE)