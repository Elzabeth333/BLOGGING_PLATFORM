from django.contrib import admin
from .models import Blog, Profile, Comment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Blog)
admin.site.register(Comment)



