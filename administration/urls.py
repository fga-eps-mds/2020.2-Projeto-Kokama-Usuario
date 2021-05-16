from django.conf.urls import url
from .views import admin_register, login, logout, password_reset_request
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^cadastrar_admin/$', admin_register, name='admin_register'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(template_name= "password/password_reset.html"), name="reset_password"),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
]