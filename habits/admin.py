from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'place', 'time', 'action', 'is_pleasant_habit', 'related_habit',
                    'periodicity_days', 'reward', 'execution_time', 'public')
    list_filter = ('owner', 'is_pleasant_habit', 'related_habit', 'public')
    search_fields = ('place', 'action', 'reward')
