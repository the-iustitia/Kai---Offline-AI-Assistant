import time
import wave
from pathlib import Path

from piper import PiperVoice


MODEL_PATH = Path(
    "data/piper/ru_RU-irina-medium.onnx"
)

OUTPUT_FILE = Path(
    "data/kai_voice.wav"
)


class KaiTTS:
    def __init__(
        self,
        model_path: Path = MODEL_PATH,
    ):
        self.model_path = Path(
            model_path
        )

        if not self.model_path.exists():
            raise FileNotFoundError(
                "Piper-модель не найдена:\n"
                f"{self.model_path}"
            )

        print(
            "[PIPER] Загружаю голос..."
        )

        start = time.perf_counter()

        self.voice = PiperVoice.load(
            self.model_path
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        print(
            "[PIPER] Голос загружен: "
            f"{elapsed:.2f} сек."
        )

    def synthesize(
        self,
        text: str,
        output_file: Path = OUTPUT_FILE,
    ):
        text = text.strip()

        if not text:
            return 0.0

        output_file = Path(
            output_file
        )

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        start = time.perf_counter()

        with wave.open(
            str(output_file),
            "wb",
        ) as wav_file:

            self.voice.synthesize_wav(
                text,
                wav_file,
            )

        elapsed = (
            time.perf_counter()
            - start
        )

        print(
            "[PIPER] Синтез: "
            f"{elapsed:.2f} сек."
        )

        return elapsed