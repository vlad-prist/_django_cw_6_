from django.core.cache import cache

from config.settings import CACHE_ENABLED
from main.models import Settings, Client


def get_settings_list_from_cache():
    """ Получает данные по категориям из кеша, если кеш пуст, то данные берутся из БД """
    if not CACHE_ENABLED:
        return Settings.objects.all()
    key = 'settings_list'
    settings_list = cache.get(key)
    if settings_list is not None:
        return settings_list
    settings_list = Settings.objects.all()  # Берем данные из БД
    cache.set(key, settings_list, 60 * 60) # Кеширование на 1 час
    return settings_list


def get_clients_list_from_cache():
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = 'clients_list'
    clients_list = cache.get(key)
    if clients_list is not None:
        return clients_list
    clients_list = Client.objects.all()  # Берем данные из БД
    cache.set(key, clients_list, 60 * 60) # Кеширование на 1 час
    return clients_list
