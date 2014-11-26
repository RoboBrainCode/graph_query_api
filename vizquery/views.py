from django.http import HttpResponse
from neo4jrestclient.client import GraphDatabase
import json

# Create your views here.
def get_node(request):
    handle = request.GET.get('handle','shoe')

    gdb = GraphDatabase("http://ec2-54-187-76-157.us-west-2.compute.amazonaws.com:7474/db/data/")
    url = "http://d1rygkc2z32bg1.cloudfront.net/"
    #q = "MATCH path = (n { handle: '"+handle+"' })-[r*1..3]-(x) RETURN r, n,x, path"
    q = "MATCH (n{handle:'"+handle+"'})-[r]-(x) RETURN r, n,x"
    #q = "MATCH (n{handle:'"+handle+"'})-[r]-(g)-[a]-(x) RETURN r, n,x,g,a"
    result = gdb.query(q=q)
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
    json_result = {"nodes":nodes,"links":links}
    return HttpResponse(json.dumps(json_result), content_type="application/json")
