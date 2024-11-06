from django.shortcuts import render, get_object_or_404, redirect
from adminpanel.models import Profile, Blog, Comment, User
from django.contrib import messages
from .forms import BlogForm, CommentForm, PasswordResetForm , ProfileForm , RegistrationForm
from django.contrib.auth import authenticate, logout , update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db import transaction
from .forms import PasswordResetForm

# Home view for logged-in users
def user_home(request):
    logged_user = request.user
    blogs = Blog.objects.filter(status='published')  # Fetch all blogs
    return render(request, 'userpanel/user_home.html', {
        'logged_user': logged_user,
        'blogs': blogs
    })


# View to add a new blog post
@login_required
def add_blog(request):
    logged_user = request.user
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)  # Populate the form with POST data
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user  # Set the author to the currently logged-in user
            blog.save()
            if blog.status == 'Published':
                messages.success(request, 'Blog successfully shared')
            else:
                messages.success(request, 'Blog successfully Drafted')
            return redirect('view_blog', blog_id=blog.id)  # Redirect to the new blog post
    else:
        form = BlogForm()  # Instantiate an empty form
    return render(request, 'userpanel/add_blog.html', {'form': form, 'logged_user': logged_user})



# View to edit a blog post
def editblog(request, blog_id):
    logged_user = request.user
    blogs = get_object_or_404(Blog, id=blog_id)  # Get the blog post or return 404
    if request.method == 'POST':
        blogs_form = BlogForm(request.POST, request.FILES, instance=blogs)  # Populate the form with POST data
        if blogs_form.is_valid():
            blogs_form.save()
            return redirect('myownblogs')  # Redirect to user's blogs after saving
    else:
        blogs_form = BlogForm(instance=blogs)  # Populate the form with existing blog data
    return render(request, 'userpanel/editblog.html', {
        'logged_user': logged_user,
        'form': blogs_form
    })


# View to display a blog post with comments
@login_required
def view_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)  # Get the blog post or return 404
    comments = Comment.objects.filter(blog=blog , status = 'show')  # Fetch all comments for the blog
    logged_user = request.user
    profile = Profile.objects.get(user=logged_user)  # Get the profile of the logged-in user

    if request.method == 'POST':
        form = CommentForm(request.POST)  # Populate the form with POST data
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = logged_user
            comment.created_at = timezone.now()
            comment.blog = blog
            comment.status = 'show'
            comment.save()
            return redirect('view_blog', blog_id=blog.id)  # Redirect back to the same blog page after comment submission
    else:
        form = CommentForm()  # Instantiate an empty form

    count = comments.count()  # Count the number of comments
    context = {
        'blog': blog,
        'comments': comments,
        'form': form,
        'logged_user': logged_user,
        'count': count,
        'profile': profile,
    }
    return render(request, 'userpanel/view_blog.html', context)





# # View to display a blog post with comments
# @login_required
# def view_blog(request, blog_id):
#     blog = get_object_or_404(Blog, id=blog_id)  # Get the blog post or return 404
#     comments = Comment.objects.filter(blog=blog)  # Fetch all comments for the blog
#     logged_user = request.user
#     profile = Profile.objects.get(user=logged_user)  # Get the profile of the logged-in user

#     if request.method == 'POST':
#         form = CommentForm(request.POST)  # Populate the form with POST data
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = logged_user
#             comment.created_at = timezone.now()
#             comment.blog = blog
#             comment.save()
#             return redirect('view_blog', blog_id=blog.id)  # Redirect back to the same blog page after comment submission
#     else:
#         form = CommentForm()  # Instantiate an empty form

#     count = comments.count()  # Count the number of comments
#     context = {
#         'blog': blog,
#         'comments': comments,
#         'form': form,
#         'logged_user': logged_user,
#         'count': count,
#         'profile': profile,
#     }
#     return render(request, 'userpanel/view_blog.html', context)



# View to delete a blog post
def deleteblog(request, blog_id):
    blogs = get_object_or_404(Blog, id=blog_id)  # Get the blog post or return 404
    if request.method == 'POST':
        blogs.delete()
        messages.success(request, 'Blog successfully deleted')
        return redirect('myownblogs')  # Redirect to user's blogs after deletion
    return render(request, 'userpanel/delete_blog.html', {'blogs': blogs})



# View to delete a comment
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Get the comment or return 404
    if request.method == 'POST':
        comment.delete()  # Delete the comment
        messages.success(request, 'Comment successfully deleted')
    return redirect('view_blog', blog_id=comment.blog.id)  # Redirect back to the blog page after comment deletion






# View to edit a user's profile
@login_required
def edit_profile(request, user_id):
    user = get_object_or_404(User, pk = user_id)  # Get the user or return 404
    logged_user = request.user
    profile = get_object_or_404(Profile, user = logged_user)

    # Ensure the logged-in user is editing their profile or has admin rights
    if logged_user != user and not logged_user.is_staff:
        return redirect('view_profile', user_id=logged_user.id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES ,instance=user)
        form1 = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if form.is_valid() and form1.is_valid():
            form.save()
            form1.save()
            messages.success(request, 'Profile successfully Edited')
            return redirect('view_profile', user_id=user.id)  # Redirect to the updated profile
    else:
        form = RegistrationForm(instance=user)  # Populate the form with existing user data
        form1 = ProfileForm(instance=user.profile)  # Populate the form with existing profile data

    context = {
        'form': form,
        'form1': form1,
        'logged_user': logged_user,
        'profile' : profile
    }
    return render(request, 'userpanel/edit_profile.html', context)



# View to display a user's profile
@login_required
def view_profile(request, user_id):
    logged_user = request.user
    user = get_object_or_404(User, id=user_id)  # Get the user or return 404
    profile = get_object_or_404(Profile, user=user)  # Get the profile or return 404

    context = {
        'profile': profile,
        'logged_user': logged_user,
        'user': user
    }
    return render(request, 'userpanel/view_profile.html', context)


# Temporary view for testing or placeholder
def temp(request):
    return render(request, 'userpanel/temp.html')


# View to list all blogs by the logged-in user
def bloglist(request):
    logged_user = request.user
    blogs = Blog.objects.filter(author=request.user)
    return render(request, 'userpanel/bloglist.html', {
        'logged_user': logged_user,
        'blogs': blogs
    })



# View to display a list of the logged-in user's blogs
@login_required
def my_blogs(request):
    logged_user = request.user
    # Fetch all blogs authored by the logged-in user
    all_blogs = Blog.objects.filter(author=logged_user)
    return render(request, 'userpanel/myblogs.html', {
        'logged_user': logged_user,
        'all_blogs': all_blogs,
        'published_blogs': all_blogs.filter(status='published'),
        'draft_blogs': all_blogs.filter(status='draft'),
    })

@login_required
def my_blogs_published(request):
    logged_user = request.user
    # Fetch blogs authored by the logged-in user with status 'published'
    published_blogs = Blog.objects.filter(author=logged_user, status='published')
    return render(request, 'userpanel/myblogs.html', {
        'logged_user': logged_user,
        'all_blogs': published_blogs,
        'published_blogs': published_blogs,
        'draft_blogs': Blog.objects.filter(author=logged_user, status='draft' ),
    })

@login_required
def my_blogs_draft(request):
    logged_user = request.user
    # Fetch blogs authored by the logged-in user with status 'draft'
    draft_blogs = Blog.objects.filter(author=logged_user, status='draft')
    return render(request, 'userpanel/myblogs.html', {
        'logged_user': logged_user,
        'all_blogs': draft_blogs,  # Provide the same template, but filtered for draft blogs
        'published_blogs': Blog.objects.filter(author=logged_user, status='published'),  # Provide published blogs as well
        'draft_blogs': draft_blogs,
    })


# View to log out the user
def user_logout(request):
    logout(request)  # Log out the user
    return redirect('home')



# View to reset the user's password

@login_required
def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password successfully Reset')  # Important for keeping the user logged in
            return redirect('user_login')
    else:
        form = PasswordResetForm(user=request.user)

    return render(request, 'userpanel/resetpassword.html', {'form': form})
