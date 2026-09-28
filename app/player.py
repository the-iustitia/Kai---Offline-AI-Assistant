import winsound
from pathlib import Path


def play_audio(
    file_path: str | Path,
):
    file_path = Path(
        file_path
    )

    if not file_path.exists():
        raise FileNotFoundError(
            f"Аудиофайл не найден: "
            f"{file_path}"
        )

    winsound.PlaySound(
        str(file_path),
        winsound.SND_FILENAME,
    )