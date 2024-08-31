from django.urls import path
from interestsapp import views as views
from interestsapp import user_creation_views as user_creation_views
from interestsapp import interest_views as interest_views

urlpatterns = [
    path('', views.login, name=''),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user_creation/', user_creation_views.user_creation, name='user_creation'),
    path('register_user/', user_creation_views.register_user, name='register_user'),
    path('logout/', views.logout, name='logout'),
    path('sendInterest/', interest_views.sendInterest, name='sendInterest'),
    path('sendResponse/', interest_views.sendResponse, name='sendResponse'),
    path('chat/<int:sender_id>/<int:receiver_id>/', views.chat_room, name='chat_room'),
]
