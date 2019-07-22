from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import json
import requests
from .models import *
import datetime
from .tools import *



# Create your views here.
def test(request):
    return HttpResponse(tools.agent_running(request.session.get("wallet")))

def signup(request):
    """
    handles the signup request from the front end

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: {"signup":True} if signup succeded
    """
    if request.method == 'POST':
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password1')

        # create user if not already created
        try:
            #create a user object
            u = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
            u.save()

            #link additional data to user profile
            usr_prof = user_profile(user=u, health_id='1234')
            usr_prof.save()


            seed = tools.id_to_seed(u.id)
            name = first_name
            wallet_name = tools.to_wallet("usr", email)

            #store the user id as a cookie
            request.session['auth'] = True
            request.session['wallet'] = wallet_name
            request.session.set_expiry(0)

            #create an agent for the user
            user_agent = agent(user=u, seed=seed, name=name, wallet_name=wallet_name)
            user_agent.save()
            agent.start("usr", wallet_name)
        except:
            return JsonResponse({"signup":False})
    return JsonResponse({"signup":True})

def org_signup(request):
    """
    handles the sign up request from the front end for organizations

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: {"signup":True} if signup succeeded
    """
    if request.method == 'POST':
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password1')
        org_name = data.get('org_name')
        org_role = data.get('org_role_name')

        try:
            u = User.objects.create_user(username=email, password=password, email=email, first_name=first_name, last_name=last_name)
            u.save()

            o = org_profile(user=u, org_name=org_name, org_role=org_role)
            o.save()


            seed = tools.id_to_seed(u.id)
            name = first_name
            wallet_name = tools.to_wallet("usr", email)

            #store the user id as a cookie
            request.session['auth'] = True
            request.session['wallet'] = wallet_name
            request.session.set_expiry(0)

            #create an agent for the user
            org_agent = agent(user=u, seed=seed, name=name, wallet_name=wallet_name)
            org_agent.save()

            #save the agent process so we can kill it later
            agent.start("usr", wallet_name)
        except:
            return JsonResponse({"signup":False})

    return JsonResponse({"signup":True})

def signin(request):
    """
    Handles the signup request from the frontend
    
    Parameters:
    request (request object): the request send by the front end

    Returns:
    dict: {"login":True} if login succeedes
    """
    if request.method == 'POST':
        ret = {}
        data = request.POST
        alleged_uname = data.get('username')
        alleged_password = data.get('password')

        user = authenticate(username=alleged_uname, password=alleged_password)
        ret['login'] = (user is not None)
        request.session['auth'] = (user is not None)
        request.session.set_expiry(0)

        # TODO error checking (see if agent is already running)
        #get the agent and start it
        agent_obj = agent.objects.get(user=user)
        request.session["wallet"] = agent_obj.wallet_name
        agent.start("usr", agent_obj.wallet_name)
    return JsonResponse(ret)

def logout(request):
    """
    handles the logout request from the front end and 
    kills the running agent

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: {"logut":True} if signup succeded
    """
    if request.method == 'GET':
        agent.kill("usr",request.session["wallet"])
        del request.session["wallet"]
    return JsonResponse({"logout":True})

def list_conn(request):
    """
    lists all the connections for the current user

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON array of all the user connections
    """
    #find the current running process
    agent_proc = get_active_agent(request)
    port = agent_proc.outbound_trans
    return HttpResponse(requests.get("http://localhost:"+str(port)+"/connections"))

def list_org(request):
    """
    lists all the organizations in the database

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON array of all organizations in the database
    """
    #list all organizations
    org_ids = list(org_profile.objects.values_list('user', flat=True))
    orgs = [User.objects.get(id=org_id).__str__() for org_id in org_ids]
    return HttpResponse(json.dumps(orgs))

def list_usr(request):
    """
    lists all the users in the database

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON array of all users in the database
    """
    #list all users
    usr_ids = list(user_profile.objects.values_list('user', flat=True))
    usrs = [User.objects.get(id=usr_id).__str__() for usr_id in usr_ids]
    return HttpResponse(json.dumps(usrs))

def wallet(request):
    """
    returns the wallet name of the current user

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON object containing the wallet name
    """
    return JsonResponse({'wallet':request.session['wallet']})

def conn(request):
    return HttpResponse("hello from conn!")


def get_agent(request):
    return agent.objects.get(wallet_name=request.session["wallet"])

def get_active_agent(request):
    agent_obj = get_agent(request)
    return active_agent.objects.get(agent_id=agent_obj.id)