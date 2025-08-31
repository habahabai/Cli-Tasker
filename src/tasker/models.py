from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    done: bool
    created_at: str

    @classmethod
    def from_row(cls, row):
        """Accepts a row-like tuple (id, title, description, done, created_at)."""
        if row is None:
            return None
        return cls(id=row[0], title=row[1], description=row[2], done=bool(row[3]), created_at=row[4])
