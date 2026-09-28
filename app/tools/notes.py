from pathlib import Path


NOTES_FILE = Path("data/notes.txt")


def create_note(text: str) -> str:
    NOTES_FILE.parent.mkdir(exist_ok=True)

    with NOTES_FILE.open("a", encoding="utf-8") as file:
        file.write(text.strip() + "\n")

    return "Заметка сохранена."


def get_notes() -> list[str]:
    if not NOTES_FILE.exists():
        return []

    with NOTES_FILE.open("r", encoding="utf-8") as file:
        return [
            line.rstrip("\n")
            for line in file
            if line.strip()
        ]


def get_note(index: int) -> str | None:
    notes = get_notes()

    if index < 0 or index >= len(notes):
        return None

    return notes[index]


def delete_note(index: int) -> str:
    notes = get_notes()

    if index < 0 or index >= len(notes):
        return "Ошибка: такой заметки нет."

    deleted_note = notes.pop(index)

    NOTES_FILE.parent.mkdir(exist_ok=True)

    with NOTES_FILE.open("w", encoding="utf-8") as file:
        for note in notes:
            file.write(note + "\n")

    return f"Заметка удалена: {deleted_note}"