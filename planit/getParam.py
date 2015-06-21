import pickle
import json
import yaml
import numpy as np
from showheatmap import plot_graph
import os

import urllib,requests
import ast
def PostWeaverQuery(fnName,params):
		query=dict(fnName=fnName,params=params)
		myport=3232
		data=json.dumps(query)
		myURL = "http://127.0.0.1:%s/weaverWrapper/execFn/" % (myport)
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.get(myURL, data=data,headers=headers)
		response=yaml.safe_load(r.text)
		return response




# from weaver import client
# c=client.Client('172.31.33.213',2002)
# from threading import Lock
# heatmapLock=Lock()
def parseStrToJson(varDict):
	newDict=dict()
	for key,val in varDict.iteritems():
		val=val.split(',')
		try:
			for i in range(len(val)):
				val[i]=float(val[i])
		except:
			print key,val
		else:
			if (len(val)>1):
				val=np.asarray(val)
			else:
				val=val[0]
			newDict[key]=val
	return newDict


def preProcessList(newDict):
	for key,val in newDict.iteritems():
		newDict[key]=val[0]
	return newDict

def mainFN(activity_name):
	currDirectory=os.path.dirname(os.path.realpath(__file__))
	path=os.path.abspath(os.path.join(os.path.abspath(os.path.join(currDirectory, os.pardir)), os.pardir))+'/Frontend/app/images/planit'
	json_data=open(currDirectory+"/support/json/"+activity_name+".json").read()
	data=yaml.safe_load(json_data)
	print 'Started weaver query'
	
	fnName='oneHop'
	params=dict(node=activity_name,edgeProps={'edgeDirection':'F','label':'ACTIVITY_PARAMS','paramtype':'pi'})
	onehop=PostWeaverQuery(fnName,params)
	pi_info=preProcessList(c.get_node(node=onehop[0]).properties)
		
	fnName='oneHop'
	params=dict(node=activity_name,edgeProps={'edgeDirection':'F','label':'ACTIVITY_PARAMS','paramtype':'human'})
	onehop=PostWeaverQuery(fnName,params)	
	human_info=preProcessList(c.get_node(node=onehop[0]).properties)
	
	fnName='oneHop'
	params=dict(node=activity_name,edgeProps={'edgeDirection':'F','label':'ACTIVITY_PARAMS','paramtype':'object'})
	onehop=PostWeaverQuery(fnName,params)	
	obj_info=preProcessList(c.get_node(node=onehop[0]).properties)

	params=dict()
	params['pi']=pi_info['pi']
	params['human']=parseStrToJson(human_info)
	params['object']=parseStrToJson(obj_info)
	print params
	plot_graph(activity_name,params,path)

# main('dancing')
