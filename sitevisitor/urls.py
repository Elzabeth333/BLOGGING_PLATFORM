from django.urls import  path
from .views import forgot_password, home, user_login, otp, registration  , view_blog_site , contact_us
urlpatterns = [
    path('',home , name='home'),
    path('user_login/', user_login , name='user_login'),
    path('registration/', registration , name='registration'),
    path('contact_us', contact_us , name='contact_us'),
    path('forgot/', forgot_password , name ='forgot_password'),
    path('otp/', otp , name ='otp'),
    path('view_blog_site/<int:blog_id>/', view_blog_site, name='view_blog_site'),
   
   
]
