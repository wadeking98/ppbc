from django.db import models
from django.contrib.auth.models import User
from django import forms
import subprocess
import os
import socket

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
    def __str__(self):
        return self.user.__str__()
    
    

class active_agent(models.Model):
    agent = models.OneToOneField(agent, on_delete=models.CASCADE)
    login_date = models.DateTimeField()
    agent_proc = None

    def start(self):
        agent_proc = subprocess.Popen([os.path.join("../../","run_agent"), 
        ""+str(5000), 
        ""+str(10000),
        ""+str(self.agent.seed),
        ""+str(self.agent.name),
        ""+str(self.agent.wallet_name),
        "../../scripts/"], stdout=subprocess.PIPE)
    
    def kill(self):
        if agent_proc is not None:
            agent_proc.kill()
    
    def __str__(self):
        return self.agent.__str__()

    