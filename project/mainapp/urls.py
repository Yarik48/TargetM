from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chat/<int:chat_id>/', views.chat, name='chat'),
    path('group/<int:group_id>/', views.group, name='group'),
    path('create_chat/', views.create_chat, name='create_chat'),
    path('send_message/<int:chat_id>/', views.send_message, name='send_message'),
    path('register', views.register,name='register'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('logout', views.logout, name='logout'),
]
