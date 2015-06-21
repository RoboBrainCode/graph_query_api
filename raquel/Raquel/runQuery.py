from weaverParser import cyParser
# from weaverWrapperFns import*
# from threading import Lock
# weaverLock=Lock()
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



def runQuery(cypherQuery):
	# print 'we are here'
	# print cypherQuery
	start=cypherQuery.find('MATCH')
	end=cypherQuery.find('RETURN')
	end_2=cypherQuery.find('LIMIT')
	query=cypherQuery[start+5:end].strip()
	args=cypherQuery[end+6:end_2].strip()
	args=args.split(',')
	if len(args)>1:
		print 'Not Supported'
		return False
	
	# print query
	# cyParser(query)
	funcNum, dict_s, propertyList, dict_e = cyParser(query)
	# print funcNum, dict_s,propertyList,dict_e
	if funcNum == 0:
		# print funcNum
		fnName='returnNodeOneHopForward'
		params=dict(src=dict_s['handle'],properties={})
		result=PostWeaverQuery(fnName,params)
		return result
	elif funcNum == 1:
		# print funcNum
		fnName='returnNodeOneHopForward'
		params=dict(src=dict_s['handle'],properties=propertyList)
		result=PostWeaverQuery(fnName,params)
		return result
		# return returnNodeOneHopForward(dict_s['handle'],propertyList)
	elif funcNum == 2:
		# print funcNum
		fnName='returnNodeOneHopBackward'
		params=dict(src=dict_e['handle'],properties={})
		result=PostWeaverQuery(fnName,params)
		return result
		# return returnNodeOneHopBackward(dict_e['handle'],{})
		# return '2'
	elif funcNum == 3:
		# print funcNum
		fnName='returnNodeOneHopBackward'
		params=dict(src=dict_e['handle'],properties=propertyList)
		result=PostWeaverQuery(fnName,params)
		return result

		# return returnNodeOneHopBackward(dict_e['handle'],propertyList)
		# return '3'
	elif funcNum == 4:
		# print funcNum
		print dict_s['handle'],dict_e['handle']
		# return returnPathMinMax(src=dict_s['handle'],dest=dict_e['handle'],path_len_min=1,path_len_max=1)	
	elif funcNum == 5:
		# print funcNum
		fnName='returnPathMinMax'
		params=dict(src=dict_s['handle'],dest=dict_e['handle'],path_len_min=propertyList['start'],path_len_max=propertyList['end'])
		result=PostWeaverQuery(fnName,params)
		return result

		
		
	elif funcNum ==6:
		# print funcNum
		fnName='returnNodesForward'
		params=dict(src=dict_s['handle'],path_len_min=propertyList['start'],path_len_max=propertyList['end'])
		result=PostWeaverQuery(fnName,params)
		return result

		# return returnNodesForward()
	elif funcNum==7:
		fnName='returnNodesBackward'
		params=dict(src=dict_e['handle'],path_len_min=propertyList['start'],path_len_max=propertyList['end'])
		result=PostWeaverQuery(fnName,params)
		return result

		# print funcNum
		# return returnNodesBackward(src=dict_e['handle'],path_len_min=propertyList['start'],path_len_max=propertyList['end'])
		# return '4'
	elif funcNum==8:

		fnName='getNode'
		params=dict(node=dict_s['handle'])
		result=PostWeaverQuery(fnName,params)
		return result
		# print funcNum, dict_s, propertyList, dict_e
		# return getNode(src=dict_s['handle'])
	else:
		return 'invalid_input'

	return True


if __name__ == "__main__":
	runQuery("MATCH ({handle:'phone'})")
	# runQuery("MATCH ({handle:'wall'})-[]->(e) RETURN e")

