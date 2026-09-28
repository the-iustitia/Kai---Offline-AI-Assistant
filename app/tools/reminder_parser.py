import re
from datetime import datetime, timedelta


NUMBER_WORDS = {
    "ноль": 0,
    "один": 1,
    "одну": 1,
    "одно": 1,
    "два": 2,
    "две": 2,
    "три": 3,
    "четыре": 4,
    "пять": 5,
    "шесть": 6,
    "семь": 7,
    "восемь": 8,
    "девять": 9,
    "десять": 10,
    "одиннадцать": 11,
    "двенадцать": 12,
    "тринадцать": 13,
    "четырнадцать": 14,
    "пятнадцать": 15,
    "шестнадцать": 16,
    "семнадцать": 17,
    "восемнадцать": 18,
    "девятнадцать": 19,
    "двадцать": 20,
}


def _number_from_text(value: str) -> int | None:
    value = value.strip().lower()

    if value.isdigit():
        return int(value)

    return NUMBER_WORDS.get(value)


def parse_reminder_time(value: str) -> datetime:
    text = value.lower().strip()

    now = datetime.now()

                   
     
              
                    
                       
                      

    match = re.search(
        r"через\s+([а-яё]+|\d+)\s+минут",
        text,
    )

    if match:
        minutes = _number_from_text(
            match.group(1)
        )

        if minutes is None:
            raise ValueError(
                "Не удалось определить количество минут."
            )

        return now + timedelta(
            minutes=minutes
        )

                   
     
              
                  
                    
                      

    match = re.search(
        r"через\s+([а-яё]+|\d+)\s+час",
        text,
    )

    if match:
        hours = _number_from_text(
            match.group(1)
        )

        if hours is None:
            raise ValueError(
                "Не удалось определить количество часов."
            )

        return now + timedelta(
            hours=hours
        )

                  
     
              
                 
                     
                     

    match = re.search(
        r"через\s+([а-яё]+|\d+)\s+дн",
        text,
    )

    if match:
        days = _number_from_text(
            match.group(1)
        )

        if days is None:
            raise ValueError(
                "Не удалось определить количество дней."
            )

        return now + timedelta(
            days=days
        )

                 
     
              
                    
                     
                         

    time_match = re.search(
        r"\b([01]?\d|2[0-3]):([0-5]\d)\b",
        text,
    )

    if not time_match:
        raise ValueError(
            "Не удалось определить время напоминания."
        )

    hour = int(
        time_match.group(1)
    )

    minute = int(
        time_match.group(2)
    )

                     

    if "послезавтра" in text:
        days_offset = 2

    elif "завтра" in text:
        days_offset = 1

    elif "сегодня" in text:
        days_offset = 0

    else:
        days_offset = 0

    result = now + timedelta(
        days=days_offset
    )

    result = result.replace(
        hour=hour,
        minute=minute,
        second=0,
        microsecond=0,
    )

                                
                                          

    if (
        days_offset == 0
        and result <= now
    ):
        result += timedelta(
            days=1
        )

    return result