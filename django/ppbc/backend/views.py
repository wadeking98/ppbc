from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import json
import requests
from .models import *
import datetime
from .tools import *
import pickle
processes = {}
test_logout = None
test = None

# Create your views here.
def test(request):
    global test
    return HttpResponse(processes.get(request.session.get("wallet")).poll())


def signup(request):
    global test_logout
    if request.method == 'POST':
        data = request.POST

        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password1')

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
        global test
        user_agent = agent(user=u, seed=seed, name=name, wallet_name=wallet_name)
        user_agent.save()
        processes.update({wallet_name:user_agent.start()})
        

        #save the agent process so we can kill it later
        
        # processes.update({wallet_name:proc})

        #register the agent as active
        # act_agent = active_agent(agent=user_agent, login_date=datetime.datetime.now())
        # act_agent.save()
        # act_agent.start()
        
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
        user_agent = agent(user=u, seed=seed, name=name, wallet_name=wallet_name)
        

        #save the agent process so we can kill it later
        proc = user_agent.start()
        processes.update({wallet_name:proc})

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
    global test
    if request.method == 'GET':
        #kill the shell running the docker container
        try:
            proc = processes.get(request.session.get("wallet"))
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=0.5)
                    print(f"Exited with return code {proc.returncode}")
                except subprocess.TimeoutExpired:
                    msg = "Process did not terminate in time"
                    print(msg)
                    raise Exception(msg)
        except KeyError:
            print("key error")
            
        #finally kill the docker container
        try:
            proc = subprocess.Popen([
                "docker", "kill", str(request.session.get("wallet"))
            ])
            proc.wait(timeout=2)
        except:
            print("cannot kill docker container: "+str(request.session.get("wallet")))
        finally:
            proc.terminate()
    return HttpResponse('logout successful')

def list_conn(request):
    #find the current running process
    agent_proc = tools.get_active_agent(request)
    port = agent_proc.outbound_trans
    return HttpResponse(requests.get("http://localhost:"+str(port)+"/connections"))

def list_org(request):
    return HttpResponse(json.dumps(['Faber']))

def list_usr(request):
    return HttpResponse(json.dumps(['Wade']))

def wallet(request):
    return JsonResponse({'wallet':request.session['wallet']})

def conn(request):
    return HttpResponse("hello from conn!")