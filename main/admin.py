from django.contrib import admin
from main.models import Client, Message


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'owner',)
    list_filter = ('owner',)
    search_fields = ('email', 'owner',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'letter', 'owner',)
    list_filter = ('subject', 'owner',)
    search_fields = ('subject', 'owner',)
