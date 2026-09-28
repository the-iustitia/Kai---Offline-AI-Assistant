import ollama

from .router import route_command, execute_command


MODEL = "qwen2.5:3b"


def ask_ai(user_text: str) -> str:
    command = route_command(user_text)

                                                
                           
                                                

    if command["action"] != "chat":
        result = execute_command(command)

        messages = [
            {
                "role": "system",
                "content": (
                    "Ты Кай — персональный AI-ассистент. "
                    "Всегда отвечай на русском языке. "
                    "Пользователь попросил выполнить действие. "
                    "Действие уже было выполнено Python. "
                    "Твоя задача — только естественно сообщить "
                    "результат пользователю. "
                    "Не утверждай, что сделал что-либо ещё. "
                    "Не добавляй несуществующие действия. "
                    "Отвечай кратко и естественно."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Запрос пользователя:\n"
                    f"{user_text}\n\n"
                    f"Результат выполнения:\n"
                    f"{result}"
                ),
            },
        ]

        response = ollama.chat(
            model=MODEL,
            messages=messages,
        )

        return response.message.content

                                                
                    
                                                

    messages = [
        {
            "role": "system",
            "content": (
                "Ты Кай — персональный AI-ассистент пользователя. "
                "Всегда отвечай на русском языке. "
                "Поддерживай естественный дружеский разговор. "
                "Понимай разговорную речь, сленг и неполные фразы. "
                "Отвечай кратко, естественно и по делу. "
                "Не утверждай, что выполнял системные действия, "
                "если Python их не выполнял."
            ),
        },
        {
            "role": "user",
            "content": user_text,
        },
    ]

    response = ollama.chat(
        model=MODEL,
        messages=messages,
    )

    return response.message.content