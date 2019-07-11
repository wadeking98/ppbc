from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import json
from .models import *
import datetime
# Create your views here.
def test(request):
    return HttpResponse(request.session.get('auth', False))

def start_agent(agent, active):
    print(agent)
    p = subprocess.Popen([os.path.join("../../","run_agent"), 
    ""+str(active.outbound_trans), 
    ""+str(active.inbound_trans),
    ""+str(agent.seed),
    ""+str(agent.name),
    ""+str(agent.wallet_name),
    "../../scripts/"], stdout=subprocess.PIPE)


def signup(request):
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


        seed = "00000000000000000000000000000000"
        name = first_name
        wallet_name = 'i_'+email.replace('@', '_').replace('.','_')

        #store the user id as a cookie
        request.session['auth'] = True
        request.session['wallet'] = wallet_name
        request.session.set_expiry(0)

        #create an agent for the user
        user_agent = agent(user=u, seed=seed, name=name, wallet_name=wallet_name)
        user_agent.save()

        #register the agent as active
        act_agent = active_agent(agent=user_agent, login_date=datetime.datetime.now())
        act_agent.save()
        act_agent.start()
        
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
            #remove the authenticaiton cookie
            #del request.session['auth']

            #get the active agent and kill the process and remove it from running agents
            # agent_obj = agent.objects.get(wallet_name=request.session['wallet'])
            # agent_proc = agent.objects.get(id=agent_obj.id)
            # agent_proc.kill()
            # agent_proc.delete()
            # print(agent_proc)
        except KeyError:
            print("key error")
    return HttpResponse('logout successful')

def list_conn(request):
    return HttpResponse(json.dumps([{'wallet':'i_wade_king', 'partner_name':'Faber', 'status':'Active', 'type':'OutBound'}]))

def list_org(request):
    return HttpResponse(json.dumps(['Faber']))

def list_usr(request):
    return HttpResponse(json.dumps(['Wade']))

def wallet(request):
    return JsonResponse({'wallet':request.session['wallet']})

def conn(request):
    return HttpResponse("hello from conn!")