from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as BaseLoginView

class LoginView(BaseLoginView):
    template_name = 'identity/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('login')
