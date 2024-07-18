from django.shortcuts import render
from django.views.generic import CreateView, UpdateView

from users.models import User


class RegisterView(CreateView):
    model = User


class ProfileView(UpdateView):
    model = User