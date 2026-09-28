from difflib import SequenceMatcher

from .command_log import (
    get_commands,
    normalize_text,
)


MATCH_THRESHOLD = 0.86


def _text_similarity(
    first: str,
    second: str,
) -> float:
    first = normalize_text(
        first
    )

    second = normalize_text(
        second
    )

    if not first or not second:
        return 0.0

    if first == second:
        return 1.0

    sequence_score = (
        SequenceMatcher(
            None,
            first,
            second,
        ).ratio()
    )

    first_words = set(
        first.split()
    )

    second_words = set(
        second.split()
    )

    if not first_words or not second_words:
        return sequence_score

    intersection = (
        first_words
        & second_words
    )

    union = (
        first_words
        | second_words
    )

    word_score = (
        len(intersection)
        / len(union)
    )

    return (
        sequence_score * 0.65
        + word_score * 0.35
    )


def find_known_command(
    user_text: str,
) -> dict | None:
    commands = get_commands()

    if not commands:
        return None

    best_command = None
    best_score = 0.0

    for command in commands:
        score = _text_similarity(
            user_text,
            command["command_text"],
        )

        if score > best_score:
            best_score = score
            best_command = command

    if (
        best_command is None
        or best_score < MATCH_THRESHOLD
    ):
        return None

    action = dict(
        best_command["action_data"]
    )

    return {
        "action": action,
        "score": best_score,
        "matched_text": (
            best_command[
                "command_text"
            ]
        ),
        "use_count": (
            best_command[
                "use_count"
            ]
        ),
    }