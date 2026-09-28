import re

from .tools.notes import create_note


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def extract_note_text(text: str):
    lowered = text.lower()

    markers = [
        "запиши дословно:",
        "запиши дословно",
        "запиши:",
        "запиши",
        "сохрани:",
        "сохрани",
        "добавь в заметки:",
        "добавь в заметки",
        "сделай заметку:",
        "сделай заметку",
    ]

    for marker in markers:
        position = lowered.find(marker)

        if position != -1:
            value = text[position + len(marker):].strip()

            if value:
                return value

    return None


def route_command(user_text: str):
    text = normalize_text(user_text)

                               
             
                               

    note_text = extract_note_text(text)

    if note_text is not None:
        return {
            "action": "create_note",
            "arguments": {
                "text": note_text,
            },
        }

                               
                    
                               

    return {
        "action": "chat",
        "arguments": {},
    }


def execute_command(command):
    action = command["action"]
    arguments = command["arguments"]

    if action == "create_note":
        return create_note(
            arguments["text"]
        )

    return None