from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timedelta

from app.db.models import Dish
from app.db.repositories import DishRepository


class StatsService:
    def __init__(self, dishes: DishRepository | None = None) -> None:
        self.dishes = dishes or DishRepository()

    def get_period_dishes(self, user_id: int, period: str) -> list[Dish]:
        start_at, end_at = self._period_bounds(period)
        return self.dishes.list_for_period(user_id, start_at, end_at)

    def summarize(self, dishes: list[Dish]) -> dict[str, object]:
        grouped: dict[str, float] = defaultdict(float)
        for dish in dishes:
            day = dish.created_at[:10]
            grouped[day] += dish.total_calories
        return {
            "total": round(sum(dish.total_calories for dish in dishes), 2),
            "by_day": dict(sorted(grouped.items())),
        }

    def _period_bounds(self, period: str) -> tuple[str | None, str | None]:
        now = datetime.now()
        today = datetime(now.year, now.month, now.day)
        if period == "day":
            return today.isoformat(timespec="seconds"), (today + timedelta(days=1)).isoformat(
                timespec="seconds"
            )
        if period == "week":
            start = today - timedelta(days=today.weekday())
            return start.isoformat(timespec="seconds"), (start + timedelta(days=7)).isoformat(
                timespec="seconds"
            )
        if period == "month":
            start = datetime(now.year, now.month, 1)
            end = datetime(now.year + (now.month == 12), 1 if now.month == 12 else now.month + 1, 1)
            return start.isoformat(timespec="seconds"), end.isoformat(timespec="seconds")
        if period == "year":
            start = datetime(now.year, 1, 1)
            end = datetime(now.year + 1, 1, 1)
            return start.isoformat(timespec="seconds"), end.isoformat(timespec="seconds")
        return None, None

