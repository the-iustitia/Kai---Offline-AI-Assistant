from faster_whisper import WhisperModel


MODEL_SIZE = "medium"

model = WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8",
)


def transcribe_audio(
    file_path: str,
) -> str:
    segments, info = model.transcribe(
        file_path,
        language="ru",
        beam_size=1,
        vad_filter=True,
    )

    text = " ".join(
        segment.text.strip()
        for segment in segments
    )

    return text.strip()