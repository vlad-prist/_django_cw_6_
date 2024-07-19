import secrets

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy, reverse

from django.core.mail import send_mail
from users.models import User
from users.forms import UserRegisterForm, UserProfileForm
from config.settings import EMAIL_HOST_USER


class UserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение регистрации',
            message=f'Привет! Перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse("main:main_page")


class GeneratePasswordView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'users/generate.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        if user:
            password = User.objects.make_random_password(length=10)
            user.set_password(password)
            user.save()
            send_mail(
                subject='Смена пароля',
                message=f'Привет! Ваш новый пароль: {password}',
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        return redirect(reverse('users:login'))


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
