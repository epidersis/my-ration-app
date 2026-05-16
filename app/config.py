from __future__ import annotations

import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
APP_ENV = os.getenv("APP_ENV", "development")
DB_PATH = Path(os.getenv("APP_DB_PATH", BASE_DIR / "data" / "my_ration.sqlite3"))

