from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from main.models import Settings, Client, Message, Attempt
from main.forms import SettingsForm, SettingsManagerForm, ClientForm, ClientManagerForm, MessageForm, MessageManagerForm


# def index(request):
#     if request.method == "POST":
#         name = request.POST.get("name")
#         email = request.POST.get("email")
#         message = request.POST.get("message")
#         print(f'{name} ({email}: {message})')
#
#     return render(request, 'main/index.html')


class ClientListView(ListView):
    model = Client
    template_name = 'main/client_list.html'

    # def get_queryset(self):
    #     '''просмотр объектов только одного пользователя'''
    #     return Client.objects.filter(owner=self.request.user)


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

    # def get_queryset(self):
    #     '''просмотр объектов только одного пользователя'''
    #     return Settings.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        '''зачем эта функция?'''
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = 'Список рассылки'
        context_data['mailings_all'] = len(Settings.objects.all())
        context_data['mailing_active'] = len(Settings.objects.filter(status='started'))
        context_data['clients_unique'] = len(Client.objects.all().distinct())
        # context_data['blog'] = Blog.objects.all()[:3] # выбор трех последних статей
        return context_data


class SettingsDetailView(DetailView):
    model = Settings
    template_name = 'main/setting_detail.html'


class SettingsCreateView(CreateView):
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


class SettingsUpdateView(UpdateView):
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

    # def get_queryset(self):
    #     Message.objects.filter(owner=self.request.user)


class MessageDetailView(DetailView):
    model = Message
    template_name = 'main/message_detail.html'


class MessageCreateView(CreateView):
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


class MessageUpdateView(UpdateView):
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
    extra_context = {
        'attempt_list': model,
    }
