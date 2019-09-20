from django.db import models
from django.contrib.auth.models import User
from django import forms
from django.core.validators import MaxValueValidator
from django.db import transaction
import subprocess
import os, signal
import socket
import datetime
import time
from .tools import *
import requests
import json


class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    health_id = models.CharField(max_length=20)
    def __str__(self):
        return self.user.__str__()

class org_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=100)
    org_role = models.CharField(max_length=100)
    def __str__(self):
        return self.org_name

class agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    seed = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    wallet_name = models.CharField(max_length=150)
    user_allocated = models.BooleanField(default=False)
    server_allocated = models.BooleanField(default=False)
    
    

    @classmethod
    def start(cls, agent_type, wallet_name, pswd):
        """
        atomically marks agent as allocated to the server or to a user,
        and starts an aries agent instance

        Parameters:
        agent_type (str): either "usr" for user or "srv" for server
        wallet_name (str): the wallet name of the agent to start
        """
        with transaction.atomic():
            agent_obj = (cls.objects.select_for_update().get(wallet_name=wallet_name))
            agent_obj.user_allocated = (agent_obj.user_allocated or (agent_type=="usr"))
            agent_obj.server_allocated = (agent_obj.server_allocated or(agent_type=="srv"))
            agent_obj.find_or_create(pswd)
            agent_obj.save()
            
    
    @classmethod
    def start_router(cls):
        router_usr = User.objects.filter(email="router@mail.com").first()
        if router_usr is None:
            router_usr = User.objects.create_user(username="router", password="1234", email="router@mail.com")
            router_usr.save()

        router_agent = agent.objects.filter(wallet_name="i_router_mail_com").first()
        if router_agent is None:
            router_agent = agent(user=router_usr, seed=tools.id_to_seed(router_usr.id),name="router",wallet_name="i_router_mail_com")
            router_agent.save()
        router_agent.find_or_create("routerpswd",router=True)


    @classmethod
    def kill(cls, agent_type, wallet_name):
        """
        atomically marks agent as unallocated to either the server 
        or to a user, and kills the aries agent instance

        Parameters:
        agent_type (str): either "usr" for user or "srv" for server
        wallet_name (str): the wallet name of the agent to start
        """
        with transaction.atomic():
            agent_obj = (cls.objects.select_for_update().get(wallet_name=wallet_name))
            #if the user is allocated and we're killing a user, set user_allocated to false
            #likewise for server
            agent_obj.user_allocated = (agent_obj.user_allocated and (agent_type!="usr"))
            agent_obj.server_allocated = (agent_obj.server_allocated and (agent_type!="srv"))
            
            # kill the agent if it's not in use
            if not agent_obj.user_allocated and not agent_obj.server_allocated:
                agent_obj.stop()
            agent_obj.save()
    

    @classmethod
    def try_post(cls, url, data, max_iter=10):
        """
        polling loop, sleeps until post succeeds or max_iter is used
        This function should be replaced when moving to an Aries version that
        supports webhooks

        Parameters:
        url (str): the url to post to
        data (str): the data being posted as json
        max_iter (int): the number of times to try posting before giving up
        """
        while max_iter > 0:
            print(max_iter)
            try:
                return requests.post(url, data=data)
            except:
                time.sleep(1)
                max_iter -= 1


    @classmethod
    def wait_until_conn(cls, url, conn_id,max_iter=10):
        """
        polling loop waits until connection becomes active
        This function should be replaced when moving to an Aries version that
        supports webhooks

        Parameters:
        url (str): the url of where to get the connections
        conn_id (str): the id of the connection in question
        """
        success = cls.search_conn(url, conn_id)
        while not success and max_iter > 0:
            max_iter -= 1
            time.sleep(1)
            success = cls.search_conn(url, conn_id)

    @classmethod
    def search_conn(cls, url, conn_id):
        """
        Parameters:
        url (str): url location of user connecitons
        conn_id (str): the id of the conneciton in question

        Returns:
        bool: True if conneciton is active
        """
        success = False
        conns = requests.get(url).json().get('results')
        for conn in conns:
            if conn.get('connection_id') == conn_id and conn.get('state') == "active":
                success = True
        return success


    
    def alloc_port(self):
        """
        binds a random free port on the machine and returns the port
        number

        Returns:
        int: the free allocated port
        """
        port = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((socket.gethostname(),0))
            port = sock.getsockname()[1]
        return port


    def find_or_create(self, pswd, router=False):
        """
        creates the aries agent unless it's already running
        """
        if not tools.agent_running(self.wallet_name):
            data = {"alias":None, "did":None, "role":"TRUST_ANCHOR", "seed":str(self.seed)}
            requests.post("http://localhost:9000/register", json.dumps(data))
            #allocate two free ports, one to inbound transport (where the 
            # agent recives credential offers, etc) and one to outbound transport (
            # where the api is hosted)
            it = 10000
            ot = 5000

            if not router:
                it = self.alloc_port()
                ot = self.alloc_port()
            
            # if ports are successfully allocated, run agent
            if it is not None and ot is not None:
                agent_env = os.environ.copy()
                agent_env["PORTS"] = str(ot)+":"+str(ot)+" "+str(it)+":"+str(it)
                agent_env["NAME"] = self.wallet_name
                proc = subprocess.Popen([
                    "./scripts/run_docker",
                    "-it", "http", "0.0.0.0", str(it),
                    "-ot", "http", "--admin", "0.0.0.0", str(ot),
                    "-e", "http://172.17.0.1:"+str(it),
                    "--genesis-url", "http://172.17.0.1:9000/genesis",
                    "--seed", self.seed,
                    "--auto-ping-connection",
                    "--accept-invites",
                    "--accept-requests",
                    "--auto-verify-presentation",
                    "--auto-respond-credential-offer",
                    # "--auto-respond-presentation-request",
                    "--wallet-name", self.wallet_name,
                    "--wallet-type", "indy",
                    "--wallet-key", pswd,
                    "--wallet-storage-type", "postgres_storage",
                    "--wallet-storage-config", "{\"url\":\"172.0.0.5:5432\", \"max_connections\":5, \"connection_timeout\":10}",
                    "--wallet-storage-creds", "{\"account\":\"postgres\",\"password\":\"docker\",\"admin_account\":\"postgres\",\"admin_password\":\"docker\"}",
                    "--label", self.name
                    ], env=agent_env, encoding="utf-8",)
                #grab the process id of the agent
                pid = proc.pid
                
                if active_agent.objects.filter(agent=self) is not None:
                    active_agent.objects.filter(agent=self).delete()

                act_agent = active_agent(agent=self,inbound_trans=it,outbound_trans=ot,pid=pid,login_date=datetime.datetime.now())
                act_agent.save()
                
                
    
    def stop(self):
        """
        starts a subprocess to kill the running docker container and
        remove the agent from the active_agents table
        """
        if tools.agent_running(self.wallet_name):
            try:
                proc = subprocess.Popen([
                    "docker", "kill", self.wallet_name
                ])
                proc.wait(timeout=2)
            except:
                print("cannot kill docker container: "+str(request.session.get("wallet")))
            finally:
                proc.terminate()
            
            #remove this agent from the active agent table
            active_agent.objects.get(agent=self).delete()
        

    def __str__(self):
        return self.user.__str__()
    
    

class active_agent(models.Model):
    agent = models.OneToOneField(agent, to_field='id', on_delete=models.CASCADE)
    inbound_trans = models.IntegerField()
    outbound_trans = models.IntegerField()
    pid = models.IntegerField()
    login_date = models.DateTimeField()
    
    def __str__(self):
        return self.agent.__str__()

    
