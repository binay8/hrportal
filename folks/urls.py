from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    # path('user_landing/', views.user_landing, name='user_landing'),
    path('login/', views.login, name='login'),
    path('create/', views.create, name='create'),
    path('request-leave/', views.request_leave, name='request_leave'),
    path('view-leave-requests/', views.view_leave_requests, name='view_leave'), 
]