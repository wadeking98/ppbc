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

def webhook(request):
    if request.method == 'POST':
        print(request.POST.text)
        return HttpResponse(request.POST.text)

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
            register_seed(request)
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
            register_seed(request)
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

        #get the agent and start it
        agent_obj = agent.objects.get(user=user)
        request.session["wallet"] = agent_obj.wallet_name
        register_seed(request)
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
    orgs = [[org_id,User.objects.get(id=org_id).__str__()] for org_id in org_ids]
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
    usrs = [[usr_id,User.objects.get(id=usr_id).__str__()] for usr_id in usr_ids]
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

def get_invite(request):
    """
    NOT AN API SERVICE
    creates an invitation and returns the invitation json

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON object defining the invitation
    """
    agent_proc = get_active_agent(request)
    port = agent_proc.outbound_trans
    return requests.post("http://localhost:"+str(port)+"/connections/create-invitation").json()


def del_conn(request):
    """
    deletes a specified user connection

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON object containing the wallet name
    """
    if request.method == 'POST':
        data = request.POST
        conn_id = data.get('conn_id')
        agent_proc = get_active_agent(request)
        port = agent_proc.outbound_trans
        requests.post("http://localhost:"+str(port)+"/connections/"+str(conn_id)+"/remove")
        return HttpResponse("hello")


def send_msg(request):
    """
    sends a message to a user

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: placeholder for now
    """
    if request.method == 'POST':
        data = request.POST
        conn_id = data.get('conn_id')
        msg = {"content":str(data.get('msg'))}
        agent_proc = get_active_agent(request)
        port = agent_proc.outbound_trans
        requests.post("http://localhost:"+str(port)+"/connections/"+str(conn_id)+"/send-message", data=json.dumps(msg))
        return HttpResponse("hello")


def send_invite(request):
    """
    automatically connects two users, even if one is offline

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    if request.method == 'POST':
        #get the post data
        data = request.POST
        usr_id = data.get('user')

        #find the agent recieving the connection
        usr = User.objects.get(id=usr_id)
        agent_obj = agent.objects.get(user=usr)
        wallet = agent_obj.wallet_name

        #mark this agent as allocated to the server
        agent.start(agent_type="srv", wallet_name=request.session.get('wallet'))
        #start or find the running aries agent
        agent.start(agent_type="srv", wallet_name=wallet)
        act_agent_obj = active_agent.objects.get(agent=agent_obj)
        port = act_agent_obj.outbound_trans

        #get the invitation json
        invite = get_invite(request)
        print(invite.get('invitation'))

        #wait for the aries agent to come online and send invitation
        response = agent.try_post(url="http://localhost:"+str(port)+"/connections/receive-invitation",data=json.dumps(invite.get('invitation')))
        conn_id = response.json().get('connection_id')
        # TODO wait until connection is active before killing server-agent process
        agent.wait_until_conn(url="http://localhost:"+str(port)+"/connections", conn_id=conn_id)

        #finally kill the agent unless it's allocated to a user
        agent.kill(agent_type="srv", wallet_name=request.session.get('wallet'))
        agent.kill(agent_type="srv", wallet_name=wallet)
        return HttpResponse(response)
    return HttpResponse("wrong method")
        

def register_seed(request):
    if request.method == 'POST':
        agent_obj = get_agent(request)
        seed = agent_obj.seed
        data = {"alias":None, "did":None, "role":"TRUST_ANCHOR", "seed":str(seed)}
        return HttpResponse(requests.post("http://localhost:9000/register", json.dumps(data)))
    return HttpResponse("method not allowed")

def issue_cred(request):
    if request.method == 'POST':
        data = request.POST

        #clean the data and get the conneciton id
        clean_data = {key:val[0] for key,val in dict(data).items() if not(key=='id')}
        conn_id = dict(data).get('id', None)

        assert(conn_id is not None)
        conn_id = conn_id[0]

        act_agent = get_active_agent(request)

        #push schema to the ledger
        schema_resp = requests.post(
            url="http://localhost:"+str(act_agent.outbound_trans)+"/schemas",
            data=json.dumps({
                "attributes":list(clean_data.keys()), 
                "schema_name":str(clean_data.get("type",None)),
                "schema_version":"1.0"
            })
        )

        schema_id = json.loads(schema_resp.text).get("schema_id", None)

        #push credential defenition to the ledger
        credef_resp = requests.post(
            url="http://localhost:"+str(act_agent.outbound_trans)+"/credential-definitions",
            data=json.dumps({"schema_id":str(schema_id)})
        )

        credef_id = json.loads(credef_resp.text).get("credential_definition_id", None)
        
        #send credential through connection
        credsend_resp = requests.post(
            url="http://localhost:"+str(act_agent.outbound_trans)+"/credential_exchange/send",
            data=json.dumps({
                "connection_id":str(conn_id),
                "credential_definition_id":str(credef_id),
                "credential_values":clean_data
                })
        )

        print(credsend_resp.text)
    return HttpResponse(credef_id)

def get_cred(request):
    wallet_name = request.session.get('wallet', None)
    assert(wallet_name!=None)
    agent_obj = agent.objects.get(wallet_name=wallet_name)
    act_agent_obj = agent_obj.active_agent
    port = act_agent_obj.outbound_trans

    cred_resp = requests.get("http://localhost:"+str(port)+"/credentials")
    return HttpResponse(cred_resp.text)


def send_cred_req(request):
    if request.method == "POST":
        #get data no matter if it's url encoded or json
        data = request.POST if dict(request.POST) != {} else request.body.decode('utf-8')
        data=json.loads(data)

        request_data = {
            "version":"1.0",
            "connection_id":data["conn_id"],
            "name":"proof of "+data["type"],
            "requested_predicates":{},
            "requested_attributes":[]
        }

        for key,val in data.items():
            if val is True:
                request_data["requested_attributes"].append({
                    "restrictions":[],
                    "name":key
                })
        print(request_data)

        act_agent = get_active_agent(request)
        port = act_agent.outbound_trans

        resp = requests.post("http://localhost:"+str(port)+"/presentation_exchange/send_request",json.dumps(request_data))
        print(resp.text)
        return HttpResponse(resp)
    return HttpResponse("wrong method")

def get_req(request):
    act_agent = get_active_agent(request)
    port = act_agent.outbound_trans
    resp = requests.get("http://localhost:"+str(port)+"/presentation_exchange")
    return HttpResponse(resp.text)

def conn(request):
    return HttpResponse("hello from conn!")


def get_agent(request):
    return agent.objects.get(wallet_name=request.session["wallet"])

def get_active_agent(request):
    agent_obj = get_agent(request)
    return active_agent.objects.get(agent_id=agent_obj.id)