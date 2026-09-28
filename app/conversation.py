from .agent import (
    FAST_MODEL,
    SMART_MODEL,
    analyze_command,
    generate_response,
)

from .executor import (
    execute_actions,
)

from .command_log import (
    log_command,
)

from .command_router import (
    find_known_command,
)


MAX_HISTORY_MESSAGES = 20


FAST_MODE = "fast"
SMART_MODE = "smart"


SMART_COMMANDS = (
    "задумайся",
    "подумай",
    "включи продвинутый режим",
    "включи умный режим",
    "умный режим",
    "продвинутый режим",
    "включи умную модель",
)


FAST_COMMANDS = (
    "обычный режим",
    "быстрый режим",
    "включи обычный режим",
    "включи быстрый режим",
    "выключи продвинутый режим",
    "выключи умный режим",
)


class Conversation:
    def __init__(self):
        self.messages = []

        self.mode = FAST_MODE

    def add_user_message(
        self,
        text: str,
    ):
        self.messages.append(
            {
                "role": "user",
                "content": text,
            }
        )

    def add_assistant_message(
        self,
        text: str,
    ):
        self.messages.append(
            {
                "role": "assistant",
                "content": text,
            }
        )

    def get_context(self) -> list[dict]:
        return self.messages[
            -MAX_HISTORY_MESSAGES:
        ]

    def _normalize_command(
        self,
        text: str,
    ) -> str:
        text = text.lower().strip()

                                                       
                                             
         
                   
         
                                   
         
                         
         
                                  
                                                       

        replacements = (
            (
                "в ключи",
                "включи",
            ),
            (
                "в ключ",
                "включи",
            ),
            (
                "включи",
                "включи",
            ),
        )

        for old, new in replacements:
            text = text.replace(
                old,
                new,
            )

                                                       
                                  
         
                                  
           
                              
                                                       

        if text.startswith("кай "):
            text = text[4:]

        elif text == "кай":
            text = ""

                                                       
                                   
                                                       

        text = (
            text
            .replace(",", " ")
            .replace(".", " ")
            .replace("!", " ")
            .replace("?", " ")
        )

                                                       
                                 
                                                       

        return " ".join(
            text.split()
        )

    def _check_mode_command(
        self,
        user_text: str,
    ) -> str | None:

        text = self._normalize_command(
            user_text
        )

                                                       
                    
                                                       

        for command in SMART_COMMANDS:
            if (
                text == command
                or text.startswith(
                    command + " "
                )
            ):
                self.mode = SMART_MODE

                return (
                    "Продвинутый режим включён."
                )

                                                       
                   
                                                       

        for command in FAST_COMMANDS:
            if (
                text == command
                or text.startswith(
                    command + " "
                )
            ):
                self.mode = FAST_MODE

                return (
                    "Обычный режим включён."
                )

        return None

    def _current_model(self) -> str:
        if self.mode == SMART_MODE:
            return SMART_MODEL

        return FAST_MODEL

    def _execute_known_command(
        self,
        user_text: str,
    ) -> dict | None:

        match = find_known_command(
            user_text
        )

        if match is None:
            return None

        action = match[
            "action"
        ]

        results = execute_actions(
            action,
            self.get_context(),
        )

        answer = (
            results[0]
            if results
            else "Готово."
        )

        print()
        print(
            "[ROUTER]"
        )

        print(
            "Известная команда."
        )

        print(
            f"Совпадение: "
            f"{match['score']:.2f}"
        )

        print(
            f"Шаблон: "
            f"{match['matched_text']}"
        )

        print(
            f"Использований: "
            f"{match['use_count']}"
        )

        print(
            f"Действие: "
            f"{action}"
        )

        return {
            "analysis": action,
            "results": results,
            "answer": answer,
            "source": "router",
        }

    def process(
        self,
        user_text: str,
    ) -> dict:

                                                       
                                                
                 
         
                                
                                                       

        mode_answer = (
            self._check_mode_command(
                user_text
            )
        )

        if mode_answer is not None:

            print()
            print(
                "[MODE]"
            )

            print(
                f"Режим: {self.mode}"
            )

            print(
                f"Модель: "
                f"{self._current_model()}"
            )

            self.add_user_message(
                user_text
            )

            self.add_assistant_message(
                mode_answer
            )

            return {
                "analysis": {
                    "action": "chat"
                },
                "results": [
                    mode_answer
                ],
                "answer": mode_answer,
                "source": "mode",
                "mode": self.mode,
                "model": self._current_model(),
            }

                                                       
                         
                                                       

        self.add_user_message(
            user_text
        )

                                                       
                                      
                                                       

        known_command = (
            self._execute_known_command(
                user_text
            )
        )

        if known_command is not None:

            known_command["mode"] = (
                self.mode
            )

            known_command["model"] = (
                self._current_model()
            )

            self.add_assistant_message(
                known_command["answer"]
            )

            return known_command

                                                       
                                  
                                                       

        context = self.get_context()

        model = self._current_model()

        print()
        print(
            "[MODEL ROUTER]"
        )

        print(
            f"Режим: {self.mode}"
        )

        print(
            f"Модель: {model}"
        )

        analysis = analyze_command(
            context,
            model=model,
        )

        execution_results = (
            execute_actions(
                analysis,
                context,
            )
        )

        answer = generate_response(
            context,
            user_text,
            execution_results,
            model=model,
        )

                                                       
                                        
                                                       

        actions = analysis.get(
            "actions"
        )

        if actions is None:
            actions = [
                analysis
            ]

        for action in actions:
            log_command(
                user_text,
                action,
            )

        self.add_assistant_message(
            answer
        )

        return {
            "analysis": analysis,
            "results": execution_results,
            "answer": answer,
            "source": "llm",
            "mode": self.mode,
            "model": model,
        }