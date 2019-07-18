from django.db import models
from django.contrib.auth.models import User
from django import forms
import subprocess
import os, signal
import socket
import datetime
import pickle

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
    


    def start(self):
        #allocate two free ports, one to inbound transport (where the 
        # agent recives credential offers, etc) and one to outbound transport (
        # where the api is hosted)
        it = self.alloc_port()
        ot = self.alloc_port()
        
        # if ports are successfully allocated, run agent
        if it is not None and ot is not None:
            agent_env = os.environ.copy()
            agent_env["PORTS"] = str(ot)+":"+str(ot)+" "+str(it)+":"+str(it)
            agent_env["NAME"] = self.wallet_name
            proc = subprocess.Popen([
                "../../scripts/run_docker",
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
                "--auto-respond-presentation-request",
                "--wallet-name", self.wallet_name,
                "--wallet-type", "indy",
                "--wallet-key", "key",
                "--wallet-storage-type", "postgres_storage",
                "--wallet-storage-config", "{\"url\":\"172.0.0.5:5432\", \"max_connections\":5, \"connection_timeout\":10}",
                "--wallet-storage-creds", "{\"account\":\"postgres\",\"password\":\"docker\",\"admin_account\":\"postgres\",\"admin_password\":\"docker\"}",
                "--label", self.name], env=agent_env, encoding="utf-8",)
            #grab the process id of the agent
            pid = proc.pid
            
            act_agent = active_agent(agent=self,inbound_trans=it,outbound_trans=ot,pid=pid,login_date=datetime.datetime.now())
            act_agent.save()
            
            #return the agent process
            return proc

        #if port allocation fails return nothing
        return None

    def alloc_port(self):
        port = None
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((socket.gethostname(),0))
            port = sock.getsockname()[1]
        return port

    
    def stop(self):
        print(self.proc)
        pass

    def __str__(self):
        return self.user.__str__()
    
    

class active_agent(models.Model):
    agent = models.OneToOneField(agent, on_delete=models.CASCADE)
    inbound_trans = models.IntegerField()
    outbound_trans = models.IntegerField()
    pid = models.IntegerField()
    login_date = models.DateTimeField()
    
    def __str__(self):
        return self.agent.__str__()

    