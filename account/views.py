from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import RegistrationForm


# user registration 
def registration(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    
    context = {'form': form}
    return render(request, 'account/registration.html', context)


# user login or signin
def user_login(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse('loged in')
    
    context = {'form': form}
    return render(request, 'account/login.html', context)


@login_required
def user_logout(request):
    logout(request)

    pass