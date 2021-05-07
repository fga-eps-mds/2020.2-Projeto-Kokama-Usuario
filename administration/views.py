from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.views.decorators.http import require_http_methods


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

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

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'192.168.1.7:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ('/password_reset/done')
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name='/password_reset.html', context={"password_reset_form":password_reset_form})

# @require_http_methods(["GET", "POST"])
# def recover_password (request):
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             user = authenticate(username=username)
#             if user.is_superuser:
#                 form.set_password(form.objects.make_random_password())
#                 form.save()
#                 return render(request, '/', {'form': form})
#     else:
#         if request.user.is_authenticated and request.user.is_superuser:
#                 return redirect(WORD_LIST_URL)
#         form = AuthenticationForm()
#     return render(request, 'recover_password.html', {'form': form})

