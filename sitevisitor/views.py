from django.shortcuts import  render, redirect
from adminpanel.models import Blog , Comment , Profile
from .forms import RegistrationForm, LoginForm , ProfileForm
from .models import User  
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from userpanel.forms import BlogForm, CommentForm
from django.utils import timezone





# Create your views here.
def home(request):
    logged_user = request.user
    blog = Blog.objects.filter(status='published')
    return render(request,'sitevisitor/home.html',{'Blog':blog , 'logged_user' : logged_user})

def view_blog_site(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id )
    comments = Comment.objects.filter(blog=blog)
    logged_user = request.user
    try:
        profile = Profile.objects.get(user=logged_user)
    except Profile.DoesNotExist:
        profile = None  # Handle the case where the profile doesn't exist

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = logged_user
            comment.created_at = timezone.now()
            comment.blog = blog
            comment.save()
            return redirect('view_blog', blog_id=blog.id)  # Redirect back to the same blog page after comment submission
    else:
        form = CommentForm()

    count = comments.count()
    context = {
        'blog': blog,
        'comments': comments,
        'form': form,
        'logged_user': logged_user,
        'count': count,
        'profile': profile,
    }

    return render(request, 'sitevisitor/view_blog.html', context)


def site_base(request):
    return render(request,'sitevisitor/site_base.html')

def forgot_password(request):
    return render(request,'sitevisitor/forgot_password.html')

def otp(request):
    return render(request,'sitevisitor/otp.html')

def registration(request):  
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        form1 = ProfileForm(request.POST , request.FILES)
        if form.is_valid() and form1.is_valid():
            user = form.save()
            profile = form1.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,'User Registered successfully')
            return redirect('user_login')    
    else:
        form = RegistrationForm()
        form1 = ProfileForm()     

    return render(request,'sitevisitor/registration.html',{'form':form , 'form1': form1})


def user_login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                if user.is_staff:                    
                    return redirect('admin_home')  
                else:                    
                    return redirect('user_home')    
                         
            else:                
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'sitevisitor/login.html', {'form': form})


def contact_us(request):
    return render(request,'sitevisitor/contact_us.html')


def user_home(request):
    logged_user = request.user
    return render(request,'sitevisitor/user_home.html',{'logged_user':logged_user})


