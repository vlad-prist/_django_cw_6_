# Проект "Сервис отправки рассылок"
Кусровая работа по работе с Джанго.
В данном проекте показаны основные моменты Джанго:
- Создание приложений
- Реализация CBV и FBV
- Работа с шаблонами
- Работа с формами
- Аутентификация
- Кеширование
- Работа с django apscheduler


## Использование
Для работы с данным проектом:
1. В виртуальном окружении установите [requirements.txt](https://nodejs.org/) (пакет с зависимостями) с помощью команды:
```sh
$ pip install -r requirements.txt
```

2. Добавьте в свой проект файл .env c необходимыми для работы паролями.
Пример [.env.sample](https://nodejs.org/) размещен в проекте
```typescript
SECRET_KEY=
DB_USER=
DB_PASSWORD=
EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_USE_TLS=
EMAIL_USE_SSL=
CACHE_ENABLED=True
CACHES_LOCATION=
```


## Разработка

### Требования
Для установки и запуска проекта, необходим [Django 4.2]()

## Реализовано в проекте

В данном проекте реализовано три приложения:
- main
- users
- blog


### main
Для данного приложения определены 4 класса:
- Client - Клиент сервиса
- Settings - Рассылка (настройки)
- Message - Сообщение для рассылки
- Attempt - Попытка рассылки

Для первых трех классов реализован полный CRUD.
Также в контроллерах прописаны ограничения по правам доступа
(по правам доступа также созданы формы)
В случае отсутствия прав реализован функционал raise PermissionDenied который выводит на страницу информацию 
"Страница не найдена"

В шаблонах _detail.html реализовано ограничение прав.

Распределение прав [permissions]() реализовано в models.py у классов Client, Settings, Message

Реализован метод отправки сообщений через django apscheduler [django apscheduler](https://pypi.org/project/django-apscheduler/)
(документация https://pypi.org/project/django-apscheduler/)

В директории [services]() размещен [sending.py](), в котором реалзован метод send_email [send_email]() попыток отправки сообщений 
(класс Attempt) 
[send_all_mails]() метод для отправки сообщений с определенной периодичностью, которая прописана в классе Settings

В директории [management]() > [commands]() размещен [ras.py](), в котором реалзован запуск  [django apscheduler]()
для запуска apscheduler:
```sh
$ python manage.py ras
```
Также реализован метод для отловки ошибок
В директории [management]() > [commands]() размещен [debug.py](),

## users
Реализован класс User для дальнейшего определения пользователей сервиса.

К данному классу реализован частичный CRUD и методы восстановления пароля
шаблоны для авторизации, регистрации, редактирования профиля и восстановление пароля
Реализованы формы для восстановления пароля, а также проверки уже используемого email при регистрации

В директории [management]() > [commands]() размещен [csu.py](), в котором реализован метод создания администратора (superuser)

для запуска :
```sh
$ python manage.py csu
```

## Blog
Для данного приложения реализованна модель Blog, с полным CRUD, шаблонами и шаблонными тегами для отображения изображений 


## fixtures
Созданы фикстуры по данным из БД:
- Список статей (blog_list)
- Список клиентов сервиса (clients_list)
- Список сообщений для отправки (messages_list)
- Список настроек (settings_list)
- Список авторизованных пользователей (users_list)

Для данных фикстур применялась команда:

[python -Xutf8 manage.py dumpdata <name_of_app>.<name_of_class> --indent=2 --exclude auth.permission --exclude contenttypes -o <name_list.json>]()


Фикстуры прав:
- Группы прав (auth_groups.json)
- Список добавленных прав (permissions_json)

Для данных фикстур применялась команда:

[python -Xutf8 manage.py dumpdata auth.group --indent=2 --exclude contenttypes -o auth_groups.json]()
