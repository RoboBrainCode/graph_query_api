from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import getParam as heatMap
from django.http import HttpResponse
import json
import unicodedata
import sys
import os
currdir=os.path.dirname(os.path.realpath(__file__))
print currdir
sys.path.append(currdir)
from planning.PathPlannerSingle import filler
def handle_uploaded_file(f,name):
	with open('file/'+name, 'wb+') as destination:
		for chunk in f.chunks():
			destination.write(chunk)


@api_view(['GET','POST'])
def upload_form(request):
	if request.method == 'POST':
		filename=request.FILES['file'].name
		handle_uploaded_file(request.FILES['file'],filename)
		return Response('uploaded')

def showHeatMap(request):
	if request.method == 'GET':
		query=unicodedata.normalize('NFKD', dict(request.GET)['query'][0]).encode('ascii','ignore').strip()
		heatMap.mainFN(query)
		returnURL="images/planit/heatmap_activity_"+query+".png"
		# print query
	return HttpResponse(json.dumps({'result':returnURL}), content_type="application/json")

def returnTraj(request):
	if request.method=='GET':
		daeFile=unicodedata.normalize('NFKD', dict(request.GET)['daeFile'][0]).encode('ascii','ignore').strip()
		xmlFile=unicodedata.normalize('NFKD', dict(request.GET)['xmlFile'][0]).encode('ascii','ignore').strip()
		parentDir=os.path.abspath(os.path.join(currdir, os.pardir))
		env_colladafile = parentDir+'/file/'+daeFile;
		context_graph = parentDir+'/file/'+xmlFile;
		import random,string
		randomName=''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))+'.pk'
		trajSavePath=os.path.abspath(os.path.join(os.path.abspath(os.path.join(currdir, os.pardir)), os.pardir))+'/Frontend/app/images/TrajXml/'+randomName
		print trajSavePath
		filler(env_colladafile,context_graph,trajSavePath)	
	return HttpResponse(json.dumps({'result':'images/TrajXml/'+randomName}), content_type="application/json")

