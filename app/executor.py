from .tools.notes import (
    create_note,
    get_notes,
    delete_note,
)

from .tools.reminders import (
    create_reminder,
    get_reminders,
    delete_reminder,
    format_reminders,
)

from .tools.reminder_parser import (
    parse_reminder_time,
)


def execute_action(action: dict) -> str:
    action_type = action.get("action")

             

    if action_type == "create_note":
        text = action.get("text")

        if not text:
            return "Ошибка: текст заметки не указан."

        return create_note(text)

    if action_type == "get_notes":
        notes = get_notes()

        if not notes:
            return "Сохранённых заметок пока нет."

        lines = []

        for index, note in enumerate(
            notes,
            start=1,
        ):
            lines.append(
                f"{index}. {note}"
            )

        return (
            "Твои заметки:\n"
            + "\n".join(lines)
        )

    if action_type == "delete_note":
        index = action.get("index")

        if index is None:
            return (
                "Ошибка: номер заметки не указан."
            )

        try:
            index = int(index)

        except (TypeError, ValueError):
            return (
                "Ошибка: номер заметки "
                "должен быть числом."
            )

        return delete_note(index - 1)

                 

    if action_type == "create_reminder":
        text = action.get("text")
        when = action.get("when")

        if not text:
            return (
                "Ошибка: текст напоминания "
                "не указан."
            )

        if not when:
            return (
                "Ошибка: время напоминания "
                "не указано."
            )

        try:
            due_at = parse_reminder_time(
                when
            )

        except ValueError as error:
            return f"Ошибка: {error}"

        return create_reminder(
            text,
            due_at,
        )

    if action_type == "get_reminders":
        reminders = get_reminders()

        return format_reminders(
            reminders
        )

    if action_type == "delete_reminder":
        reminder_id = action.get("index")

        if reminder_id is None:
            return (
                "Ошибка: номер напоминания "
                "не указан."
            )

        try:
            reminder_id = int(reminder_id)

        except (TypeError, ValueError):
            return (
                "Ошибка: номер напоминания "
                "должен быть числом."
            )

        deleted = delete_reminder(
            reminder_id
        )

        if not deleted:
            return (
                "Ошибка: такого напоминания нет."
            )

        return (
            f"Напоминание #{reminder_id} удалено."
        )

                      

    if action_type == "chat":
        return "Обычный разговор."

    return "Действие не поддерживается."


def execute_actions(
    result: dict,
    messages: list[dict],
) -> list[str]:

    if "actions" in result:
        actions = result["actions"]
    else:
        actions = [result]

    results = []

    for action in actions:
        results.append(
            execute_action(action)
        )

    return results