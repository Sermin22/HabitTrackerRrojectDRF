from rest_framework.serializers import ValidationError


def validate_execution_time(value):
    """
    Проверка времени выполнения привычки (не более 120 секунд).
    """
    if value > 120:
        raise ValidationError(f"Время выполнения привычки превышает допустимое значение (120 мин.). "
                              f"Текущее значение: {value}")


def validate_periodicity_days(value):
    """
    Периодичность выполнения привычки должна быть не меньше 1 раза в 7 дней.
    """
    if value > 7:
        raise ValidationError(f"Привычка выполняется недостаточно часто (менее 1 раза в 7 дней). "
                              f"Текущее значение: {value}.")
