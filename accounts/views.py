from django.shortcuts import render, redirect
from . models import *
from . forms import *
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views import View


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})
    
class ProfileView(View):
    @login_required
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {'form': form})
    
    @login_required
    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'form': form})
    
class ChangePasswordView(View):
    @login_required
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'accounts/change_password.html', {'form': form})
    
    @login_required
    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        return render(request, 'accounts/change_password.html', {'form': form})

def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')

