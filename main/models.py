from django.db import models
from django.conf import settings

NULLABLE = {"blank": True, "null": True}


class Client(models.Model):
    ''' Клиент сервиса '''
    email = models.EmailField(verbose_name="Почта для рассылки")
    first_name = models.CharField(max_length=150, verbose_name="Имя", **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name="Фамилия", **NULLABLE)
    comment = models.TextField(verbose_name="Комментарий", **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Settings(models.Model):
    ''' Рассылка (настройки) '''
    PERIOD_DAILY = "Ежедневно"
    PERIOD_WEEKLY = "weekly"
    PERIOD_MONTHLY = "monthly"

    PERIOD_CHOICES = (
        (PERIOD_DAILY, "Ежедневно"),
        (PERIOD_WEEKLY, "Еженедельно"),
        (PERIOD_MONTHLY, "Ежемесячно"),
    )

    STATUS_CREATED = "created"
    STATUS_STARTED = "started"
    STATUS_DONE = "done"

    STATUS_CHOICES = (
        (STATUS_CREATED, "Создана"),
        (STATUS_STARTED, "Запущена"),
        (STATUS_DONE, "Завершена"),
    )

    start_time = models.DateTimeField(verbose_name="Время начала")
    end_time = models.DateTimeField(verbose_name="Время завершения", **NULLABLE)
    period = models.CharField(
        max_length=20,
        choices=PERIOD_CHOICES,
        default=PERIOD_DAILY,
        verbose_name="Период рассылки",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
        verbose_name="Статус рассылки",
    )
    message = models.ForeignKey(
        "Message", on_delete=models.CASCADE, verbose_name="сообщения", **NULLABLE
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, related_name="mailing_settings")

    def __str__(self):
        return f"{self.start_time} / {self.period}"

    class Meta:
        verbose_name = "Настройки рассылки"
        verbose_name_plural = "Настройки рассылок"


class Message(models.Model):
    ''' Сообщение для рассылки '''
    subject = models.CharField(max_length=150, verbose_name="Тема письма")
    letter = models.TextField(verbose_name="Тело письма")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class Attempt(models.Model):
    ''' Попытка рассылки (CRUD не описывается)'''
    STATUS_OK = "ok"
    STATUS_FAILED = "failed"
    STATUS_CHOICES = (
        (STATUS_OK, "Успешно"),
        (STATUS_FAILED, "Не удалось"),
    )

    last_try = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата последней попытки"
    )
    client = models.ForeignKey(
        Client, on_delete=models.SET_NULL, verbose_name="Клиент", **NULLABLE
    )
    settings = models.ForeignKey(
        Settings, on_delete=models.SET_NULL, verbose_name="Настройки", **NULLABLE
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=STATUS_OK, verbose_name="Статус"
    )
    server_response = models.CharField(verbose_name='статус', max_length=350, **NULLABLE)

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

