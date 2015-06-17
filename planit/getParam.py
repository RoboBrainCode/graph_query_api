import pickle
import json
import yaml
import numpy as np
from showheatmap import plot_graph
import os
from weaver import client
c=client.Client('172.31.33.213',2002)
from threading import Lock
heatmapLock=Lock()
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
	with heatmapLock:        
		onehop=c.traverse(activity_name).out_edge({'edgeDirection':'F','label':'ACTIVITY_PARAMS','paramtype':'pi'}).node().execute()
		pi_info=preProcessList(c.get_node(node=onehop[0]).properties)
		onehop=c.traverse(activity_name).out_edge({'edgeDirection':'F','label':'ACTIVITY_PARAMS','paramtype':'human'}).node().execute()	
		human_info=preProcessList(c.get_node(node=onehop[0]).properties)
		onehop=c.traverse(activity_name).out_edge({'edgeDirection':'F','label':'ACTIVITY_PARAMS','paramtype':'object'}).node().execute()
		obj_info=preProcessList(c.get_node(node=onehop[0]).properties)
	print 'Ended weaver query'	
	params=dict()
	params['pi']=pi_info['pi']
	params['human']=parseStrToJson(human_info)
	params['object']=parseStrToJson(obj_info)
	print params
	plot_graph(activity_name,params,path)

# main('dancing')
