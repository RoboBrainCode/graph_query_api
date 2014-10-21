# ===========================================================================================
# Description: Parses user input and returns search parameters, which could be [conceptWord], 
# [conceptWord, edge_type], or [conceptWord1, conceptWord2].
# Author: Michela Meister
# ===========================================================================================

import sys
import re
from py2neo import cypher
import nltk
import numpy

# Globals

# edgeWords is the set of words that correspond to specific edge_types    
edgeWords = [{'can', 'use'}, {'correspond', 'corresponds', 'match', 'matches'}, {'to', 'like', 'similar', 'same', 'as'}, {'look', 'taste', 'tastes', 'smell', 'smells', 'looks', 'like', 'appears', 'appearance', 'appear', 'has', 'color'}, {'shape', 'shaped', 'form', 'formed'}, {'consists', 'has', 'part', 'include', 'includes', 'is', 'made', 'of', 'parts', 'ingredient', 'ingredients', 'inside', 'in'}, {'is', 'type', 'of', 'kind', 'version'}, {'can', 'perform', 'action', 'do', 'be', 'used', 'for'}, {'require', 'requires', 'is', 'subtask', 'of', 'need', 'needed', 'to', 'do', 'task', 'step'} ]

# edgeTypeList is the list of edge_types that match with the set of words of the same index in edgeWords
edgeTypeList = ['#can_use', '#corresponds_to', '#similar_to', '#has_appearance', '#has_3dshape', '#has_part', '#is_type_of', '#can_perform_action', '#sub_task_of']

# garbageWords are the words and symbols to remove from user input
garbageWords = {'.', '?', 'is', 'are', 'was', 'were', 'I', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them', 'a', 'an', 'the'}

# Matches tokens to words in edgeWords set in order to choose edge_type.
def chooseEdgeType(tokens):
    i = 0
    maxIndex = -1
    maxPercentage = 0
    for group in edgeWords:
        p = len(list(set(tokens) & set(group)))
	if p > maxPercentage:
	    maxPercentage = p
	    maxIndex = i
	i = i+1
    if (maxIndex == -1):
	return ""
    return edgeTypeList[maxIndex]

# Returns tokens with garbageWords removed.
def removeGarbageWords(tokens):
    garbageList = []
    for word in tokens:
        if word in garbageWords:
            garbageList.append(word)
    for word in garbageList:
        tokens.remove(word)
    return tokens

# returns first noun
def chooseConceptWord(taggedWords):
    for pair in taggedWords:
        if ((pair[1] == 'NN') | (pair[1] == 'NNS')):
            return pair[0]
    return ""

# return second noun
def chooseSecondConceptWord(firstConceptWord, taggedWords):
    for pair in taggedWords:
	if ((pair[1] == 'NN') | (pair[1] == 'NNS')):
	    if (pair[0] != firstConceptWord):
	        return pair[0]
    return ""

def main(args):
    if len(args) != 1:
	print 'This script requires no arguments.'
	sys.exit(-1)
    user_in = raw_input("Write a sentence.\n")
    searchWords = parseThis(user_in)

# Parsing function. Takes in user input and returns search words.
def parseThis(user_in):
    
    # process input
    tokens = nltk.word_tokenize(user_in)
    taggedWords = nltk.pos_tag(tokens)
    print taggedWords
    
    # look for concept words
    searchWords = []
    conceptWord = chooseConceptWord(taggedWords)
    if conceptWord == "":
        return searchWords
    else:
	searchWords = [conceptWord]
	secondConceptWord = chooseSecondConceptWord(conceptWord, taggedWords)
	
    # remove garbage words
    tokens = removeGarbageWords(tokens)
    
    # look for an edge_type
    edge_type = chooseEdgeType(tokens)
    
    # if edge_type found, use it. if no edge_type found, consider second concept word.
    if (edge_type == ""):
	if (secondConceptWord != ""):
	    searchWords = [conceptWord, secondConceptWord]
	    return searchWords
    else:
        searchWords = [conceptWord, edge_type]
    return searchWords

if __name__ == "__main__":
    main(sys.argv)
