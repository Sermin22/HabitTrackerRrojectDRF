from habits.models import Habit
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from habits.validators import validator_periodicity_days, validator_execution_time


class HabitSerializer(ModelSerializer):
    periodicity_days = serializers.IntegerField(validators=[validator_periodicity_days])
    execution_time = serializers.IntegerField(validators=[validator_execution_time])
    related_habit = serializers.PrimaryKeyRelatedField(
        queryset=Habit.objects.all(),  # Habit.objects.filter(is_pleasant_habit=True)
        required=False,
        allow_null=True
    )
    reward = serializers.CharField(
        required=False,
        allow_null=True
    )

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["owner"]  # запретить пользователю указывать owner вручную при создании или обновлении
        # привычки через API

    def validate(self, data):
        # Проверка на невозможность совместного выбора
        if data.get("related_habit") and data.get("reward"):
            raise serializers.ValidationError("Невозможно выбрать одновременно и связанную привычку, "
                                              "и вознаграждение.")
        # Если привычка помечена как приятная, то не может быть связанной привычки и вознаграждения
        if data.get("is_pleasant_habit") is True:
            if data.get("reward"):
                raise serializers.ValidationError("У приятной привычки не может быть вознаграждения.")
            if data.get("related_habit"):
                raise serializers.ValidationError("У приятной привычки не может быть связанной привычки.")
        return data

    def validate_related_habit(self, value):
        if value and not value.is_pleasant_habit:
            raise serializers.ValidationError("В связанные можно выбирать только приятные привычки.")
        return value

        # # Еще вариант в validate Проверка на запрет вознаграждения и связанной привычки для приятных привычек
        # if data.get("is_pleasant_habit") and (data.get("reward") or data.get("related_habit")):
        #     raise serializers.ValidationError("У приятной привычки не может быть вознаграждения "
        #                                       "или связанной привычки.")

        # # Можно в validate Проверка periodicity_days через внешний вылидатор
        # if "periodicity_days" in data:
        #     validator_periodicity_days(data.get("periodicity_days"))
        # # Можно в validate Проверяем execution_time через внешний вылидатор
        # if "execution_time" in data:
        #     validator_execution_time(data.get("execution_time"))

    # def validate_periodicity_days(self, value):
    #     # Вызываем внешний валидатор для проверки periodicity_days
    #     validator_periodicity_days(value)
    #     return value

    # def validate_execution_time(self, value):
    #     # Вызываем внешний валидатор для проверки execution_time
    #     validator_execution_time(value)
    #     return value

    # def validate_execution_time(self, value):
    #     # Проверяем поле "execution_time" в зависимости от значения "is_pleasant_habit"
    #     instance = getattr(self, "instance", None)
    #     if not instance or not instance.is_pleasant_habit:
    #         # Если это полезная привычка или создается новая, проводим проверку времени (не более 120 сек.),
    #         # если это приятная привычка, то время может быть больше
    #         if value > 120:
    #             raise serializers.ValidationError("Время выполнения полезной привычки "
    #                                               "не должно превышать 120 минут.")
    #     return value
