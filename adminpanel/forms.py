from .models import User
from django import forms
from .models import  Blog, Comment , Profile
from django.contrib.auth.forms import PasswordChangeForm , UserCreationForm
from django.contrib.auth import password_validation



class RegistrationForm(forms.ModelForm):
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
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        label="Username"
    )
    
    
    class Meta:
        model = User  
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'profile_image']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            
        }


class BlogForm(forms.ModelForm):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        (' published', 'Published'),
        ('archived', 'Archived'),
    )

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-inline'}),
        initial='Published'  # Optional: Set an initial value if needed
    )

    class Meta:
        model = Blog
        exclude = ['author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'blog_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']  # Fields that will be shown in the form



class PasswordResetForm(forms.Form):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Old Password"
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="New Password"
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirm New Password"
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Old password is incorrect.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError("The new passwords do not match.")
        
        password_validation.validate_password(new_password1, self.user)
        
        return cleaned_data

    def save(self, commit=True):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        if commit:
            self.user.save()
        return self.user


