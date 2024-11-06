from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True)
    id_proof = models.ImageField(upload_to='id_proofs/', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
    
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    blog_image = models.ImageField(upload_to='blog_images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=150)
    
    

    def __str__(self):
        return self.title
    


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.blog.title}'
