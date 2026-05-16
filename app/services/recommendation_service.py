from __future__ import annotations


NO_DATA_MESSAGE = "Нет данных для рекомендации. Добавьте блюда за день."
LOW_CALORIES_MESSAGE = "Калорий мало. Проверьте, достаточно ли вы поели сегодня."
NORMAL_CALORIES_MESSAGE = "Рацион примерно в пределах нормы."
HIGH_CALORIES_MESSAGE = (
    "Вы за сегодня съели слишком много. Позанимайтесь спортом, чтобы сжечь лишнее."
)


def get_daily_recommendation(total_calories: float | None, has_dishes: bool = True) -> str:
    if not has_dishes or total_calories is None:
        return NO_DATA_MESSAGE
    if total_calories < 1500:
        return LOW_CALORIES_MESSAGE
    if total_calories <= 2200:
        return NORMAL_CALORIES_MESSAGE
    return HIGH_CALORIES_MESSAGE

