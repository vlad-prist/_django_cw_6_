from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from blog.models import Blog
from main.models import Settings, Client, Message, Attempt
from main.forms import SettingsForm, SettingsManagerForm, ClientForm, ClientManagerForm, MessageForm, MessageManagerForm


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'main/client_list.html'

    # permission_required = ['main.see_list_of_clients',
    #                        'main.ban_clients', ]
    #
    # def get_queryset(self):
    #     '''просмотр объектов только одного пользователя'''
    #     if self.request.user.is_authenticated:
    #         return Client.objects.filter(owner=self.request.user)
    #     elif [self.request.user.has_perm(i for i in self.permission_required)]:
    #         return Client.objects.filter(permissions=self.permission_required)


class ClientDetailView(DetailView):
    model = Client
    template_name = 'main/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    success_url = reverse_lazy('main:client_list')
    form_class = ClientForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    success_url = reverse_lazy('main:client_list')
    form_class = ClientForm

    permission_required = ['main.see_list_of_clients',
                           'main.ban_clients', ]

    def get_object(self, queryset=None):
        '''просмотреть и изменить только свои рассылки'''
        obj = super().get_object()
        if obj.owner == self.request.user or [self.request.user.has_perm(i for i in self.permission_required)]:
            return obj
        raise PermissionDenied

    def get_form_class(self):
        '''группа менеджеров может редактировать определенные поля'''
        # permission_required = ['main.see_list_of_clients',
        #                        'main.ban_clients',]
        user = self.request.user
        if user == self.object.owner:
            return ClientForm
        elif [user.has_perm(i for i in self.permission_required)]:
            return ClientManagerForm
        raise PermissionDenied


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')

    def get_object(self, queryset=None):
        '''просмотреть и изменить только свои рассылки'''
        obj = super().get_object()
        if obj.owner == self.request.user:
            return obj
        raise PermissionDenied


class SettingsListView(ListView):
    model = Settings
    template_name = 'main/setting_list.html'

    def get_queryset(self):
        '''просмотр объектов только одного пользователя'''
        if self.request.user.is_authenticated:
            return Settings.objects.filter(owner=self.request.user)


class SettingsDetailView(DetailView):
    model = Settings
    template_name = 'main/setting_detail.html'


class SettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Settings
    success_url = reverse_lazy('main:setting_list')
    form_class = SettingsForm

    def form_valid(self, form):
        '''при создании рассылки присваивается автор(владелец)'''
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        '''пользоватеь видит только свои рассылки'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class SettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Settings
    success_url = reverse_lazy('main:setting_list')
    form_class = SettingsForm
    permission_required = ['main.see_any_mailing_settings',
                           'main.switch_of_mailing_settings', ]

    def get_object(self, queryset=None):
        '''просмотреть и изменить только свои рассылки'''
        obj = super().get_object()
        if obj.owner == self.request.user or [self.request.user.has_perm(i for i in self.permission_required)]:
            return obj
        raise PermissionDenied

    def get_form_kwargs(self):
        '''пользователь видит только свои рассылки'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return SettingsForm
        elif [user.has_perm(i for i in self.permission_required)]:
            return SettingsManagerForm
        raise PermissionDenied


class SettingsDeleteView(DeleteView):
    model = Settings
    success_url = reverse_lazy('main:setting_list')

    def get_object(self, queryset=None):
        '''просмотреть и изменить только свои рассылки'''
        obj = super().get_object()
        if obj.owner == self.request.user:
            return obj
        raise PermissionDenied


class MessageListView(ListView):
    model = Message
    template_name = 'main/message_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    template_name = 'main/message_detail.html'


class MessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')

    def form_valid(self, form):
        '''при создании сообщения присваивается автор(владелец)'''
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        '''пользоватеь видит только свои сообщения'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Message
    success_url = reverse_lazy('main:message_list')
    form_class = MessageForm

    def get_object(self, queryset=None):
        '''просмотреть и изменить только свои сообщения'''
        obj = super().get_object()
        if obj.owner == self.request.user or self.request.user.has_perm('change_mailing_message'):
            return obj
        raise PermissionDenied

    def get_form_kwargs(self):
        '''пользоватеь видит только свои сообщения'''
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MessageForm
        elif user.has_perm('change_mailing_message'):
            return MessageManagerForm
        raise PermissionDenied


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.owner == self.request.user:
            return obj
        raise PermissionDenied


class AttemptListView(ListView):
    model = Attempt

    def get_context_data(self, **kwargs):
        '''метод для отображения общей информации на главной страницы'''
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список рассылок'
        context['mailings_all'] = len(Settings.objects.all())
        context['mailing_active'] = len(Settings.objects.filter(status='started'))
        context['clients_unique'] = len(Client.objects.all().distinct()) #distinct - уникальные объекты
        context['blog'] = Blog.objects.all()[:3] # выбор трех последних статей
        return context
