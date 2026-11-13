from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name='Слаг'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class Candidate(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name='Название'
    )
    director = models.CharField(
        max_length=256,
        verbose_name='Режисёр'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    category = models.ManyToManyField(
        Category,
        verbose_name='Категория',
        related_name='candidates'
    )
    description = models.TextField(
        blank=False,
        null=False,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Кандидат'
        verbose_name_plural = 'Кандидаты'
    
    def __str__(self):
        return self.title