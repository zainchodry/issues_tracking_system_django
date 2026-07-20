from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, Profile
from .forms import RegisterForm, ProfileForm, ChangePasswordForm
from django.contrib import messages
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from django.views import View
from django.db.models import Count, Q


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = request.user.profile
        form = ProfileForm(instance=profile)
        return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

    def post(self, request):
        profile = request.user.profile
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('profile')
        return render(request, 'accounts/change_password.html', {'form': form})


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        from projects.models import Project, ProjectMember
        from issues.models import Issue
        from notifications.models import Notification

        user = request.user

        # Projects
        if user.role == 'ADMIN':
            projects = Project.objects.all()
            issues = Issue.objects.all()
        elif user.role == 'MANAGER':
            projects = Project.objects.filter(
                Q(owner=user) | Q(project_members__user=user)
            ).distinct()
            issues = Issue.objects.filter(
                Q(reporter=user) | Q(assignee=user) | Q(project__owner=user)
            ).distinct()
        else:
            projects = Project.objects.filter(project_members__user=user).distinct()
            issues = Issue.objects.filter(assignee=user)

        # Stats
        total_projects = projects.count()
        active_projects = projects.filter(status='ACTIVE').count()
        total_issues = issues.count()
        open_issues = issues.filter(status='TODO').count()
        in_progress = issues.filter(status='IN_PROGRESS').count()
        completed_issues = issues.filter(status='COMPLETED').count()
        overdue_issues = [i for i in issues if i.is_overdue]

        # Recent items
        recent_issues = issues.select_related('project', 'assignee').order_by('-created_at')[:5]
        recent_projects = projects.select_related('owner').order_by('-created_at')[:5]

        # Unread notifications
        unread_notifications = Notification.objects.filter(
            recipient=user, is_read=False
        ).order_by('-created_at')[:5]
        unread_count = Notification.objects.filter(recipient=user, is_read=False).count()

        context = {
            'total_projects': total_projects,
            'active_projects': active_projects,
            'total_issues': total_issues,
            'open_issues': open_issues,
            'in_progress': in_progress,
            'completed_issues': completed_issues,
            'overdue_count': len(overdue_issues),
            'recent_issues': recent_issues,
            'recent_projects': recent_projects,
            'unread_notifications': unread_notifications,
            'unread_count': unread_count,
        }
        return render(request, 'dashboard/dashboard.html', context)


def logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')
