from habits.models import Habit
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class HabitSerializer(ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
