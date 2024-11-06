from django import forms
from adminpanel.models import Profile , Blog , Comment
from .models import User 
from django.contrib.auth.forms import UserCreationForm
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Username"
    )
    password1 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )
    password2 = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm Password"
    )
    
   
    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username



    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        # Check if password length is at least 8 characters
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        # Check if password contains at least one lowercase letter
        if not re.search(r'[a-z]', password1):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        
        # Check if password contains at least one uppercase letter or number
        if not re.search(r'[A-Z]', password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        
        # Check if password contains at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            raise forms.ValidationError("Password must contain at least one special character.")
                
        # Check if password contains at least one number
        if not re.search(r'[0-9]', password1):
            raise forms.ValidationError("Password must contain at least one number.")
        
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        
        return password2


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'profile_image', 'id_proof']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'id_proof': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

        class Meta:
            model = Profile
            fields = ['phone', 'profile_image', 'id_proof']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Profile.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Password"
    )

    

