from django.db import models
from user.models import User, BaseModel

# Create your models here.
class Poll(BaseModel):
    class PollStatus(models.TextChoices):
        ACTIVE = "AC", "Активно"
        FINISHED = "FN", "Завершено"
    
    question = models.CharField(
        max_length=256,
        verbose_name='Вопрос')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание')
    status = models.CharField(
        max_length=2,
        choices=PollStatus,
        default=PollStatus.ACTIVE,
        verbose_name='Статус'
    )
    choices = models.ManyToManyField(
        'candidates.Candidate',
        related_name='polls',
        verbose_name='Варианты ответа'
    )

    class Meta:
        verbose_name = 'Голосование'
        verbose_name_plural = 'Голосования'

    def __str__(self):
        return self.question

class Vote(BaseModel):
    poll = models.ForeignKey(
        Poll,
        on_delete=models.CASCADE,
        related_name='votes',
        null=True,
        verbose_name='Голосование'
    )
    choice = models.ForeignKey(
        'candidates.Candidate',
        on_delete=models.CASCADE,
        related_name='votes',
        verbose_name='Выбор'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='votes',
        verbose_name='Пользователь'
    )

    class Meta:
            verbose_name = 'Голос'
            verbose_name_plural = 'Голоса'
