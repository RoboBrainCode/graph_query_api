# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from serializer import FeedBackSerializer
from datetime import datetime  
from models import e2eFeedback  
from rest_framework import permissions
import yaml,json
@api_view(['GET'])
def feedbackSys(request):
	if request.method == 'GET':
		data=yaml.safe_load(request.body)
		serializer = FeedBackSerializer(data=data)
		if serializer.is_valid():
			feedback=e2eFeedback()
			objList=feedback.__class__.objects.all().filter(feedId=data['feedId'])
			print objList
			if (len(objList)>0):
				pass
			else:
				serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Records upvotes for a feed
def countUpvotes(request):
	print request.method
	if request.method == 'GET':
		data=dict(request.GET)
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)
		for key,val in data.iteritems():
			data[key]=val[0]
		payload=data
		feedid = payload['feedid']
		vote_dir = int(payload['vote'])
		change = payload['change']
		if not feedid:
			error_response = {
				'Error': 'No feedid provided'
			}
			return HttpResponse(json.dumps(error_response), content_type='application/json')
		if not vote_dir == -1 and not vote_dir == 1:
			error_response = {
				'Error': 'voteid {0} not provided. Can only be 1 or -1'.format(vote_dir)
			}
			return HttpResponse(json.dumps(error_response), content_type='application/json')

		feedback= e2eFeedback.objects.get(id=feedid)
		votes = {}
		if vote_dir == 1:
			feedback.upvotes += 1
			if change=='true':
				feedback.downvotes -= 1
		if vote_dir == -1:
			feedback.downvotes += 1
			if change=='true':
				feedback.upvotes -= 1
		votes = {
			'upvotes': max(feedback.upvotes, 0),
			'downvotes': max(feedback.downvotes, 0)
		}
		feedback.save()

		return HttpResponse(json.dumps(votes), content_type='application/json')

def recordFeedback(request):
	if request.method == 'GET':
		data=dict(request.GET)
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)
		for key,val in data.iteritems():
			data[key]=val[0]
		payload=data
		feedid=payload['feedid']
		tellmedaveFeedback = payload['tellmedave']
		planitFeedback= payload['planit']
		if not feedid:
			error_response = {
				'Error': 'No feedid provided'
			}
			return HttpResponse(json.dumps(error_response), content_type='application/json')

		feedback= e2eFeedback.objects.get(id=feedid)
		
		if tellmedaveFeedback:
			feedback.tellmedaveFeedback.append(tellmedaveFeedback)
		if planitFeedback:
			feedback.planitFeedback.append(planitFeedback)

		feedback.save()

		return HttpResponse(json.dumps({'success':1}), content_type='application/json')


def returnTopFeeds(request):
	# Number of feeds required
	if request.method == 'GET':
		data = yaml.safe_load(request.body)
		number=data.get('num',10)
		max_len = e2eFeedback.objects.count()
		upper_limit = min(max_len, number)
		feedList = e2eFeedback.objects.order_by('id')[:upper_limit]
		json_feeds = [feed.to_json() for feed in feedList]
		return HttpResponse(json.dumps(json_feeds), content_type="application/json")


# This function allows infinite scrolling.
def addMoreFeeds(request):
	if request.method == 'GET':
		data=dict(request.GET)
		json_data=json.dumps(data)
		data=yaml.safe_load(json_data)
		for key,val in data.iteritems():
			data[key]=val[0]
		# Feeds already present
		current_feeds = int(data.get('current','10')) # default cur=10

		# Number of extra feeds required
		extra_feeds = int(data.get('num','10')) # default k=10

		max_len = e2eFeedback.objects.count()
		upper_limit = min(max_len, current_feeds + extra_feeds)


		feedList = e2eFeedback.objects.order_by('id')[current_feeds:upper_limit]
		json_feeds = [feed.to_json() for feed in feedList]

		return HttpResponse(json.dumps(json_feeds), content_type="application/json")





