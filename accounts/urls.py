from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy, re_path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_change/', views.password_change, name='password_change'),
    path('signup/', views.signup, name='signup'),
    path('edit/', views.profile_edit, name='profile_edit'),

    re_path(r'^(?P<username>[\w.@+-]+)/follow/$', views.user_follow, name='user_follow'),
    re_path(r'^(?P<username>[\w.@+-]+)/unfollow/$', views.user_unfollow, name='user_unfollow'),

]