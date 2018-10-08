from django.conf.urls import url
from . import views    

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create),
    url(r'^validate_login$', views.validate_login),
    url(r'^logout$', views.logout),
    url(r'^wall$', views.wall),
    url(r'^msuccess$', views.msuccess),
    url(r'(?P<id>\d+)/csuccess$', views.csuccess),
]         
