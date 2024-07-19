from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserRegisterView, ProfileView, GeneratePasswordView, email_verification, UserListView

app_name = UsersConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('generate-password/', GeneratePasswordView.as_view(
        template_name='users/generate_password.html'), name='generate-password'),
    path('generate-password/done/', GeneratePasswordView.as_view(
        template_name='users/generate_password_done.html'), name='generate-password-done'),
    path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
    path('', UserListView.as_view(), name='user_list'),
]
