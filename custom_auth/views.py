from django.shortcuts import render
from django.views import View

from .forms import LoginForm

class LoginView(View):

    def get(self, request):

        context = {
            'form': LoginForm()
        }

        return render(request, 'login/login.html', context)

