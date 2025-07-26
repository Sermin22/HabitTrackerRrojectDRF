from celery import shared_task
from django.utils import timezone
from habits.models import Habit
from habits.services import send_telegram_massage


@shared_task
def send_habit_reminder():
    today = timezone.now().date()
    habits = Habit.objects.filter(owner__isnull=False)
    for habit in habits:
        start_date = habit.updated_at.date()
        days_since_update = (today - start_date).days  # получаем сколько дней с обновления
        message = (
            f"Сегодня нужно выполнить привычку: {habit.action[:50]} в {habit.time.strftime('%H:%M')} - {habit.place}"
        )
        if habit.owner.tg_chat_id and days_since_update % habit.periodicity_days == 0:
            send_telegram_massage(habit.owner.tg_chat_id, message)
