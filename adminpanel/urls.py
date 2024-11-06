from django.urls import  path
from .views import  admin_home,  blogviewadmin , bloglistadmin , viewprofileadmin ,myblogsadmin , userlistadmin , editblogadmin , deleteblogadmin , addblogadmin , resetpasswordadmin , editprofileadmin  , blogs_hidden , hide_blog , hide_comments , deleteblogadmin , show_blog , activate_user , deactivate_user
from django.views.generic import TemplateView


urlpatterns = [
    path('', admin_home , name='admin_home'),
    path('addblogadmin/',addblogadmin, name='addblogadmin'),
    path('deleteblog_admin/<int:blog_id>/',deleteblogadmin, name='deleteblogadmin'),
    path('blog_list_admin/', bloglistadmin , name='bloglistadmin'),
    path('hidden-blogs/', blogs_hidden, name='hidden_blogs'),
    path('hide-blog/<int:blog_id>/', hide_blog, name='hide_blog'),
    path('show_blog/<int:blog_id>/', show_blog, name='show_blog'),
    path('hide_comments/<int:comment_id>/', hide_comments, name='hide_comments'),
    path('user_list_admin/', userlistadmin , name='userlistadmin'),
    path('view_profile_admin/<int:user_id>/', viewprofileadmin , name='viewprofileadmin'),
    path('my_blogs_admin/', myblogsadmin , name='myblogsadmin'),
    path('blog_view_admin/<int:blog_id>/', blogviewadmin , name='blogviewadmin'),
    path('editblogadmin/<int:blog_id>/', editblogadmin , name='editblogadmin'),
    path('resetpassword/', resetpasswordadmin, name='resetpasswordadmin'),
    path('password_reset_done/', TemplateView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('editprofile_admin/<int:user_id>/', editprofileadmin, name='editprofileadmin'),
    path('activate_user/<int:user_id>/', activate_user, name='activate_user'),
    path('deactivate_user/<int:user_id>/', deactivate_user, name='deactivate_user'),
    
   
]
