from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('check_username/', views.check_username, name='check_username'),
    path('check_nickname/', views.check_nickname, name='check_nickname'),
] 