from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from algorithms.basic import getManifests, getSingleManifet, getNumberOfContainers, getNumberOfBills, getBills_per_manifest,getManifestsNoAjax
from algorithms.basic import getContainers , getContainers_per_manifest
from algorithms.basic import getBills, getSimpleContainers
from algorithms.basic import getNumberOfManifests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import json , math
from decimal import *

import decimal
from django.utils import simplejson

def json_encode_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")
	
def index(request):
	if request.user.is_authenticated():
		context = RequestContext(request)
		size = getNumberOfManifests()
		pagination = 0 
		pagination = int (math.ceil(size / 20.0))
		pages = range(pagination)
		context_dict = {'number_of_pages': pages}
		return render_to_response('webint/index.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')

def manifests_no_ajax(request):
	if request.user.is_authenticated():
		context = RequestContext(request)
		manif_list = getManifestsNoAjax()
		conta_list = getContainers()
		bills_list = getBills()
		context_dict = {'outer_list': manif_list, 'cont_outer_list': conta_list, 'bills_outer_list': bills_list}
		return render_to_response('webint/manifest_no_ajax.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')

def containers_view(request):
	if request.user.is_authenticated():
		context = RequestContext(request)
		containers_list = getSimpleContainers()
		context_dict = {'cont_list': containers_list}
		return render_to_response('webint/containers.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')

def	bills_view(request):
	if request.user.is_authenticated():
		context = RequestContext(request)
		bill_list = getBills()
		context_dict = {'bill_list': bill_list}
		return render_to_response('webint/bills.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')


def customquerry(request):
	if request.user.is_authenticated():
		context = RequestContext(request)
		context_dict = {}
		return render_to_response('webint/customquerry.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')

def docs(request):
	if request.user.is_authenticated():
		context = RequestContext(request)
		context_dict = {}
		return render_to_response('webint/docs.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')

def mylogin(request):
	context = RequestContext(request)
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST['username']
		password = request.POST['password']
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				print user.first_name 
				login(request, user)
				return HttpResponseRedirect('/webint/')
			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your account is disabled.")
		else:
			# Bad login details were provided. So we can't log the user in.
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	else:
		return render_to_response('webint/login.html', {}, context)

def not_logged_in(request):
	context = RequestContext(request)
	return render_to_response('webint/notloggedin.html', {}, context)

def mylogout(request):
		logout(request)
		return HttpResponseRedirect('/webint/')

def test_view(request):
		context = RequestContext(request)
		context_dict = {}
		return render_to_response('webint/test.html', context_dict, context)

def test_ajax(request, pagenumber):
	if request.user.is_authenticated():
		context = RequestContext(request)
		data = getManifests( int( pagenumber ) )
		return HttpResponse(json.dumps(data), content_type = "application/json")

def ajax_bills_per_manifest(request, pagenumber, manifestID ):
	if request.user.is_authenticated():
		context = RequestContext(request)
		data = getBills_per_manifest( int( pagenumber ), manifestID )
		return HttpResponse(json.dumps(data), content_type = "application/json")

def ajax_conts_per_manifest(request, pagenumber, manifestID ):
	if request.user.is_authenticated():
		context = RequestContext(request)
		data = getContainers_per_manifest( int( pagenumber ), manifestID )
		return HttpResponse(simplejson.dumps(data, default=json_encode_decimal), content_type = "application/json")

def unb_single_manifest_details(request, unbRef):
	if request.user.is_authenticated():
		context = RequestContext(request)
		unbref_id = str(unbRef)

		numberOfContainersPerManifest = getNumberOfContainers(unbref_id)
		numberOfBillsPerManifest =  getNumberOfBills(unbref_id)
		print numberOfContainersPerManifest
		print numberOfBillsPerManifest
		paginationCont = 0
		paginationBill = 0
		paginationCont = int (math.ceil(numberOfContainersPerManifest / 20.0))
		paginationBill = int (math.ceil(numberOfBillsPerManifest / 20.0))
		pagesCont = range(paginationCont)
		pagesBill = range(paginationBill)

		data = getSingleManifet(unbRef)
		context_dict = {'data': data, 'pagesBill' : pagesBill , 'pagesCont' : pagesCont, 'unb' :unbRef}
		return render_to_response('webint/singlemanf.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')


def single_manifest_details(request, manifestID):
	if request.user.is_authenticated():
		context = RequestContext(request)
		manf_id = str(manifestID)

		numberOfContainersPerManifest = getNumberOfContainers(manf_id)
		numberOfBillsPerManifest =  getNumberOfBills(manf_id)
		print numberOfContainersPerManifest
		print numberOfBillsPerManifest
		paginationCont = 0
		paginationBill = 0
		paginationCont = int (math.ceil(numberOfContainersPerManifest / 20.0))
		paginationBill = int (math.ceil(numberOfBillsPerManifest / 20.0))
		pagesCont = range(paginationCont)
		pagesBill = range(paginationBill)

		data = getSingleManifet(manf_id)
		context_dict = {'data': data, 'pagesBill' : pagesBill , 'pagesCont' : pagesCont}
		return render_to_response('webint/singlemanf.html', context_dict, context)
	else:
		return  HttpResponseRedirect('/webint/not_logged_in')



