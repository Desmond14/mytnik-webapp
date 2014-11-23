import json
import math
import decimal

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson

from algorithms.basic import get_manifests, get_containers_with_status, get_simple_containers, rule_parser
from algorithms.basic import get_containers, get_containers_per_manifest, get_bills_for_container
from algorithms.basic import get_bills
from webint.models import ContainerStatus


def json_encode_decimal(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    raise TypeError(repr(obj) + " is not JSON serializable")


def update_status(request):
    if request.method == "POST":
        status = ContainerStatus.objects.get(container_id=request.POST['container'])
        new_status_param = request.POST.get('new_status')
        if new_status_param is not None:
            status.status = request.POST['new_status']
            # print "This is update_status"
        else:
            new_assignee = User.objects.get(username=request.POST['new_assignee'])
            print new_assignee.username
            status.assignee = new_assignee
            # print "this is update assignee"
        status.save()
        return HttpResponse(json.dumps(status.status), 'application/json')
    return HttpResponse(status=404)


def manifests(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        context_dict = {}
        return render_to_response('webint/manifests.html', context_dict, context)
    else:
        return HttpResponseRedirect('/webint/not_logged_in')


def manifests_datatables(request):
    if request.user.is_authenticated():
        items_list = get_manifests()
        items_list_dict = {}
        items_list_dict.update({'aaData': items_list})
        return HttpResponse(json.dumps(items_list_dict), 'application/json')


def containers_datatables(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        items_list = get_containers()
        items_list_dict = {}
        items_list_dict.update({'aaData': items_list})
        return HttpResponse(json.dumps(items_list_dict), 'application/json')


def bills_datatables(request):
    if request.user.is_authenticated():
        items_list = get_bills()
        items_list_dict = {}
        items_list_dict.update({'aaData': items_list})
        return HttpResponse(json.dumps(items_list_dict), 'application/json')


def containers_with_status_datatables(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        items_list = get_containers_with_status()
        items_list_dict = {}
        items_list_dict.update({'aaData': items_list})
        return HttpResponse(json.dumps(items_list_dict), 'application/json')


def bills_per_cont_datatables(request, containerID):
    if request.user.is_authenticated():
        items_list = get_bills_for_container(containerID)
        items_list_dict = {}
        items_list_dict.update({'aaData': items_list})
        return HttpResponse(json.dumps(items_list_dict), 'application/json')


def containers_view(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        usernames = User.objects.all().values_list('username', flat=True)
        context_dict = {'users': list(usernames)}
        return render_to_response('webint/containers.html', context_dict, context)
    else:
        return HttpResponseRedirect('/webint/not_logged_in')


def bills_view(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        context_dict = {}
        return render_to_response('webint/bills.html', context_dict, context)
    else:
        return HttpResponseRedirect('/webint/not_logged_in')


def docs(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        context_dict = {}
        return render_to_response('webint/docs.html', context_dict, context)
    else:
        return HttpResponseRedirect('/webint/not_logged_in')


def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                print user.first_name
                login(request, user)
                return HttpResponseRedirect('/webint/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('webint/login.html', {}, context)


def not_logged_in(request):
    context = RequestContext(request)
    return render_to_response('webint/notloggedin.html', {}, context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/webint/')


def bills_per_cont(request, containerID):
    if request.user.is_authenticated():
        context = RequestContext(request)
        context_dict = {'container_id': containerID}
        return render_to_response('webint/bills_per_cont.html', context_dict, context)
    else:
        return HttpResponseRedirect('/webint/not_logged_in')


def alerts(request):
    if request.user.is_authenticated():
        context = RequestContext(request)
        context_dict = {}
        json_data = open('tmp.json').read()
        data = json.loads(json_data)
        context_dict = rule_parser(data)
        return render_to_response('webint/alerts.html', context_dict, context)
    else:
        return HttpResponseRedirect('/webint/not_logged_in')