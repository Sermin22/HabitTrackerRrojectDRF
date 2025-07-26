from django.db import models
from config import settings


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
    )
    reward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Вознаграждение")
    execution_time = models.PositiveIntegerField(
        default=120, verbose_name="Время на выполнение (в секундах)",
        help_text="Укажите время на выполнение привычки (в секундах, не более 120 сек, "
                  "по умолчанию 120 сек.)",
    )
    public = models.BooleanField(
        default=False, verbose_name="Публикация привычки",
        help_text="Опубликуйте привычку",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"

    def __str__(self):
        return f"{self.action[:50]} - {self.time} - {self.place}"
