from django.conf.urls import url
from .views import admin_register, login, logout, recover_password

urlpatterns = [
    url(r'^cadastrar_admin/$', admin_register, name='admin_register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'recuperacao/$', recover_password, name='recover_password'),
]