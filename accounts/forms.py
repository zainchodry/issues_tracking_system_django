from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from . models import *

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='full-name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='confirm-password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label='role', choices=User.Roles.choices, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user", "created_at", "updated_at"]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "city": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label='old-password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='new-password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='confirm-new-password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ForgetPasswordForm(PasswordResetForm):
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

class ResetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='new-password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='confirm-new-password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com', 'autofocus': True})
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '••••••••'})
    )
