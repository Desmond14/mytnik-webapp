from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from algorithms.basic import getManifests
from algorithms.basic import getContainers
from algorithms.basic import getBills

def index(request):
	context = RequestContext(request)
	context_dict = {'boldmessage': "Developed by Konrad Zuchowicz"}
	return render_to_response('webint/index.html', context_dict, context)
	
def manifest(request):
	context = RequestContext(request)
	manif_list = getManifests()
	conta_list = getContainers()
	bills_list = getBills()
	context_dict = {'outer_list': manif_list, 'cont_outer_list': conta_list, 'bills_outer_list': bills_list}
	return render_to_response('webint/manifest.html', context_dict, context)

def customquerry(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('webint/customquerry.html', context_dict, context)

def docs(request):
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('webint/docs.html', context_dict, context)

