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
## Register modules:
#######

moduledict["main"]          = "main_v3"
moduledict["globals"]       = [1, "globals"]
moduledict["motion"]        = [1, "motion_v1"]
moduledict["tools"]         = [1, "tools_v2"]
moduledict["mparser"]       = [1, "mazeParser_v1"]
moduledict["astar"]         = [1, "aStar"]
moduledict["visualization"] = [1, "visualization_v1"]
moduledict["vision"]        = [1, "visionDag4"]
moduledict["arcode"]        = [1, "getARCode"]
moduledict["behaviour"]     = [0, "behaviour_v1"]


###########################
# start & run framework
###########################
from framework import mframework
mframework.startUpFramework(moduledict, VERBOSE)
