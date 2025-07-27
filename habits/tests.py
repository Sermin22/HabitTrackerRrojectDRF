from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from django.urls import reverse
from habits.models import Habit


class HabitTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@mail.ru")
        self.habit = Habit.objects.create(
            owner=self.user,
            place="Комната дома",
            time="07:00",
            action="Сделать комплекс упражнений",
            is_pleasant_habit=False,
            reward="Легкий завтрак из свежих фруктов и орехов",
            periodicity_days=1,
            execution_time=120,
            public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        '''Проверяем вывод привычки'''
        url = reverse("habits:habit_retrieve", args=[self.habit.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("action"), "Сделать комплекс упражнений"
        )

    def test_habit_create(self):
        '''Проверяем создание привычки'''
        url = reverse("habits:habit_create")
        data = {
            "owner": self.user,
            "place": "Парк",
            "time": "07:30",
            "action": "Бегать 30 минут",
            "is_pleasant_habit": False,
            "periodicity_days": 1,
            "execution_time": 120,
            "public": True
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Habit.objects.all().count(), 2
        )
        result = response.json()
        self.assertEqual(
            result.get("action"), "Бегать 30 минут"
        )

    def test_habit_update(self):
        '''Проверяем изменение привычки'''
        url = reverse("habits:habit_update", args=[self.habit.pk])
        data = {
            "action": "Быстрая ходьба 1 час"
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = response.json()
        self.assertEqual(
            result.get("action"), "Быстрая ходьба 1 час"
        )

    def test_habit_delete(self):
        '''Проверяем удаление привычки'''
        url = reverse("habits:habit_delete", args=[self.habit.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Habit.objects.all().count(), 0
        )

    def test_related_habit_validation(self):
        # Создаем приятную привычку
        pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00",
            action="Пить кофе",
            is_pleasant_habit=True,
            periodicity_days=1,
            execution_time=120,
            public=False
        )
        # Создаем полезную привычку с привязкой приятной
        useful_habit = Habit.objects.create(
            owner=self.user,
            place="Офис",
            time="09:00",
            action="Чтение",
            is_pleasant_habit=False,
            related_habit=pleasant_habit,
            periodicity_days=1,
            execution_time=120,
            public=True
        )
        self.assertEqual(useful_habit.related_habit, pleasant_habit)

    def test_invalid_related_habit(self):
        """Нельзя добавить связанную привычку, если она не отмечена как приятная"""
        wrong_related = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="07:00",
            action="Зарядка",
            is_pleasant_habit=False
        )
        url = reverse("habits:habit_create")
        data = {
            "owner": self.user,
            "place": "Стадион",
            "time": "06:30",
            "action": "Пробежка",
            "is_pleasant_habit": False,
            "related_habit": wrong_related.pk,
            "periodicity_days": 1,
            "execution_time": 120,
            "public": False
        }
        response = self.client.post(url, data)
        # Проверка кода ошибки
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка наличия сообщения об исключении
        result = response.json()
        self.assertIn("related_habit", result)
        self.assertIn("В связанные можно выбирать только приятные привычки.", result["related_habit"])

    def test_invalid_related_habit_and_reward(self):
        '''Проверка валидности на невозможность выбрать одновременно
        и связанную привычку, и вознаграждение'''

        # Создаем приятную привычку
        pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00",
            action="Пить кофе",
            is_pleasant_habit=True,
            )
        reward = "Игра"  # вознаграждение
        url = reverse("habits:habit_create")
        data = {
            "owner": self.user,
            "place": "Стадион",
            "time": "06:30",
            "action": "Пробежка",
            "is_pleasant_habit": False,
            "related_habit": pleasant_habit.pk,
            "reward": reward,
            "periodicity_days": 1,
            "execution_time": 120,
            "public": False
        }
        response = self.client.post(url, data)
        # Проверка кода ошибки
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка наличия сообщения об исключении
        result = response.json()
        self.assertIn("Невозможно выбрать одновременно и связанную привычку, и вознаграждение.",
                      result["non_field_errors"])

    def test_invalid_pleasant_habit_related_habit(self):
        '''Проверяем, что у приятной привычки не может быть связанной привычки'''

        # Создаем приятную привычку
        pleasant_habit = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="08:00",
            action="Пить кофе",
            is_pleasant_habit=True,
        )
        url = reverse("habits:habit_create")
        data = {
            "owner": self.user,
            "place": "Дом",
            "time": "08:30",
            "action": "Пить чай",
            "is_pleasant_habit": True,
            "related_habit": pleasant_habit.pk,
            "periodicity_days": 1,
            "execution_time": 120,
            "public": False
        }
        response = self.client.post(url, data)
        # Проверка кода ошибки
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка наличия сообщения об исключении
        result = response.json()
        self.assertIn("У приятной привычки не может быть связанной привычки.",
                      result["non_field_errors"])

    def test_invalid_pleasant_habit_reward(self):
        '''Проверяем, что у приятной привычки не может быть вознаграждения'''

        reward = "Игра"  # вознаграждение
        url = reverse("habits:habit_create")
        data = {
            "owner": self.user,
            "place": "Дом",
            "time": "08:30",
            "action": "Пить чай",
            "is_pleasant_habit": True,
            "reward": reward,
            "periodicity_days": 1,
            "execution_time": 120,
            "public": False
        }
        response = self.client.post(url, data)
        # Проверка кода ошибки
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Проверка наличия сообщения об исключении
        result = response.json()
        self.assertIn("У приятной привычки не может быть вознаграждения.",
                      result["non_field_errors"])