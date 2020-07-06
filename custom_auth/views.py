from custom_auth.exceptions import LoginFailureException
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.conf import settings

from .forms import LoginForm, SignUpForm
from .backend import AuthBackend
from .models import User


class LoginView(View):

    def get(self, request):

        context = {
            'form': LoginForm()
        }

        return render(request, 'login/login.html', context)

    def post(self, request):

        form = LoginForm(request.POST)
        
        try:
            if not form.is_valid():
                raise LoginFailureException()
            
            user = AuthBackend().authenticate(
                request, 
                username=form.cleaned_data['username'], 
                password=form.cleaned_data['password']
            )
        
        except LoginFailureException:

            form.add_error(None, 'ユーザ名またはパスワードが間違っています。')
            context = {'form': form}
            return render(request, 'login/login.html', context)

        login(request, user, 'custom_auth.backend.AuthBackend')

        return redirect(settings.LOGIN_SUCCESS_URL)


class SignUpView(View):

    def get(self, request):

        context = {
            'form': SignUpForm()
        }

        return render(request, 'signup/signup.html', context)

    def post(self, request):

        form = SignUpForm(request.POST)

        if not form.is_valid():

            context = {
                'form': form
            }
            return render(request, 'signup/signup.html', context)

        user = User(
            username=form.cleaned_data['username'],
            password=make_password(form.cleaned_data['password']),
            is_admin=False,
        )

        user.save()

        return redirect('login:login')

class LogoutView(View):

    def get(self, request):

        logout(request)

        return redirect('login:login')

class TopView(View):

    def get(self, request):

        if not request.user.is_authenticated:
            return redirect('login:login')
        
        if not request.user.is_admin:
            return render(request, 'top/top.html')

        return render(request, 'top/top_admin.html')

def handler404(request, exception):
    return render(request, 'widget_404.html', status=404)
