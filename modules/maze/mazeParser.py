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
    def setDependencies(self, modules):
        pass
        
    def parseMaze(self, filename="./maze.txt"):
        """
        parseMaze(filename) -> dict Edges.
        
        Creates a dictionary in which edges are represented as collections
        of tuples, indicating to which nodes each node is connected. 
        """

        # read data from the file
        data_file = open(filename, 'r')
        data = data_file.readlines()
        
        # create a dictionary of edges and valid moves.
        edges = dict()
        validMoves = {}
        
        # init vars
        start = 1
        y = 0
        
        # for every position in the maze
        for lineNr in xrange(len(data)):
            # if a line containing | and digits
            if lineNr % 2 == 1:
                # parse each token seperately
                for t in xrange(0, len(data[lineNr][:-1]), 2):
                    token = data[lineNr][t]
                    if token == "|":
                        self.addEdge(edges, (t/2, y+1), (t/2, y  ))
                    elif token == " ":
                        self.addEdge(validMoves, (t/2, y), (t/2-1, y))
            else:
                # else, look at each second (namely the '-')
                for t in xrange(start, len(data[lineNr][:-1]), 2):           
                    token = data[lineNr][t]
                    # parse the tokens correctly
                    if token == "-":
                        self.addEdge(edges, (t/2+1, y), (t/2,   y))
                    if token == " ":
                        self.addEdge(validMoves, (t/2, y), (t/2, y-1))
            # start is either 0 or 1        
            start = (start == 0)
            # increment y
            if start == 1:
                y += 1
                
        print "e:", edges
        print "v:", validMoves
        return edges, validMoves
                    
    def addEdge(self, edgeDict, node1, node2):
        """
        addEdge(dictionary, node1, node2)
        
        Add an edge to the dictionary between inputnodes,
        both edge(node1, node2) and edge(node2, node1)
        """
        if node1 in edgeDict:
            edgeDict[node1] += [node2]
        else:
            edgeDict[node1] = [node2]
        if node2 in edgeDict:
            edgeDict[node2] += [node1]
        else:
            edgeDict[node2] = [node1]
            
    def prettyPrint(self, edges, qrpos):
        """
        prettyPrint(dict edges, dict qrpositions)
        
        Prints the maze and qr points in a fashionable way.
        """
        max_x, max_y = max(edges.keys())
        print max_x, max_y
        
        for y in range(max_y*2+1):
            if y % 2 == 0:
                if (y == 0):
                    sys.stdout.write('  ')      
                    for i in range(max_x):
                        sys.stdout.write(' '+ str(i))
                    sys.stdout.write('\n')      
                sys.stdout.write('  .')                    
                for x in range(max_x):
                    if (x+1, y/2) in edges[(x,y/2)]:
                        sys.stdout.write('-')
                    else:
                        sys.stdout.write(' ')
                    sys.stdout.write('.')
                print ''
            else:      
                sys.stdout.write(str(y/2) + " ")
                for x in range(max_x + 1):
                    if (x, y/2+1) in edges[(x,y/2)]:
                        sys.stdout.write('|')
                    else:
                        sys.stdout.write(' ')
                    if (x,y/2) in qrpos:
                        sys.stdout.write(str(qrpos[(x,y/2)]))
                    else:
                        sys.stdout.write(' ')
                print ''
                    
if __name__ == "__main__":
    parser = mazeParser()
    edges, validMoves = parser.parseMaze()
    for move in validMoves:
        print move, ":\t", validMoves[move]
    print validMoves
    
    
    #for edge in edges:
    #    print edge, edges[edge]
    #print '\n', qrpos
    parser.prettyPrint(edges, {1})
