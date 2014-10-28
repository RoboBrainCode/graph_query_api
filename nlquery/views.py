# Create your views here.
from django.http import HttpResponse
import json
import numpy as np
import query

def return_nlquery_result(request):
    query_in = request.GET.get('user_in','')
    query_result = query.answerQuestion(query_in)

    json_result = [{'user_out':query_result}]
    return HttpResponse(json.dumps(json_result), content_type="application/json")
