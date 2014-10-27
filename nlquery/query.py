# ===============================================================
# Description: Rudimentary query system.
# Author: Michela Meister (function get_node from Ayush Dubey) 
# ===============================================================

import sys
import re
from py2neo import cypher
from parser import parseThis
from path import findPath

# Globals
graph_url = "http://ec2-54-187-76-157.us-west-2.compute.amazonaws.com:7474/"

def parse(question):
    return question.split()

# choose search based on token input
def callBestSearch(tokens):
    if len(tokens) > 1:
	if (tokens[1][0] == '#'):
            #find neighbor
    	    return findNeighbor(tokens[0], tokens[1])
	else:
	    return findPath(tokens[0], tokens[1])
    else:
        return get_node(tokens[0])

# Find in and out edges of type edge_type connected to given node.
def findNeighbor(node, edge_type):
    outputString = ""
    session = cypher.Session(graph_url)
    tx = session.create_transaction()
    tx.append("MATCH (n { handle: '" + node + "' })-[e:" + edge_type + "]->nbr "
              "RETURN nbr.handle")
    nbrs = tx.execute()
    assert len(nbrs) == 1
    if len(nbrs) == 1:
    	if len(nbrs[0]) != 0:
            for neighbor in nbrs[0]:
            	outputString += node + ' -- ' + edge_type + ' --> ' + neighbor.values[0] + '\n'
        else:
            outputString += 'No results found.\n'
    else:
	outputString += 'Node ' + node + ' does not exist.\n'    
    return outputString

# Find all media related to node. Returns string for printed output.
def get_node(handle):
    outputString = ""
    session = cypher.Session(graph_url)
    tx = session.create_transaction()

    tx.append("MATCH (n { handle: '" + handle + "' }) "
              "RETURN n.media")

    results = tx.execute()

    assert len(results) == 1
    if len(results[0]) == 1:
        # node exists
        outputString += 'Node ' + handle + ' found.\n'
        outputString += 'Media: ' + str(results[0][0].values[0]) + '\n'
        
        #out-edges
        tx.append("MATCH (n { handle: '" + handle + "' })-[r]->nbr "
                  "RETURN type(r),nbr.handle")
        nbrs = tx.execute()
        assert len(nbrs) == 1
        if len(nbrs[0]) != 0:
            outputString += 'Out edges:\n'
        for pair in nbrs[0]:
            r = pair.values[0]
            nbr = pair.values[1]
	    if r is None:
	        outputString = "edge error\n"
	    else:
                outputString += handle + ' -- ' + r + ' --> ' + nbr + '\n'
        
        #in-edges
        tx.append("MATCH (n { handle: '" + handle + "' })<-[r]-nbr "
                  "RETURN type(r),nbr.handle")
        nbrs = tx.execute()
        assert len(nbrs) == 1
        if len(nbrs[0]) != 0:
            outputString += 'In edges:\n'
        for pair in nbrs[0]:
            r = pair.values[0]
	    nbr = pair.values[1]
	    if r is None:
	        outputString = "edge error\n"
            else:
		outputString += handle + ' <-- ' + r + ' -- ' + nbr + '\n'
    
    else:
        outputString += 'Node ' + handle + ' does not exist.\n'

    tx.commit()
    return outputString

def getTokenString(tokens):
    str = ""
    for t in tokens:
	str += t + " "
    return str

# Query function. Gets user input, parses input, and manages graph search. 
def answerQuestion(user_in):
    output = user_in + "\n"

    #parse question into tokens
    tokens = parseThis(user_in) 

    tokenStr = "[ " + getTokenString(tokens) + "]\n"

    if tokens == []:
        output = "I don't know how to answer that question.\n"
    else:
        #determine best search
        output = callBestSearch(tokens)

    return output

def main(args):
    user_in = raw_input("Ask me a question.\n")
    print answerQuestion(user_in)

if __name__ == "__main__":
    main(sys.argv)
