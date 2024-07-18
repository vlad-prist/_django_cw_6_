from django.urls import path
from main.apps import MainConfig
from main.views import (
    index,
    MessageListView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    ClientListView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    SettingsListView,
    SettingsDetailView,
    SettingsCreateView,
    SettingsUpdateView,
    SettingsDeleteView,
    AttemptListView,
)


app_name = MainConfig.name

urlpatterns = [
    path('', index, name='main_page'),

    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client_detail'),
    path('clients/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('clients/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),

    path('message/', MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', MessageCreateView.as_view(), name='message_create'),
    path('message/update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),
    path('message/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),

    path('settings/', SettingsListView.as_view(), name='setting_list'),
    path('settings/<int:pk>/', SettingsDetailView.as_view(), name='setting_detail'),
    path('settings/create/', SettingsCreateView.as_view(), name='setting_create'),
    path('settings/update/<int:pk>/', SettingsUpdateView.as_view(), name='setting_update'),
    path('settings/delete/<int:pk>/', SettingsDeleteView.as_view(), name='setting_delete'),

]
