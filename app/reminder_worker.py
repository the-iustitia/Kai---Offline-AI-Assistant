import tkinter as tk

from app.tools.reminders import (
    get_due_reminders,
    complete_reminder,
)


CHECK_INTERVAL = 10_000


def check_reminders(root: tk.Tk):
    try:
        reminders = get_due_reminders()

        for reminder in reminders:
            show_reminder(
                root,
                reminder,
            )

            complete_reminder(
                reminder["id"]
            )

    except Exception as error:
        print(
            "Ошибка системы напоминаний:",
            error,
        )

    finally:
        root.after(
            CHECK_INTERVAL,
            check_reminders,
            root,
        )


def show_reminder(
    root: tk.Tk,
    reminder: dict,
):
    window = tk.Toplevel(root)

    window.title(
        "Кай — напоминание"
    )

    window.geometry(
        "400x220"
    )

    window.resizable(
        False,
        False,
    )

    window.transient(root)

    window.grab_set()

    title = tk.Label(
        window,
        text="НАПОМИНАНИЕ",
        font=(
            "Segoe UI",
            18,
            "bold",
        ),
    )

    title.pack(
        pady=(30, 15)
    )

    text = tk.Label(
        window,
        text=reminder["text"],
        font=(
            "Segoe UI",
            12,
        ),
        wraplength=340,
        justify="center",
    )

    text.pack(
        padx=20,
        pady=10,
    )

    button = tk.Button(
        window,
        text="Понятно",
        font=(
            "Segoe UI",
            11,
        ),
        command=window.destroy,
    )

    button.pack(
        pady=15
    )


def start_reminder_worker(
    root: tk.Tk,
):
    print(
        "Система напоминаний запущена."
    )

    root.after(
        0,
        check_reminders,
        root,
    )