
# =========================================================================
# Description: Returns the path between given two nodes in RoboBrain graph.
# Author: Michela Meister
# =========================================================================

import sys
import re
from py2neo import cypher

# Constants
max_length_path = 15

# Globals
graph_url = "http://ec2-54-187-76-157.us-west-2.compute.amazonaws.com:7474/"

# Function findPath takes in two node handles and attempts to find the shortest path between them.
# If a path exists, the findPath returns the list of nodes along this path. If a path does not exist, 
# findPath returns an empty list. Paths have a length limit of max_length_path.

def findPath(handle_a, handle_b):
    session = cypher.Session(graph_url)
    tx = session.create_transaction()
    
    tx.append("MATCH p = shortestPath((a)-[*.." + str(max_length_path) + "]-(b)) "
	      "WHERE a.handle = '" + handle_a + "' AND b.handle = '" + handle_b + "' "
	      "RETURN extract(n IN nodes(p)|n.handle) AS extracted ")

    results = tx.execute()
    
    # if a path can't be found, return empty list
    outputStr = ""
    if (len(results[0]) < 1):
	outputStr = "I don't know how to answer that question.\n"
	return outputStr

    pathNodes = ""
    for node in results[0][0].values:
	pathNodes = node

    for n in pathNodes:
	outputStr += n + " "
    
    return outputStr

def main(args):
    if len(args) != 3:
	print 'This script requires 2 arguments.'
    path = findPath(args[1], args[2])
    print path

if __name__ == "__main__":
    main(sys.argv)
