from django.http import HttpResponse
import json
from threading import Lock
from weaverGetNode import *
clientLock=Lock()
import unicodedata
def getNode(request):
	val=unicodedata.normalize('NFKD', dict(request.GET)['query'][0]).encode('ascii','ignore').strip()
	number=int(unicodedata.normalize('NFKD', dict(request.GET)['number'][0]).encode('ascii','ignore'))
	overwrite=int(unicodedata.normalize('NFKD', dict(request.GET)['overwrite'][0]).encode('ascii','ignore'))
	direction=str(unicodedata.normalize('NFKD', dict(request.GET)['directionVal'][0]).encode('ascii','ignore'))

	with clientLock:
		result=getNodeEdge(name=val,num=number,directionVal=direction)
	for i in range(0,len(result['nodes'])):
		print result['nodes'][i]['handle']
		print result['nodes'][i]['id']
	if result:
		result['nodes'][0]['root']='true'
	else:
		result={}
	return HttpResponse(json.dumps(result), content_type="application/json")
