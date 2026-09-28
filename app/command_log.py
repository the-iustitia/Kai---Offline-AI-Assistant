from pathlib import Path
import json
import sqlite3
from datetime import datetime


DATABASE_FILE = Path(
    "data/command_log.db"
)


def _connect():
    DATABASE_FILE.parent.mkdir(
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_command_log():
    with _connect() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                action TEXT NOT NULL,
                command_text TEXT NOT NULL,
                action_data TEXT NOT NULL,
                created_at TEXT NOT NULL,
                use_count INTEGER NOT NULL DEFAULT 1
            )
            """
        )

        connection.commit()


def normalize_text(text: str) -> str:
    text = text.lower().strip()

    chars = []

    for char in text:
        if char.isalnum() or char.isspace():
            chars.append(char)
        else:
            chars.append(" ")

    text = "".join(chars)

    return " ".join(
        text.split()
    )


def should_log_action(
    action: dict,
) -> bool:
    action_type = action.get(
        "action"
    )

    if action_type in (
        None,
        "",
        "chat",
        "create_note",
    ):
        return False

    return True


def log_command(
    command_text: str,
    action: dict,
):
    if not should_log_action(
        action
    ):
        return

    action_type = action.get(
        "action"
    )

    normalized = normalize_text(
        command_text
    )

    if not normalized:
        return

    action_data = json.dumps(
        action,
        ensure_ascii=False,
    )

    now = datetime.now().isoformat(
        timespec="seconds"
    )

    init_command_log()

    with _connect() as connection:
        row = connection.execute(
            """
            SELECT id
            FROM commands
            WHERE action = ?
              AND command_text = ?
            LIMIT 1
            """,
            (
                action_type,
                normalized,
            ),
        ).fetchone()

        if row:
            connection.execute(
                """
                UPDATE commands
                SET use_count = use_count + 1,
                    created_at = ?
                WHERE id = ?
                """,
                (
                    now,
                    row["id"],
                ),
            )

        else:
            connection.execute(
                """
                INSERT INTO commands (
                    action,
                    command_text,
                    action_data,
                    created_at,
                    use_count
                )
                VALUES (?, ?, ?, ?, 1)
                """,
                (
                    action_type,
                    normalized,
                    action_data,
                    now,
                ),
            )

        connection.commit()


def get_commands() -> list[dict]:
    init_command_log()

    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT
                id,
                action,
                command_text,
                action_data,
                created_at,
                use_count
            FROM commands
            ORDER BY use_count DESC, id DESC
            """
        ).fetchall()

    commands = []

    for row in rows:
        try:
            action_data = json.loads(
                row["action_data"]
            )

        except json.JSONDecodeError:
            action_data = {
                "action": row["action"]
            }

        commands.append(
            {
                "id": row["id"],
                "action": row["action"],
                "command_text": row[
                    "command_text"
                ],
                "action_data": action_data,
                "created_at": row[
                    "created_at"
                ],
                "use_count": row[
                    "use_count"
                ],
            }
        )

    return commands