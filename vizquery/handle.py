#! /usr/bin/env python
# 
# ===============================================================
#    Description:  Get a node from the RoboBrain graph backed by
#                  neo4j. 
# 
#        Created:  2014-09-15 21:23:41
# 
#         Author:  Ayush Dubey, dubey@cs.cornell.edu
# 
# Copyright (C) 2013, Cornell University, see the LICENSE file
#                     for licensing agreement
# ===============================================================
# 

import sys
import re
import time
from pprint import pprint
from neo4jrestclient.client import GraphDatabase
from py2neo import cypher
from lxml import html
import requests
import re
import json
import threading
from bottle import route, run, template, hook, response

class parttime_Thread (threading.Thread):
    def __init__(self, threadID, name):
        threading,Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        append(self.threadID)

#These lines are needed for avoiding the "Access-Control-Allow-Origin" errors
@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@route('/get_node/<handle>', method='GET')
def get_node(handle):
    gdb = GraphDatabase("http://ec2-54-187-76-157.us-west-2.compute.amazonaws.com:7474/db/data/")
    url = "http://d1rygkc2z32bg1.cloudfront.net/"
    #q = "MATCH path = (n { handle: '"+handle+"' })-[r*1..3]-(x) RETURN r, n,x, path"
    q = "MATCH (n{handle:'"+handle+"'})-[r]-(x) RETURN r, n,x"
    #q = "MATCH (n{handle:'"+handle+"'})-[r]-(g)-[a]-(x) RETURN r, n,x,g,a"
    result = gdb.query(q=q)
    #pprint(vars(result))
    length = len(result)
    nodes = {}
    links = {}
    id = 0
    for x in range(0,length):
        relationship = result[x][0]
        #for relationship in relationships:
        rel_self = relationship["self"]
        if rel_self not in links:
            metadata = relationship["metadata"]
            type = relationship["metadata"]["type"]
            start = relationship["start"]
            end = relationship["end"]
            links[rel_self] = {"type":type,"start":start,"end":end}

        start_node = result[x][1]
        print start_node
        start_node_self = start_node["self"]
        if start_node_self not in nodes:
            if "mediapath" in start_node["data"]:
                nodes[start_node_self] = {"url":start_node_self, "handle":start_node["data"]["handle"], "mediapath": start_node["data"]["mediapath"]}
            else:
                nodes[start_node_self] = {"url":start_node_self, "handle":start_node["data"]["handle"]}

        end_node = result[x][2]
        end_node_self = end_node["self"]
        if end_node_self not in nodes:
            if "mediapath" in end_node["data"]:
                nodes[end_node_self] = {"url":end_node_self, "handle":end_node["data"]["handle"], "mediapath": url+end_node["data"]["mediapath"]}
            else:
                nodes[end_node_self] = {"url":end_node_self, "handle":end_node["data"]["handle"]}
    return {"nodes":nodes,"links":links}

#run(host='localhost', port=8081)
run(host='ec2-54-148-208-139.us-west-2.compute.amazonaws.com', port=8080)

