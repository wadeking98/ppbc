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
    path('logout/', views.logout, name='logout')
]