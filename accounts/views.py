#from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import PasswordResetConfirmView

from .forms import RegisterationForm, LogInForm, ResetPasswordForm

class ResetPasswordView(PasswordResetConfirmView):

    form_class = ResetPasswordForm


def HomePageView(request):
    return render(request, 'index.html')


def RegisterView(request):

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}
    if request.POST:
        form = RegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='accounts.backends.EmailAuthBackend')
            return redirect('home')
    else:
        form = RegisterationForm()

    context['register_form'] = form
    return render(request, 'accounts/register.html', context)


def LogInView(request):

    user = request.user
    if user.is_authenticated:
        return redirect('home')

    context = {}
    if request.POST:
        form = LogInForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user, backend='accounts.backends.EmailAuthBackend')
                return redirect('home')

    else:
        form = LogInForm()

    context['login_form'] = form
    return render(request, "accounts/login.html", context)


def LogOutView(request):
	logout(request)
	return redirect('home')