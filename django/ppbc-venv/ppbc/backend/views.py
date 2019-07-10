from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import json
from pbkdf2 import crypt
from .models import *
# Create your views here.
def test(request):
    return HttpResponse(request.session.get('auth', False))

def signup(request):
    if request.method == 'POST':
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password1')
        port = 1234

        u = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
        u.save()

        usr_prof = user_profile(user=u, usr_port=port)
        usr_prof.save()

    return HttpResponse(request.POST['first_name'])

def org_signup(request):
    if request.method == 'POST':
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password1')
        port = 1234
        org_name = data.get('org_name')
        org_role = data.get('org_role_name')

        u = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
        u.save()

        o = org_profile(user=u, org_name=org_name, org_role=org_role, usr_port=port)
        o.save()
    return HttpResponse("hello from org_signup!")

def signin(request):
    if request.method == 'POST':
        ret = {}
        data = request.POST
        alleged_uname = data.get('username')
        alleged_password = data.get('password')

        user = authenticate(username=alleged_uname, password=alleged_password)
        ret['login'] = (user is not None)
        request.session['auth'] = (user is not None)
        request.session.set_expiry(0)
                
    return JsonResponse(ret)

def logout(request):
    if request.method == 'GET':
        try:
            del request.session['auth']
        except KeyError:
            pass
    return HttpResponse('logout successful')

def list_conn(request):
    return HttpResponse(json.dumps([{'wallet':'i_wade_king', 'partner_name':'Faber', 'status':'Active', 'type':'OutBound'}]))

def list_org(request):
    return HttpResponse(json.dumps(['Faber']))

def list_usr(request):
    return HttpResponse(json.dumps(['Wade']))

def wallet(request):
    return JsonResponse({'wallet':'i_wade_king'})

def conn(request):
    return HttpResponse("hello from conn!")