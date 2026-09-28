import json
import time

import ollama


FAST_MODEL = "qwen2.5:0.5b"
SMART_MODEL = "qwen2.5:3b"

MAX_CONTEXT_MESSAGES = 20


SYSTEM_PROMPT = """
Ты — мозг голосового ассистента Кай.

Твоя задача — понять запрос пользователя и выбрать действие.

Ты работаешь с инструментами:

create_note
get_notes
delete_note

create_reminder
get_reminders
delete_reminder

chat

Правила:

1. Отвечай ТОЛЬКО валидным JSON.
2. Не добавляй markdown.
3. Не добавляй пояснения вне JSON.
4. Если пользователь хочет сохранить информацию, используй create_note.
5. Если пользователь хочет узнать свои заметки, используй get_notes.
6. Если пользователь хочет удалить заметку, используй delete_note.
7. Если пользователь хочет создать напоминание, используй create_reminder.
8. Если пользователь хочет посмотреть напоминания, используй get_reminders.
9. Если пользователь хочет удалить напоминание, используй delete_reminder.
10. Для обычного разговора используй chat.
11. Используй предыдущие сообщения разговора для понимания слов
    "это", "последнее", "тот", "ту", "запиши это" и подобных ссылок
    на предыдущий контекст.
12. Не придумывай действия, которых нет среди инструментов.

Формат одного действия:

{
    "action": "create_note",
    "text": "текст заметки"
}

Для delete_note:

{
    "action": "delete_note",
    "index": 1
}

Для create_reminder:

{
    "action": "create_reminder",
    "text": "текст напоминания",
    "when": "завтра в 18:00"
}

Для delete_reminder:

{
    "action": "delete_reminder",
    "index": 1
}

Для get_notes:

{
    "action": "get_notes"
}

Для get_reminders:

{
    "action": "get_reminders"
}

Для обычного разговора:

{
    "action": "chat"
}

Если нужно выполнить несколько действий:

{
    "actions": [
        {
            "action": "..."
        },
        {
            "action": "..."
        }
    ]
}
"""


def _extract_json(text: str) -> dict:
    text = text.strip()

    try:
        result = json.loads(text)

        if isinstance(result, dict):
            return result

    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "Модель не вернула JSON."
        )

    fragment = text[
        start:end + 1
    ]

    result = json.loads(
        fragment
    )

    if not isinstance(result, dict):
        raise ValueError(
            "JSON должен быть объектом."
        )

    return result


def _validate_result(
    result: dict,
) -> dict:
    if "actions" in result:
        if not isinstance(
            result["actions"],
            list,
        ):
            raise ValueError(
                "Поле actions должно быть списком."
            )

        return result

    if "action" not in result:
        raise ValueError(
            "В JSON отсутствует action."
        )

    return result


def analyze_command(
    messages: list[dict],
    model: str = FAST_MODEL,
) -> dict:
    prompt_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        }
    ]

    prompt_messages.extend(
        messages[
            -MAX_CONTEXT_MESSAGES:
        ]
    )

    start = time.perf_counter()

    response = ollama.chat(
        model=model,
        messages=prompt_messages,
        options={
            "temperature": 0,
        },
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    print()
    print(
        "[LLM]"
    )

    print(
        f"Модель: {model}"
    )

    print(
        f"Время: {elapsed:.2f} сек."
    )

    raw = response["message"]["content"]

    try:
        result = _extract_json(
            raw
        )

        return _validate_result(
            result
        )

    except (
        ValueError,
        json.JSONDecodeError,
    ):
        print(
            "[LLM] Первая попытка "
            "вернула некорректный JSON."
        )

        repair_messages = [
            {
                "role": "system",
                "content": (
                    SYSTEM_PROMPT
                    + "\n\n"
                    + "Предыдущий ответ был "
                    "некорректным. "
                    "Верни только исправленный "
                    "валидный JSON."
                ),
            }
        ]

        repair_messages.extend(
            messages[
                -MAX_CONTEXT_MESSAGES:
            ]
        )

        repair_messages.append(
            {
                "role": "user",
                "content": (
                    "Исправь предыдущий "
                    "ответ и верни только JSON."
                ),
            }
        )

        repair_response = ollama.chat(
            model=model,
            messages=repair_messages,
            options={
                "temperature": 0,
            },
        )

        repaired = (
            repair_response[
                "message"
            ][
                "content"
            ]
        )

        result = _extract_json(
            repaired
        )

        return _validate_result(
            result
        )


def generate_response(
    messages: list[dict],
    user_text: str,
    execution_results: list[str],
    model: str = FAST_MODEL,
) -> str:
    results_text = "\n".join(
        execution_results
    )

    response_messages = [
        {
            "role": "system",
            "content": """
Ты — голосовой ассистент Кай.

Ответь пользователю естественно и кратко на русском языке.

Учитывай результат выполненного действия.

Не упоминай:
- JSON
- инструменты
- Executor
- модели
- внутреннюю архитектуру

Не повторяй без необходимости весь текст пользователя.

Если действие уже выполнено, просто сообщи результат.
""",
        }
    ]

    response_messages.extend(
        messages[
            -MAX_CONTEXT_MESSAGES:
        ]
    )

    response_messages.append(
        {
            "role": "user",
            "content": (
                "Последний запрос:\n"
                f"{user_text}\n\n"
                "Результат выполнения:\n"
                f"{results_text}\n\n"
                "Сформулируй короткий "
                "естественный ответ."
            ),
        }
    )

    start = time.perf_counter()

    response = ollama.chat(
        model=model,
        messages=response_messages,
        options={
            "temperature": 0.4,
        },
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    print(
        f"[LLM RESPONSE] "
        f"Модель: {model}"
    )

    print(
        f"[LLM RESPONSE] "
        f"Время: {elapsed:.2f} сек."
    )

    return (
        response["message"]["content"]
        .strip()
    )