from django.contrib import admin
from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'place', 'time', 'action', 'is_pleasant_habit', 'related_habit',
                    'periodicity_days', 'reward', 'execution_time', 'public', 'created_at', 'updated_at')
    list_filter = ('owner', 'is_pleasant_habit', 'related_habit', 'public')
    search_fields = ('place', 'action', 'reward')
