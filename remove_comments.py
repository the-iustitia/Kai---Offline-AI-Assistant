import io
import os
import tokenize


PROJECT_DIR = r"C:\Users\KnightBits\Desktop\Workspace\ai-assistant"


def remove_comments_from_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()

    try:
        tokens = tokenize.generate_tokens(
            io.StringIO(source).readline
        )
        tokens = list(tokens)
    except tokenize.TokenError:
        print(f"[SKIP] Ошибка разбора: {file_path}")
        return

    new_tokens = []

    for token in tokens:
        if token.type == tokenize.COMMENT:
            continue

        new_tokens.append(token)

    cleaned_source = tokenize.untokenize(new_tokens)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(cleaned_source)

    print(f"[OK] {file_path}")


def main():
    for root, dirs, files in os.walk(PROJECT_DIR):
        # Не трогаем служебные каталоги.
        dirs[:] = [
            directory
            for directory in dirs
            if directory not in {
                "__pycache__",
                ".git",
                ".venv",
                "venv",
            }
        ]

        for file_name in files:
            if not file_name.endswith(".py"):
                continue

            file_path = os.path.join(root, file_name)

            # Не обрабатываем сам этот скрипт.
            if os.path.abspath(file_path) == os.path.abspath(__file__):
                continue

            remove_comments_from_file(file_path)


if __name__ == "__main__":
    main()