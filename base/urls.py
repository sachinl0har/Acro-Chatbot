from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('chat/', views.index, name='chat'),
    path('profile/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
]