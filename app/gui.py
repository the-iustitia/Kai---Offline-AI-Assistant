import os
import threading
import time
import tkinter as tk

from app.audio import record_audio
from app.transcriber import transcribe_audio
from app.conversation import Conversation
from app.reminder_worker import start_reminder_worker
from app.tts import KaiTTS
from app.player import play_audio
from app.particle_core import ParticleCore


AUDIO_FILE = "data/gui_voice.wav"

VOICE_FILE = "data/kai_voice.wav"

START_WIDTH = 900
START_HEIGHT = 700

MIN_WIDTH = 600
MIN_HEIGHT = 500


def main():
    root = tk.Tk()

    root.title(
        "Кай"
    )

    root.geometry(
        f"{START_WIDTH}x{START_HEIGHT}"
    )

    root.minsize(
        MIN_WIDTH,
        MIN_HEIGHT,
    )

    root.configure(
        background="#05070a"
    )

                                                               
            
                                                               

    canvas = tk.Canvas(
        root,
        background="#05070a",
        highlightthickness=0,
    )

    canvas.pack(
        fill="both",
        expand=True,
    )

                                                               
         
                                                               

    kai = Conversation()

    print()
    print(
        "=" * 60
    )

    print(
        "КАЙ ЗАПУСКАЕТСЯ"
    )

    print(
        "=" * 60
    )

                                                               
           
                                                               

    try:
        tts = KaiTTS()

    except Exception as error:
        print()
        print(
            "[PIPER] ОШИБКА:"
        )
        print(error)
        print()

        tts = None

                                                               
                   
                                                               

    core = ParticleCore(
        canvas,
        width=START_WIDTH,
        height=START_HEIGHT,
        particle_count=1300,
    )

    core.set_state(
        "idle"
    )

                                                               
               
                                                               

    state_text = tk.StringVar(
        value="КАЙ"
    )

    state_label = tk.Label(
        root,
        textvariable=state_text,
        background="#05070a",
        foreground="#ff9d3d",
        font=(
            "Segoe UI",
            10,
            "bold",
        ),
    )

    state_label.place(
        relx=0.5,
        rely=0.94,
        anchor="center",
    )

                                                               
                 
                                                               

    def update_canvas_size(
        event=None,
    ):
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        if width <= 1 or height <= 1:
            return

        core.resize(
            width,
            height,
        )

    canvas.bind(
        "<Configure>",
        update_canvas_size,
    )

                                                               
                         
                                                               

    def set_state(
        state: str,
        text: str,
    ):
        core.set_state(
            state
        )

        state_text.set(
            text
        )

                                                               
           
                                                               

    def finish_success():
        set_state(
            "idle",
            "КАЙ",
        )

                                                               
            
                                                               

    def finish_error(
        error: str,
    ):
        print()
        print(
            "[ERROR]"
        )
        print(error)
        print()

        set_state(
            "error",
            "ОШИБКА",
        )

        root.after(
            2500,
            finish_success,
        )

                                                               
                        
                                                               

    def process_voice():
        pipeline_start = (
            time.perf_counter()
        )

        try:
                                                               
                       
                                                               

            root.after(
                0,
                set_state,
                "listening",
                "СЛУШАЮ",
            )

            print()
            print(
                "=" * 60
            )

            print(
                "[VOICE] Начало команды"
            )

            print(
                "=" * 60
            )

                                                               
                    
                                                               

            record_start = (
                time.perf_counter()
            )

            record_audio(
                AUDIO_FILE,
            )

            record_time = (
                time.perf_counter()
                - record_start
            )

            print(
                f"[VOICE] Запись: "
                f"{record_time:.2f} сек."
            )

                                                               
                     
                                                               

            root.after(
                0,
                set_state,
                "processing",
                "РАСПОЗНАЮ",
            )

            whisper_start = (
                time.perf_counter()
            )

            user_text = (
                transcribe_audio(
                    AUDIO_FILE
                )
            )

            whisper_time = (
                time.perf_counter()
                - whisper_start
            )

            print()
            print(
                "[WHISPER]"
            )

            print(
                user_text
            )

            print(
                f"[WHISPER] Время: "
                f"{whisper_time:.2f} сек."
            )

            if not user_text:
                raise RuntimeError(
                    "Whisper не смог "
                    "распознать речь."
                )

                                                               
                  
                                                               

            root.after(
                0,
                set_state,
                "processing",
                "ДУМАЮ",
            )

            qwen_start = (
                time.perf_counter()
            )

            result = kai.process(
                user_text
            )

                                             
                                     
            root.after(
                0,
                core.set_mode,
                result["mode"],
            )

            qwen_time = (
                time.perf_counter()
                - qwen_start
            )

            analysis = (
                result["analysis"]
            )

            execution_results = (
                result["results"]
            )

            answer = (
                result["answer"]
            )

            print()
            print(
                "[QWEN]"
            )

            print(
                analysis
            )

            print(
                f"[QWEN] Время: "
                f"{qwen_time:.2f} сек."
            )

            print()
            print(
                "[EXECUTOR]"
            )

            print(
                execution_results
            )

                                                               
                   
                                                               

            if tts is not None:
                root.after(
                    0,
                    set_state,
                    "speaking",
                    "ГОВОРЮ",
                )

                piper_start = (
                    time.perf_counter()
                )

                tts.synthesize(
                    answer,
                    VOICE_FILE,
                )

                piper_time = (
                    time.perf_counter()
                    - piper_start
                )

                print()
                print(
                    "[PIPER] Время: "
                    f"{piper_time:.2f} сек."
                )

                                                               
                              
                                                               

                player_start = (
                    time.perf_counter()
                )

                play_audio(
                    VOICE_FILE
                )

                player_time = (
                    time.perf_counter()
                    - player_start
                )

                print(
                    "[PLAYER] Время: "
                    f"{player_time:.2f} сек."
                )

            else:
                print()
                print(
                    "[PIPER] Голос "
                    "отключён."
                )

                                                               
                   
                                                               

            print()
            print(
                "[КАЙ]"
            )

            print(
                answer
            )

                                                               
                  
                                                               

            total_time = (
                time.perf_counter()
                - pipeline_start
            )

            print()
            print(
                "-" * 60
            )

            print(
                "[PIPELINE]"
            )

            print(
                f"Запись:      "
                f"{record_time:.2f} сек."
            )

            print(
                f"Whisper:     "
                f"{whisper_time:.2f} сек."
            )

            print(
                f"Qwen:        "
                f"{qwen_time:.2f} сек."
            )

            if tts is not None:
                print(
                    f"Piper:       "
                    f"{piper_time:.2f} сек."
                )

                print(
                    f"Воспроизв.:  "
                    f"{player_time:.2f} сек."
                )

            print(
                f"ИТОГО:       "
                f"{total_time:.2f} сек."
            )

            print(
                "-" * 60
            )

            print()

            root.after(
                0,
                finish_success,
            )

        except Exception as error:
            root.after(
                0,
                finish_error,
                str(error),
            )

        finally:
                                                           
                                      
                                                           

            if os.path.exists(
                AUDIO_FILE
            ):
                try:
                    os.remove(
                        AUDIO_FILE
                    )

                except OSError:
                    pass

                                                               
                              
                                                               

    def start_voice():
        thread = threading.Thread(
            target=process_voice,
            daemon=True,
        )

        thread.start()

                                                               
                  
                                                               

    def on_click(
        event=None,
    ):
        if core.current_state in (
            "listening",
            "processing",
            "speaking",
        ):
            return

        start_voice()

    canvas.bind(
        "<Button-1>",
        on_click,
    )

                                                               
                 
                                                               

    start_reminder_worker(
        root
    )

                                                               
              
                                                               

    def close_app():
        core.stop()

        root.destroy()

    root.protocol(
        "WM_DELETE_WINDOW",
        close_app,
    )

                                                               
            
                                                               

    print()
    print(
        "Кай готов."
    )

    print(
        "Кликни по окну и говори."
    )

    print()

    root.mainloop()


if __name__ == "__main__":
    main()