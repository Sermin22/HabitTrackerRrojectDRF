from django.core.exceptions import ValidationError
from django.db import models
from config import settings
from habits.validators import validate_periodicity_days, validate_execution_time


class Habit(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name="Пользователь создавший привычку", on_delete=models.CASCADE,
        related_name="habits", blank=True, null=True,
    )
    place = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Место выполнения",
        help_text="Укажите место для выполнения привычки",
    )
    time = models.TimeField(verbose_name="Время для выполнения", help_text="Укажите время когда выполнять привычку",)
    action = models.TextField(verbose_name="Описание действия", help_text="Опишите действие, представляющее привычку",)
    is_pleasant_habit = models.BooleanField(default=False, verbose_name="Приятная привычка?")
    related_habit = models.ForeignKey(
        "self", on_delete=models.SET_NULL, blank=True, null=True,
        verbose_name="Связанная c полезной приятная привычка",
        related_name="pleasurable_habits",
        help_text="Добавьте связанную приятную привычку",
        limit_choices_to={"is_pleasant_habit": True}
    )
    periodicity_days = models.PositiveIntegerField(
        default=1, verbose_name="Периодичность (дней)",
        help_text="Добавьте приятную привычку к полезной",
        validators=[validate_periodicity_days],
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Время на выполнение (в секундах)",
        help_text="Укажите время на выполнение привычки (в секундах, для полезной - не более 120 сек)",
        validators=[validate_execution_time],
    )
    public = models.BooleanField(
        default=False, verbose_name="Публикация привычки",
        help_text="Опубликуйте привычку",
    )

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def clean(self):
        if self.related_habit and self.reward:
            raise ValidationError("Невозможно выбрать одновременно и связанную привычку, и вознаграждение.")
        if self.is_pleasant_habit and (self.reward or self.related_habit):
            raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки.")

    def __str__(self):
        return f"{self.action[:50]} - {self.time} - {self.place}"
