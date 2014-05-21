from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from algorithms.basic import getManifests
from algorithms.basic import getContainers
from algorithms.basic import getBills
from django.contrib.auth.models import User
from dajaxice.core import dajaxice_functions
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
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

def mylogout(request):
		logout(request)
		return HttpResponseRedirect('/webint/')

def test_view(request):
	if request.method == 'GET':
		GET = request.GET
		print GET
		context = RequestContext(request)
		context_dict = {}
		return render_to_response('webint/test.html', context_dict, context)



