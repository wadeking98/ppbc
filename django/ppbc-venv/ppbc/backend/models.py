from django.db import models
from django.contrib.auth.models import User

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