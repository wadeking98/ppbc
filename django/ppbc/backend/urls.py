from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.test, name='test'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('org_signup/', views.org_signup, name='org_signup'),
    path('list_conn/', views.list_conn, name='list_conn'),
    path('list_org/', views.list_org, name='list_org'),
    path('list_usr/', views.list_usr, name='list_usr'),
    path('wallet/', views.wallet, name='wallet'),
    path('conn/', views.conn, name='conn'),
    path('logout/', views.logout, name='logout'),
    path('send_invite/', views.send_invite, name='send_invite'),
    path('del_conn/', views.del_conn, name='del_conn'),
    path('send_msg/', views.send_msg, name='send_msg'),
    path('register_seed/', views.register_seed, name='register_seed'),
    path('issue_cred/', views.issue_cred, name='issue_cred'),
    path('webhook/', views.webhook, name='webhook'),
    path('credentials/', views.get_cred, name='get_cred'),
    path('send_cred_req/', views.send_cred_req, name='send_cred_req'),
    path('get_req/', views.get_req, name='get_req'),
    path('get_req_cred/', views.get_req_cred, name='get_req_cred'),
    path('subm_pres/', views.subm_pres, name='subm_pres')
]