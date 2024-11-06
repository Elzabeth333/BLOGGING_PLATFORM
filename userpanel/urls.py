from django.urls import path
from .views import add_blog, my_blogs,   user_home, view_blog ,  bloglist ,  user_logout ,editblog, temp, deleteblog, delete_comment,  view_profile , edit_profile , reset_password , my_blogs_published , my_blogs_draft
from django.views.generic import TemplateView

urlpatterns = [
    path('',user_home, name='user_home'),
    path('add_blog/',add_blog, name='add_blog'),
    path('bloglist/', bloglist, name='bloglist'),
    path('my_blogs/', my_blogs, name='myownblogs'),
    path('my_blogs/published/', my_blogs_published, name='my_blogs_published'),
    path('my_blogs/draft/', my_blogs_draft, name='my_blogs_draft'),
    path('editblog/<int:blog_id>/',editblog, name='editblog'),
    path('deleteblog/<int:blog_id>/',deleteblog, name='deleteblog'),
    path('view_blog/<int:blog_id>/', view_blog, name='view_blog'),
    path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
    path('edit-profile/<int:user_id>/', edit_profile, name='editprofileuser'),
    path('view_profile/<int:user_id>/', view_profile, name='view_profile'),
    path('logout/',user_logout,name='sign_out'),
    path('temp/',temp,name='temp'),
    path('resetpassword/', reset_password, name='reset_password'),
    path('password_reset_done/', TemplateView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    
]