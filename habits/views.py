from rest_framework.generics import ListAPIView
from habits.models import Habit
from habits.serilizers import HabitSerializer


class HabitListAPIView(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
