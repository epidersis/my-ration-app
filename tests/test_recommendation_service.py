from app.services.recommendation_service import (
    HIGH_CALORIES_MESSAGE,
    LOW_CALORIES_MESSAGE,
    NO_DATA_MESSAGE,
    NORMAL_CALORIES_MESSAGE,
    get_daily_recommendation,
)


def test_recommendation_no_data() -> None:
    assert get_daily_recommendation(None, has_dishes=False) == NO_DATA_MESSAGE


def test_recommendation_low_calories() -> None:
    assert get_daily_recommendation(1499, has_dishes=True) == LOW_CALORIES_MESSAGE


def test_recommendation_normal_lower_boundary() -> None:
    assert get_daily_recommendation(1500, has_dishes=True) == NORMAL_CALORIES_MESSAGE


def test_recommendation_normal_upper_boundary() -> None:
    assert get_daily_recommendation(2200, has_dishes=True) == NORMAL_CALORIES_MESSAGE


def test_recommendation_high_calories() -> None:
    assert get_daily_recommendation(2200.1, has_dishes=True) == HIGH_CALORIES_MESSAGE

