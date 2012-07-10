# Maze represented as a graph:
# 1. nodes represented by tuple containing (x, y).
# 2. edges represented by locations of neighbours with which they are connected.

# example maze
# . .-.-.-.
# | |     |
# . .-. .-.
# |       |
# .-.-.-. .

import sys

class mazeParser:
    def setDependencies(modules):
        pass
        
    def parseMaze(self, filename="./maze.txt"):
        pass
                    
    
                    
if __name__ == "__main__":
    parser = mazeParser()
    edges, qrpos, validMoves = parser.parseMaze()
    for move in validMoves:
        print move, ":\t", validMoves[move]
    print validMoves
    #for edge in edges:
    #    print edge, edges[edge]
    #print '\n', qrpos
    #parser.prettyPrint(edges, qrpos)
