from django.http import HttpResponse
from neo4jrestclient.client import GraphDatabase
import json
import gc
import requests

# Create your views here.
def get_node(request):
    handle = request.GET.get('handle','shoe')

    gdb = GraphDatabase("http://ec2-54-187-76-157.us-west-2.compute.amazonaws.com:7474/db/data/")
    url = "http://d1rygkc2z32bg1.cloudfront.net/"
    #q = "MATCH path = (n { handle: '"+handle+"' })-[r*1..3]-(x) RETURN r, n,x, path"
    q = "MATCH (n{handle:'"+handle+"'})-[r]-(x) RETURN r, n,x"
    #q = "MATCH (n{handle:'"+handle+"'})-[r]-(g)-[a]-(x) RETURN r, n,x,g,a"
    #result = gdb.query(q=q)
    result = requests.post(gdb._transaction + '/commit',
            data=json.dumps({'statements': [{
                'statement': "MATCH (n{handle:'"+handle+"'})-[r]-(x) RETURN r,n,x"}]
                }),
            headers={
                'Accept': 'application/json; charset=UTF-8',
                'Content-Type': 'application/json'
                }).json();
    result = result['results'][0]        
    result = result['data']                
    length = len(result)
    nodes = {}
    links = {}
    id = 0
    for x in range(0,length):
        tuple = result[x]['row']
        start_node = tuple[1]
        end_node = tuple[2]
        #for relationship in relationships:
        rel_self = "link-"+start_node["handle"]+"-"+end_node["handle"]
        if rel_self not in links:
            links[rel_self] = {"type":"BLANK","start":start_node['handle'],"end":end_node['handle']}                                                                                                    
            
        if start_node['handle'] not in nodes:       
            if "mediapath" in start_node:   
                nodes[start_node['handle']] = {"url":"a","handle":start_node["handle"], "mediapath": start_node["mediapath"]}
            else:
                nodes[start_node['handle']] = {"url":"a","handle":start_node["handle"]}
        end_node_self = end_node["handle"]
        if end_node_self not in nodes:  
            if "mediapath" in end_node:     
                nodes[end_node_self] = {"url":"a","handle":end_node["handle"], "mediapath": url+end_node["mediapath"]}                                                                                                                                                                          
            else:
                nodes[end_node_self] = {"url":"a","handle":end_node["handle"]}                                                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                        

    json_result = {"nodes":nodes,"links":links}
    del result
    gc.collect()
    return HttpResponse(json.dumps(json_result), content_type="application/json")
