from __future__ import annotations

from app.db.database import init_db
from app.ui.app import run


def main() -> None:
    init_db()
    run()


if __name__ == "__main__":
    main()

