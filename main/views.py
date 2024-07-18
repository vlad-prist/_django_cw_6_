from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from main.models import Settings, Client, Message, Attempt
from main.forms import SettingsForm


def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        print(f'{name} ({email}: {message})')

    return render(request, 'main/main_page.html')


class ClientListView(ListView):
    model = Client
    template_name = 'main/client_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'main/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('main:client_list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('main:client_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')


class SettingsListView(ListView):
    model = Settings
    template_name = 'main/setting_list.html'


class SettingsDetailView(DetailView):
    model = Settings
    template_name = 'main/setting_detail.html'


class SettingsCreateView(CreateView):
    model = Settings
    success_url = reverse_lazy('main:setting_list')
    form_class = SettingsForm


class SettingsUpdateView(UpdateView):
    model = Settings
    success_url = reverse_lazy('main:setting_list')
    form_class = SettingsForm


class SettingsDeleteView(DeleteView):
    model = Settings
    success_url = reverse_lazy('main:setting_list')


class MessageListView(ListView):
    model = Message
    template_name = 'main/message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'main/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('main:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    fields = '__all__'
    success_url = reverse_lazy('main:message_list')


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')


class AttemptListView(ListView):
    model = Attempt
