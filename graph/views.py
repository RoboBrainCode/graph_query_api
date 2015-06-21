# from threading import Lock
# from weaverGetNode import *
# clientLock=Lock()
from django.http import HttpResponse
import json
import yaml
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

import unicodedata
def getNode(request):
	val=unicodedata.normalize('NFKD', dict(request.GET)['query'][0]).encode('ascii','ignore').strip()
	number=int(unicodedata.normalize('NFKD', dict(request.GET)['number'][0]).encode('ascii','ignore'))
	overwrite=int(unicodedata.normalize('NFKD', dict(request.GET)['overwrite'][0]).encode('ascii','ignore'))
	direction=str(unicodedata.normalize('NFKD', dict(request.GET)['directionVal'][0]).encode('ascii','ignore'))

	fnName='oneHopGraphml'
	edgeProps=dict(edgeDirection='F')
	params=dict(name=val,num=number,edgeProps=edgeProps)
	result=PostWeaverQuery(fnName,params)
	# with clientLock:
	# 	result=getNodeEdge(name=val,num=number,directionVal=direction)
	# for i in range(0,len(result['nodes'])):
	# 	print result['nodes'][i]['handle']
	# 	print result['nodes'][i]['id']
	if result:
		result['nodes'][0]['root']='true'
	else:
		result={}
	return HttpResponse(json.dumps(result), content_type="application/json")
