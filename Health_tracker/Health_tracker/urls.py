from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('exercise/', views.exercise, name='exercise'),
    path('diet/', views.diet, name='diet'),
]