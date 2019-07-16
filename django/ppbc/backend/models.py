from django.db import models
from django.contrib.auth.models import User
from django import forms
import subprocess
import os, signal
import socket
import datetime

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
        it = None
        ot = None
        # allocate a free inbound and outbound socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as in_sock:
            in_sock.bind((socket.gethostname(),0))
            it = in_sock.getsockname()[1]

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as out_sock:
            out_sock.bind((socket.gethostname(), 0))
            ot = out_sock.getsockname()[1]
        
        # if ports are successfully allocated, run agent
        if it is not None and ot is not None:
            agent_env = os.environ.copy()
            agent_env["PORTS"] = str(ot)+":"+str(ot)+" "+str(it)+":"+str(it)
            self.proc = subprocess.Popen([
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
                "--label", self.name], env=agent_env)
            pid = self.proc.pid
            agent_proc = active_agent(agent=self, inbound_trans=it, outbound_trans=ot, pid=pid, login_date=datetime.datetime.now())
            agent_proc.save()
    
    def stop(self):
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

    