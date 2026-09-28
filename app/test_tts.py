from app.tts import (
    list_voices,
    speak,
)


def main():
    print(
        "Установленные голоса:"
    )

    list_voices()

    print()
    print(
        "Проверка голоса Кая..."
    )

    speak(
        "Привет. Я Кай. "
        "Голосовая система работает."
    )

    print()
    print(
        "Тест завершён."
    )


if __name__ == "__main__":
    main()