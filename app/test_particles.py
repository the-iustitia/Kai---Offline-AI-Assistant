import tkinter as tk

from app.particle_core import ParticleCore


def main():
    root = tk.Tk()

    root.title("Кай — Particle Core")
    root.geometry("700x700")
    root.resizable(False, False)

    canvas = tk.Canvas(
        root,
        width=700,
        height=700,
        background="#05070a",
        highlightthickness=0,
    )

    canvas.pack()

    core = ParticleCore(
        canvas,
        width=700,
        height=700,
        particle_count=1800,
    )

    def set_idle():
        core.set_state("idle")

    def set_listening():
        core.set_state("listening")

    def set_processing():
        core.set_state("processing")

    def set_speaking():
        core.set_state("speaking")

    def set_error():
        core.set_state("error")

    def set_reminder():
        core.set_state("reminder")

    controls = tk.Frame(
        root,
        background="#05070a",
    )

    controls.place(
        x=10,
        y=10,
    )

    buttons = [
        ("IDLE", set_idle),
        ("LISTEN", set_listening),
        ("THINK", set_processing),
        ("SPEAK", set_speaking),
        ("ERROR #", set_error),
        ("REMINDER !", set_reminder),
    ]

    for text, command in buttons:
        button = tk.Button(
            controls,
            text=text,
            command=command,
            bg="#111820",
            fg="#69d9ff",
            activebackground="#1c2c38",
            activeforeground="#ffffff",
            relief="flat",
            borderwidth=0,
        )

        button.pack(
            side="left",
            padx=3,
        )

    def close():
        core.stop()
        root.destroy()

    root.protocol(
        "WM_DELETE_WINDOW",
        close,
    )

    root.mainloop()


if __name__ == "__main__":
    main()