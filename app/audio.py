import time
import wave

import numpy as np
import sounddevice as sd


SAMPLE_RATE = 16000
CHANNELS = 1

MAX_RECORD_SECONDS = 8.0

SILENCE_SECONDS = 0.8

SILENCE_THRESHOLD = 450

START_TIMEOUT = 3.0


def get_input_device():
    device = sd.query_devices(
        kind="input"
    )

    print(
        "Используется микрофон:",
        device["name"],
    )

    return device["index"]


def _calculate_rms(data) -> float:
    samples = data.astype(
        np.float32
    )

    if len(samples) == 0:
        return 0.0

    return float(
        np.sqrt(
            np.mean(
                samples ** 2
            )
        )
    )


def record_audio(
    file_path: str,
    max_seconds: float = MAX_RECORD_SECONDS,
):
    device = get_input_device()

    print(
        "Говори..."
    )

    block_duration = 0.05

    block_size = int(
        SAMPLE_RATE
        * block_duration
    )

    chunks = []

    speech_started = False

    silence_time = 0.0

    start_time = time.perf_counter()

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16",
        blocksize=block_size,
        device=device,
    ) as stream:

        while True:
            data, overflowed = (
                stream.read(
                    block_size
                )
            )

            if overflowed:
                print(
                    "[AUDIO] "
                    "Предупреждение: "
                    "переполнение буфера."
                )

            data = data.copy()

            chunks.append(data)

            rms = _calculate_rms(
                data
            )

            if rms >= SILENCE_THRESHOLD:
                speech_started = True
                silence_time = 0.0

            elif speech_started:
                silence_time += (
                    block_duration
                )

            elapsed = (
                time.perf_counter()
                - start_time
            )

                                          
                                     

            if (
                speech_started
                and silence_time
                >= SILENCE_SECONDS
            ):
                break

                                 
                                       
                               

            if (
                not speech_started
                and elapsed
                >= START_TIMEOUT
            ):
                break

                               

            if elapsed >= max_seconds:
                break

    if not chunks:
        raise RuntimeError(
            "Не удалось записать аудио."
        )

    audio = np.concatenate(
        chunks,
        axis=0,
    )

                            
                           

    audio = audio[:]

    with wave.open(
        file_path,
        "wb",
    ) as wav_file:

        wav_file.setnchannels(
            CHANNELS
        )

        wav_file.setsampwidth(
            2
        )

        wav_file.setframerate(
            SAMPLE_RATE
        )

        wav_file.writeframes(
            audio.tobytes()
        )

    duration = (
        len(audio)
        / SAMPLE_RATE
    )

    print(
        f"[AUDIO] Записано: "
        f"{duration:.2f} сек."
    )

    return duration