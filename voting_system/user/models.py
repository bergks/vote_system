from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )

    class Meta:
        abstract = True

class User(models.Model):
    username = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Логин'
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Имя',
    )
    surname = models.CharField(
        max_length=128,
        null=True,
        blank=True,
        verbose_name='Фамилия',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
