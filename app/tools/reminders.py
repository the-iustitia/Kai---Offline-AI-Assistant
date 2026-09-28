from datetime import datetime
from pathlib import Path
import sqlite3


DATABASE_FILE = Path("data/reminders.db")


def _connect():
    DATABASE_FILE.parent.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row

    return connection


def init_reminders():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                due_at TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        connection.commit()


def create_reminder(text: str, due_at: datetime) -> str:
    init_reminders()

    with _connect() as connection:
        cursor = connection.execute(
            """
            INSERT INTO reminders (text, due_at, done)
            VALUES (?, ?, 0)
            """,
            (
                text.strip(),
                due_at.isoformat(),
            ),
        )

        connection.commit()

        reminder_id = cursor.lastrowid

    formatted_time = due_at.strftime(
        "%d.%m.%Y %H:%M"
    )

    return (
        f"Напоминание #{reminder_id} создано на "
        f"{formatted_time}: {text.strip()}"
    )


def get_reminders(include_done: bool = False) -> list[dict]:
    init_reminders()

    with _connect() as connection:
        if include_done:
            rows = connection.execute(
                """
                SELECT id, text, due_at, done
                FROM reminders
                ORDER BY due_at
                """
            ).fetchall()
        else:
            rows = connection.execute(
                """
                SELECT id, text, due_at, done
                FROM reminders
                WHERE done = 0
                ORDER BY due_at
                """
            ).fetchall()

    return [dict(row) for row in rows]


def get_due_reminders() -> list[dict]:
    init_reminders()

    now = datetime.now().isoformat()

    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, text, due_at, done
            FROM reminders
            WHERE done = 0
              AND due_at <= ?
            ORDER BY due_at
            """,
            (now,),
        ).fetchall()

    return [dict(row) for row in rows]


def complete_reminder(reminder_id: int) -> bool:
    init_reminders()

    with _connect() as connection:
        cursor = connection.execute(
            """
            UPDATE reminders
            SET done = 1
            WHERE id = ?
              AND done = 0
            """,
            (reminder_id,),
        )

        connection.commit()

    return cursor.rowcount > 0


def delete_reminder(reminder_id: int) -> bool:
    init_reminders()

    with _connect() as connection:
        cursor = connection.execute(
            """
            DELETE FROM reminders
            WHERE id = ?
            """,
            (reminder_id,),
        )

        connection.commit()

    return cursor.rowcount > 0


def format_reminders(reminders: list[dict]) -> str:
    if not reminders:
        return "Активных напоминаний нет."

    lines = ["Твои напоминания:"]

    for reminder in reminders:
        due_at = datetime.fromisoformat(
            reminder["due_at"]
        )

        formatted_time = due_at.strftime(
            "%d.%m.%Y %H:%M"
        )

        lines.append(
            f"{reminder['id']}. "
            f"{formatted_time} — "
            f"{reminder['text']}"
        )

    return "\n".join(lines)