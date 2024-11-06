from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Blog, Comment
from .forms import ProfileForm,  CommentForm , BlogForm
from django.contrib.auth.decorators import login_required

# Example view for blog creation
@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Blog created successfully.')
            return redirect('blog_detail', pk=blog.pk)
        else:
            messages.error(request, 'Error creating blog. Please check the form.')
    else:
        form = BlogForm()
    return render(request, 'blog/create.html', {'form': form})


# Other CRUD views (update, delete, read) would follow similar patterns
