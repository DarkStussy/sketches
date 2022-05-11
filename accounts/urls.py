from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login_user/', views.login_user, name='login-user'),
    path('profile/', views.profile, name='profile'),
    path('add_answer/<int:order_id>/', views.add_answer, name='add_answer'),
]
