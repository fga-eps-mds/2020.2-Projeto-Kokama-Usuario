from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.views.decorators.http import require_http_methods

WORD_LIST_URL = '/traducao/lista_de_palavras/'

@require_http_methods(["GET", "POST"])
def admin_register(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                email = form.cleaned_data.get('email')
                user = authenticate(username=username, password=raw_password, email=email)
                user.is_superuser = True
                user.is_staff = True
                user.save()
                return redirect(WORD_LIST_URL)
        else:
            form = UserCreationForm()
        return render(request, 'admin_register.html', {'form': form})
    else:
        return redirect('/')
                
@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user.is_superuser:
                django_login(request, user)
                return redirect(WORD_LIST_URL)
    else:
        if request.user.is_authenticated and request.user.is_superuser:
                return redirect(WORD_LIST_URL)
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@require_http_methods(["GET"])
def logout(request):
    django_logout(request)
    return redirect('/administracao/login/')


# O método make_random_password do BaseUserManager pode ser usado para criar novas senhas aleatórias, especificando-se o tamanho (padrão: 10) e o alfabeto (padrão: alfanumérico, maiúsculas e minúsculas, só ignorando alguns caracteres parecidos).

# Sendo assim, tudo que sua view precisa fazer é obter uma instância do User certo, chamar o set_password desse usuário com a senha aleatória criada (o próprio método se encarrega de hasheá-la) e então salvá-lo. Exemplo:

# def resetar_senha(request):
#     usuario = User.objects.get(username=request.POST["username"])
#     usuario.set_password(User.objects.make_random_password())
#     usuario.save()
#     return HttpResponseRedirect("url/de/sucesso")
@require_http_methods(["GET", "POST"])
def recover_password (request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = authenticate(username=username)
            if user.is_superuser:
                form.set_password(form.objects.make_random_password())
                form.save()
                return render(request, '/', {'form': form})
    else:
        if request.user.is_authenticated and request.user.is_superuser:
                return redirect(WORD_LIST_URL)
        form = AuthenticationForm()
    return render(request, 'recover_password.html', {'form': form})

# --------------------------
# @require_http_methods(["GET", "POST"])
# def recover_password (request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             if user.is_superuser:
#                 new_password = form.cleaned_data.get('new_password'):
#                 user = authenticate(username=username, password=new_password)
#                 user.is_staff = True
#                 user.save()
#                 form.save()
#                 return render(request, '/', {'form': form})
#     else:
#         if request.user.is_authenticated and request.user.is_superuser:
#                 return redirect(WORD_LIST_URL)
#         form = AuthenticationForm()
#     return render(request, 'recover_password.html', {'form': form})
# # ----------------------------

# # @action(["post"], detail=False)
# #     def set_password(self, request, *args, **kwargs):
# #         serializer = self.get_serializer(data=request.data)
# #         serializer.is_valid(raise_exception=True)

# #         self.request.user.set_password(serializer.data["new_password"])
# #         self.request.user.save()

#         # if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
#         #     context = {"user": self.request.user}
#         #     to = [get_userEMAIL.password_chang_email(self.request.user)]
#         #     settings.ed_confirmation(self.request, context).send(to)

#         # if settings.LOGOUT_ON_PASSWORD_CHANGE:
#         #     utils.logout_user(self.request)
#         # elif settings.CREATE_SESSION_ON_LOGIN:
#         #     update_session_auth_hash(self.request, self.request.user)
#         # return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(["post"], detail=False)
#     def reset_password(self, request, *args, **kwargs):
#         form = AuthenticationForm(data=request.POST)
#         form.is_valid(raise_exception=True)
#         user = serializer.get_user()

#         if user:
#             context = {"user": user}
#             to = [get_user_email(user)]
#             settings.EMAIL.password_reset(self.request, context).send(to)

#         return Response(status=status.HTTP_204_NO_CONTENT)

#     @action(["post"], detail=False)
#     def reset_password_confirm(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.user.set_password(serializer.data["new_password"])
#         if hasattr(serializer.user, "last_login"):
#             serializer.user.last_login = now()
#         serializer.user.save()

#         if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
#             context = {"user": serializer.user}
#             to = [get_user_email(serializer.user)]
#             settings.EMAIL.password_changed_confirmation(self.request, context).send(to)
#         return Response(status=status.HTTP_204_NO_CONTENT)