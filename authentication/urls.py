from django.urls import path
from authentication.views import sign_up ,user_login ,user_logout

urlpatterns = [
    path('signup', sign_up, name='add User'),
    path('signin', user_login),
    path('logout', user_logout)
]