from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Blog, Profile, User, Comment
from .forms import BlogForm, CommentForm, PasswordResetForm, RegistrationForm, ProfileForm
from django.contrib.auth import update_session_auth_hash

# View for admin home page
def admin_home(request):
    logged_user = request.user
    blogs = Blog.objects.filter(status='published')
    return render(request, 'adminpanel/admin_home.html', {
        'logged_user': logged_user,
        'blogs': blogs  
    })


# View to display blogs authored by the logged-in user
@login_required
def myblogsadmin(request):
    logged_user = request.user
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'adminpanel/my_blogs_admin.html', {
        'logged_user': logged_user,
        'blogs': blogs,
    })

# View to edit a user's profile
@login_required
def editprofileadmin(request, user_id):
    user = get_object_or_404(User, pk = user_id)  # Get the user or return 404
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)

    # Ensure the logged-in user is editing their profile or has admin rights
    if logged_user != user and not logged_user.is_staff:
        return redirect('viewprofileadmin', user_id=logged_user.id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES ,instance=user)
        form1 = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request, 'Profile successfully Edited')
            return redirect('viewprofileadmin', user_id=user.id)  # Redirect to the updated profile
    else:
        form = RegistrationForm(instance=user)  # Populate the form with existing user data
        form1 = ProfileForm(instance=user.profile)  # Populate the form with existing profile data

    context = {
        'form': form,
        'form1': form1,
        'logged_user': logged_user,
        'profile' : profile
    }
    return render(request, 'adminpanel/editprofile_admin.html', context)



# View to add a new blog post
@login_required
def addblogadmin(request):
    logged_user = request.user
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Populate the form with POST data
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Set the author to the currently logged-in user
            blog.save()
            messages.success(request, 'Blog successfully shared')
            return redirect('blogviewadmin', blog_id=blog.id)  # Redirect to the new blog post
    else:
        form = BlogForm()  # Instantiate an empty form
    return render(request, 'adminpanel/addblogadmin.html', {'form': form, 'logged_user': logged_user})



@login_required
def blogviewadmin(request, blog_id):
    blog = get_object_or_404(Blog, id = blog_id)
    comments = Comment.objects.filter(blog = blog , status = 'show' ) 
    logged_user = request.user
    profile = Profile.objects.get(user=logged_user)
     # Fetch approved comments for this blog
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = logged_user
            comment.created_at = timezone.now()
            comment.blog = blog
            comment.status = 'show'
            comment.author = request.user  # Assuming you have an 'author' field in your Comment model
            comment.save()
            return redirect('blogviewadmin', blog_id=blog.id)  # Redirect back to the same blog page after comment submission
    else:
        
        form = CommentForm()
    count = comments.count()    
    context = {
        'blog': blog, 
        'comments': comments, 
        'form': form , 
        'logged_user': logged_user , 
        'count' : count ,
        'profile' : profile,
        'comments' : comments ,
        'count' : count,
        
        
    }   
    
    return render(request, 'adminpanel/blog_view_admin.html', context)


# View to display a list of all users with their profiles
@login_required
def userlistadmin(request):
    logged_user = request.user
    profiles = Profile.objects.select_related('user').all()
    context = {
        'profiles': profiles,
        'logged_user': logged_user,
    }
    return render(request, 'adminpanel/user_list_admin.html', context)


# View to display a user's profile
@login_required
def viewprofileadmin(request, user_id):
    logged_user = request.user
    user = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user)
    context = {
        'profile': profile,
        'logged_user': logged_user,
        'user': user
    }
    return render(request, 'adminpanel/view_profile_admin.html', context)


# View to edit a blog post
@login_required
def editblogadmin(request, blog_id):
    logged_user = request.user
    blog = get_object_or_404(Blog, id=blog_id)

    # Check if the request method is POST, meaning form submission
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)  # Populate form with existing blog data
        if form.is_valid():  # Validate form data
            form.save()  # Save form data to update the blog post
            return redirect('myblogsadmin')  # Redirect to user's blogs after saving
    else:
        form = BlogForm(instance=blog)  # Populate form with existing blog data for GET request

    return render(request, 'adminpanel/editblogadmin.html', {
        'logged_user': logged_user,
        'form': form
    })


# View to delete a blog post
@login_required
def deleteblogadmin(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Retrieve the blog post or return 404 if not found

    # Check if the request method is POST, meaning form submission
    if request.method == 'POST':
        blog.delete()  # Delete the blog post from the database
        messages.success(request, 'Blog successfully deleted')  # Display success message
        return redirect('myblogsadmin')  # Redirect to user's blogs after deletion

    return render(request, 'adminpanel/deleteblogadmin.html', {'blogs': blog})


# View to list all users
@login_required
def user_list(request):
    logged_user = request.user
    users = User.objects.all()  # Retrieve all users from the database

    return render(request, 'adminpanel/user_list.html', {
        'logged_user': logged_user,
        'users': users
    })


# View to list all published blogs
@login_required
def bloglistadmin(request):
    logged_user = request.user
    all_blogs = Blog.objects.exclude(status='draft')  # Exclude draft blogs from the list

    return render(request, 'adminpanel/blog_list_admin.html', {
        'logged_user': logged_user,
        'all_blogs': all_blogs
    })


# View to hide a blog post
@login_required
def hide_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Retrieve the blog post or return 404 if not found
    blog.status = 'hide'  # Set the blog status to 'hide' to hide the blog post
    blog.save()  # Save the updated status in the database
    messages.success(request, 'Blog successfully hidden.')  # Display success message

    return redirect('bloglistadmin')  # Redirect to the admin blog list page


# View to show hidden blogs
@login_required
def blogs_hidden(request):
    logged_user = request.user
    hidden_blogs = Blog.objects.filter(status='hide')  # Retrieve all hidden blogs

    return render(request, 'adminpanel/blog_list_admin.html', {
        'logged_user': logged_user,
        'hidden_blogs': hidden_blogs,
    })


# View to publish a hidden blog
@login_required
def show_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Retrieve the blog post or return 404 if not found
    blog.status = 'published'  # Set the blog status to 'published' to publish the blog post
    blog.save()  # Save the updated status in the database
    messages.success(request, 'Blog successfully unhidden.')  # Display success message

    return redirect('bloglistadmin')  # Redirect to the admin blog list page


# View to hide a comment
@login_required
def hide_comments(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Retrieve the comment or return 404 if not found

    # Check if the request method is POST, meaning form submission
    if request.method == 'POST':
        comment.status = 'hide'  # Set the comment status to 'hide' to hide the comment
        comment.save()  # Save the updated status in the database
        messages.success(request, 'Comment is hidden successfully.')  # Display success message

        return redirect('blogviewadmin', blog_id=comment.blog.id)  # Redirect back to the blog page after comment hidden


# View to activate a user account
@login_required
def activate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Retrieve the user or return 404 if not found
    user.is_active = True  # Set the user's 'is_active' field to True to activate the account
    user.save()  # Save the updated status in the database
    messages.success(request, f"{user.username} has been activated successfully.")  # Display success message

    return redirect('userlistadmin')  # Redirect to the admin user list page


# View to deactivate a user account
@login_required
def deactivate_user(request, user_id):
    user = get_object_or_404(User, id=user_id)  # Retrieve the user or return 404 if not found
    user.is_active = False  # Set the user's 'is_active' field to False to deactivate the account
    user.save()  # Save the updated status in the database
    messages.success(request, f"{user.username} has been deactivated successfully.")  # Display success message

    return redirect('userlistadmin')  # Redirect to the admin user list page


# View to reset the password for the logged-in user
@login_required
def resetpasswordadmin(request):
    if request.method == 'POST':
        form = PasswordResetForm(user=request.user, data=request.POST)  # Populate form with POST data
        if form.is_valid():  # Validate form data
            user = form.save()  # Save form data to reset the user's password
            update_session_auth_hash(request, user)  # Update the session to prevent logout
            messages.success(request, 'Password successfully reset')  # Display success message
            return redirect('user_login')  # Redirect to login page after password reset
    else:
        form = PasswordResetForm(user=request.user)  # Populate form with existing user data for GET request

    return render(request, 'userpanel/resetpassword.html', {'form': form})  # Render password reset form template
