import sqlite3
from pathlib import Path
from typing import List, Optional
from .models import Task
from datetime import datetime

DEFAULT_DB_PATH = Path.home() / ".tasker" / "tasks.db"


class TaskDB:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = Path(db_path) if db_path else DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # Use check_same_thread=False for safe usage from different threads (optional)
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._ensure_tables()

    def _ensure_tables(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                done INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def add_task(self, title: str, description: str = "") -> int:
        cur = self.conn.cursor()
        created = datetime.utcnow().isoformat()
        cur.execute(
            "INSERT INTO tasks (title, description, done, created_at) VALUES (?, ?, 0, ?)",
            (title, description, created),
        )
        self.conn.commit()
        return cur.lastrowid

    def list_tasks(self, show_all: bool = True) -> List[Task]:
        cur = self.conn.cursor()
        if show_all:
            cur.execute("SELECT id, title, description, done, created_at FROM tasks ORDER BY id DESC")
        else:
            cur.execute("SELECT id, title, description, done, created_at FROM tasks WHERE done=0 ORDER BY id DESC")
        rows = cur.fetchall()
        return [Task.from_row((r["id"], r["title"], r["description"], r["done"], r["created_at"])) for r in rows]

    def get_task(self, task_id: int) -> Optional[Task]:
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, description, done, created_at FROM tasks WHERE id=?", (task_id,))
        row = cur.fetchone()
        return Task.from_row((row["id"], row["title"], row["description"], row["done"], row["created_at"])) if row else None

    def complete_task(self, task_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        return cur.rowcount > 0

    def close(self):
        self.conn.close()
