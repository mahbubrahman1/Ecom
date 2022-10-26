from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from .forms import RegistrationForm, ProfileForm
from .models import Profile


# user profile 
@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Profile saved')
            form = ProfileForm(instance=profile)
    
    context = {'form': form}
    return render(request, 'account/profile.html', context)


# user registration 
def registration(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
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
                return HttpResponseRedirect(reverse('home'))
    
    context = {'form': form}
    return render(request, 'account/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, 'Logged out!')

    return HttpResponseRedirect(reverse('home'))