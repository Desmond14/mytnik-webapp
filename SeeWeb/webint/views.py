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
from django.contrib.auth.decorators import login_required


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
            status.save()
        return HttpResponse(json.dumps(status.status), 'application/json')
    return HttpResponse(status=404)


def update_assignee(request):
    if request.method == "POST":
        status = ContainerStatus.objects.get(container_id=request.POST['container'])
        new_assignee = User.objects.get(username=request.POST['new_assignee'])
        if new_assignee is not None:
            status.assignee = new_assignee
            status.save()
        return HttpResponse(json.dumps(status.status), 'application/json')
    return HttpResponse(status=404)


@login_required(login_url="/webint/login/")
def manifests(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('webint/manifests.html', context_dict, context)


def manifests_datatables(request):
    if request.user.is_authenticated():
        items_list = get_manifests()
        items_list_dict = {}
        items_list_dict.update({'aaData': items_list})
        return HttpResponse(json.dumps(items_list_dict), 'application/json')


def containers_datatables(request):
    if request.user.is_authenticated():
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


@login_required
def containers_view(request):
    context = RequestContext(request)
    usernames = User.objects.all().values_list('username', flat=True)
    context_dict = {'users': list(usernames)}
    return render_to_response('webint/containers.html', context_dict, context)


@login_required
def bills_view(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('webint/bills.html', context_dict, context)


@login_required
def docs(request):
    context = RequestContext(request)
    context_dict = {}
    return render_to_response('webint/docs.html', context_dict, context)


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


@login_required
def bills_per_cont(request, containerID):
    context = RequestContext(request)
    context_dict = {'container_id': containerID}
    return render_to_response('webint/bills_per_cont.html', context_dict, context)


@login_required
def alerts(request):
    context = RequestContext(request)
    json_data = open('tmp.json').read()
    data = json.loads(json_data)
    context_dict = rule_parser(data)
    return render_to_response('webint/alerts.html', context_dict, context)


def get_usernames(request):
    usernames = User.objects.all().values_list('username', flat=True)
    return HttpResponse(json.dumps({'users': list(usernames)}), 'application/json')