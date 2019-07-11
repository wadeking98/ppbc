from django.db import models
from django.contrib.auth.models import User
from django import forms
import subprocess

# Create your models here.

# class client(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(max_length=50)
#     password = models.CharField(max_length=64)
#     usr_port = models.IntegerField()
#     def __str__(self):
#         return self.first_name

# class org(models.Model):
#     client = models.ForeignKey(client, on_delete=models.CASCADE)
#     org_name = models.CharField(max_length=100)
#     org_role = models.CharField(max_length=100)
#     def __str__(self):
#         return self.org_name

class user_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usr_port = models.IntegerField()
    def __str__(self):
        return self.user.__str__()

class org_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org_name = models.CharField(max_length=100)
    org_role = models.CharField(max_length=100)
    usr_port = models.IntegerField()
    def __str__(self):
        return self.org_name

class agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    inbound_trans = models.IntegerField()
    outbound_trans = models.IntegerField()
    seed = models.CharField(max_length=32)
    name = models.CharField(max_length=100)
    wallet_name = models.CharField(max_length=150)
    def __str__(self):
        return self.user.__str__()
    
    def start(self, script_dir):
        subprocess.run([script_dir+"run_agent", 
        self.outbound_trans, 
        self.inbound_trans,
        self.seed,
        self.name,
        self.wallet_name])