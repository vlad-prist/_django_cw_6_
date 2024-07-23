# Generated by Django 4.2 on 2024-07-22 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="settings",
            options={
                "permissions": [
                    ("see_any_mailing_settings", "Просмотр любых рассылок"),
                    ("see_list_of_users", "Просмотр списка пользователей сервиса"),
                    ("ban_users", "Блокирование пользователей сервиса"),
                    ("switch_of_mailing_settings", "Отключение рассылки"),
                    ("change_mailing_settings", "Редактирование рассылки"),
                    ("manage_list_of_mailing_settings", "Управление списком рассылки"),
                    (
                        "change_mailing_settings_and_message",
                        "Изменение рассылки и сообщения",
                    ),
                ],
                "verbose_name": "Настройки рассылки",
                "verbose_name_plural": "Настройки рассылок",
            },
        ),
    ]
