from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import getParam as heatMap
from django.http import HttpResponse
import json
import unicodedata

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
		
	# elif request.method == 'GET':
	# 	files = Files.objects.all()
	# 	serializer = FilesSerializer(files)
	# 	return Response(serializer.data)
