from django.conf.urls import url
from .views import admin_register, login

urlpatterns = [
    url(r'^admin_register/$', admin_register, name='admin_register'),
    url(r'^login/$', login, name='login'),
]