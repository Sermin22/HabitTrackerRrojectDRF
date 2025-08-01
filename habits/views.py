from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.paginators import HabitsPagination
from habits.serilizers import HabitSerializer
from users.permissions import IsOwnerOrReadOnly


class HabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = HabitsPagination

    def get_queryset(self):
        # Только привычки текущего пользователя и публичные
        return Habit.objects.filter(owner=self.request.user) | Habit.objects.filter(public=True)


class HabitCreateAPIView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    # User, создавший привычку становится владельцем этой привычки
    def perform_create(self, serializer):
        habit = serializer.save()
        habit.owner = self.request.user
        habit.save()


class HabitRetrieveAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class HabitUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class HabitDestroyAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


# class PublicHabitsListAPIView(ListAPIView):
#     queryset = Habit.objects.all()  # Habit.objects.filter(public=True) можно тут без get_queryset
#     serializer_class = HabitSerializer
#     permission_classes = [IsAuthenticated]
#     pagination_class = HabitsPagination
#
#     def get_queryset(self):
#         # Фильтруем и выводим только опубликованные привычки
#         return Habit.objects.filter(public=True)
