import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from client import ask_ai
from transcriber import transcribe_audio


load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.voice)
async def handle_voice(message: Message):
    print("Получил голосовое!")

    file = await bot.get_file(message.voice.file_id)

    audio_path = f"data/voice_{message.message_id}.ogg"

    await bot.download_file(file.file_path, audio_path)

    print("Файл скачан:", audio_path)

    text = transcribe_audio(audio_path)

    print("Распознано:", text)

    os.remove(audio_path)

    print("Временный аудиофайл удалён:", audio_path)

    answer = ask_ai(text)

    await message.answer(answer)


@dp.message()
async def handle_message(message: Message):
    if not message.text:
        return

    answer = ask_ai(message.text)

    await message.answer(answer)


async def main():
    print("Кай запускается...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
