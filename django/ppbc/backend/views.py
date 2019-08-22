from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate
import json
import requests
from .models import *
import datetime
from .tools import *


#_________________API_ENDPOINTS___________________________

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


def get_cred(request):
    """
    fetches the user's credentials from the agent wallet

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    wallet_name = request.session.get('wallet', None)
    assert(wallet_name!=None)
    agent_obj = agent.objects.get(wallet_name=wallet_name)
    act_agent_obj = agent_obj.active_agent
    port = act_agent_obj.outbound_trans

    cred_resp = requests.get("http://localhost:"+str(port)+"/credentials")
    return HttpResponse(cred_resp.text)


def get_req(request):
    """
    gets all credential request exchanges

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    act_agent = get_active_agent(request)
    port = act_agent.outbound_trans
    resp = requests.get("http://localhost:"+str(port)+"/presentation_exchange")
    return HttpResponse(resp.text)

def get_req_cred(request):
    """
    get credentials that fit a certain presentation request

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    if request.method == "POST":
        data = get_data(request)
        if not (data.get('id',False) and data.get('referent',False)):
            raise Exception("data id or refernt not set") 
        port = get_act_port(request)
        resp = requests.get("http://localhost:"+str(port)+"/presentation_exchange/"+str(data['id'])+"/credentials/"+str(data['referent']))
        print("http://localhost:"+str(port)+"/presentation_exchange/"+str(data['id'])+"/credentials/"+str(data['referent']))
        return HttpResponse(resp)
    return HttpResponse("wrong method")




def issue_cred(request):
    """
    creates a schema defenition, credential defenition and finally
    issues a credential to another agent over a connection

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
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
            agent.start("usr", wallet_name, password)
        except Exception as err:
            print(err)
            return JsonResponse({"signup":False})

    return JsonResponse({"signup":True})


def register_seed(request):
    """
    registers the wallet seed so that the agent wallet is connected to the
    ledger

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    if request.method == 'POST':
        agent_obj = get_agent(request)
        seed = agent_obj.seed
        data = {"alias":None, "did":None, "role":"TRUST_ANCHOR", "seed":str(seed)}
        return HttpResponse(requests.post("http://localhost:9000/register", json.dumps(data)))
    return HttpResponse("method not allowed")


def remove_req(request):
    if request.method == "POST":
        data = get_data(request)
        id = data.get("id", None)
        assert(id is not None)
        port = get_act_port(request)
        resp = requests.post("http://localhost:"+str(port)+"/presentation_exchange/"+str(id)+"/remove")
        return HttpResponse(resp.text)
    return HttpResponse("wrong method")


def send_cred_req(request):
    """
    sends a credential presentation request over a connection

    Parameters:
    request (request object): the request sent by the front end
    containing the requested credential attributes

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    if request.method == "POST":
        #get data no matter if it's url encoded or json
        data = request.POST if dict(request.POST) != {} else request.body.decode('utf-8')
        data=json.loads(data)

        request_data = {
            "version":"1.0",
            "connection_id":data["conn_id"],
            "name":data["title"],
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



def send_invite(request, routing=False):
    """
    automatically connects two users, even if one is offline

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    if request.method == 'POST':
        #get the post data
        data = get_data(request)
        usr_id = data.get('user')

        #find the agent recieving the connection
        usr = User.objects.get(id=usr_id)
        agent_obj = agent.objects.get(user=usr)
        wallet = agent_obj.wallet_name

        # #mark this agent as allocated to the server
        # agent.start(agent_type="srv", wallet_name=request.session.get('wallet'))
        # #start or find the running aries agent
        # agent.start(agent_type="srv", wallet_name=wallet)
        act_agent_obj = active_agent.objects.get(agent=agent_obj)
        port = act_agent_obj.outbound_trans

        # router_conn("i_router_mail_com",agnt=agent_obj)

        #get the invitation json
        invite = get_invite(request)
        print(invite.get('invitation'))

        #wait for the aries agent to come online and send invitation
        response = agent.try_post(url="http://localhost:"+str(port)+"/connections/receive-invitation",data=json.dumps(invite.get('invitation')))
        conn_id = response.json().get('connection_id')

        #accept the recieved invitation
        # requests.post(
        #     url="http://localhost:"+str(port)+"/connections/"+str(conn_id)+"/accept-invitation"
        # )
        
        # wait until connection is active before killing server-agent process
        agent.wait_until_conn(url="http://localhost:"+str(port)+"/connections", conn_id=conn_id)

        #finally kill the agent unless it's allocated to a user
        agent.kill(agent_type="srv", wallet_name=request.session.get('wallet'))
        agent.kill(agent_type="srv", wallet_name=wallet)
        return HttpResponse(response)
    return HttpResponse("wrong method")




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
        if user is not None:
            agent_obj = agent.objects.get(user=user)
            request.session["wallet"] = agent_obj.wallet_name
            register_seed(request)
            agent.start("usr", agent_obj.wallet_name, alleged_password)
    return JsonResponse(ret)


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
            agent.start("usr", wallet_name, password)
        except:
            return JsonResponse({"signup":False})
    return JsonResponse({"signup":True})


def subm_pres(request):
    """
    submits the credential presentation

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    if request.method == "POST":
        data = get_data(request)
        req_id = list(data.keys())[0]

        port = get_act_port(request)
        url = "http://localhost:"+str(port)+"/presentation_exchange/"+str(req_id)+"/send_presentation"

        #post data tempalte
        post_data = {
            "requested_predicates": {},
            "requested_attributes": {},
            "self_attested_attributes": {}
        }
        for key in data[req_id]:
            post_data["requested_attributes"][key] = {
                "cred_id":data[req_id][key],
                "revealed":True
            }
        
        resp = requests.post(url, json.dumps(post_data))
        return HttpResponse(resp.text)
    return HttpResponse("wrong method")


def test(request):
    return HttpResponse(tools.agent_running(request.session.get("wallet")))

def webhook(request):
    if request.method == 'POST':
        print(request.POST.text)
        return HttpResponse(request.POST.text)


def wallet(request):
    """
    returns the wallet name of the current user

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON object containing the wallet name
    """
    return JsonResponse({'wallet':request.session['wallet']})










#_________________HELPER_FUNCTIONS________________________

def conn(request):
    return HttpResponse("hello from conn!")


def get_act_port(request=None, agnt=None):
    """
    gets the port used by the current agent's api

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    HttpResponse: the response object fromt he aries agent 
    """
    return get_active_agent(request).outbound_trans if agnt is None else get_active_agent(agnt=agnt).outbound_trans


def get_active_agent(request=None, agnt=None):
    agent_obj = get_agent(request) if agnt is None else agnt
    return active_agent.objects.get(agent_id=agent_obj.id)


def get_agent(request=None, wallet_nm=None):
    return agent.objects.get(wallet_name=request.session["wallet"]) if wallet_nm is None else agent.objects.get(wallet_name=wallet_nm)


def get_data(request):
    """
    cleans and returns data provided in a request

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: the cleaned data
    """
    data = request.POST if dict(request.POST) != {} else request.body.decode('utf-8')
    if isinstance(data, str):
        data = json.loads(data)
    return data

def get_invite(request=None, agnt=None):
    """
    NOT AN API SERVICE
    creates an invitation and returns the invitation json

    Parameters:
    request (request object): the request sent by the front end

    Returns:
    dict: JSON object defining the invitation
    """
    agent_proc = get_active_agent(request) if agnt is None else get_active_agent(agnt=agnt)
    port = agent_proc.outbound_trans
    return requests.post("http://localhost:"+str(port)+"/connections/create-invitation").json()


def router_conn(router_nm, request=None, agnt=None):
    """
    connects the active agent to the router

    Parameters:
    request (request object): the request sent by the front end
    router_it (int): the inbound transport port used by the router
    agnt (agent object): the agent connecting to the router

    Returns:
    str: the id of the connection with the router
    """
    router = get_agent(wallet_nm=router_nm)
    agnt = get_agent(request) if agnt is None else agnt

    #make sure the router is running
    router.find_or_create(router=True)

    invite = get_invite(agnt=agnt)

    #get the agent and router ports
    agnt_port = get_act_port(agnt=agnt)
    router_port = get_act_port(agnt=router)

    response = requests.post(
        url="http://localhost:"+str(router_port)+"/connections/receive-invitation",
        data=json.dumps(invite.get('invitation'))
        )

    conn_id = response.json().get('connection_id')

    requests.post(
        url="http://localhost:"+str(router_port)+"/connections/"+str(conn_id)+"/accept-invitation"
    )
    


