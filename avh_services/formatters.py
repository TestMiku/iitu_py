import datetime
from itertools import filterfalse

from num2words import num2words


def remove_spaces(x: str, /) -> str:
    return "".join(filterfalse(str.isspace, x))


def format_number(x: float, /) -> str:
    return f"{x:,.2f}".replace(",", " ")


def format_number_as_words(x: float, /) -> str:
    formatted = format_number(x)
    integer_part, fractional_part = formatted.split(".")
    return f"{formatted} ( {num2words(integer_part.replace(' ', ''), lang='ru')} ) тенге и {fractional_part} тиын"


def format_count(x: float | str, /) -> str:
    return (
        format_count(float(x))
        if isinstance(x, str)
        else str(int(x) if x.is_integer() else x)
    )


def format_date(date: datetime.date | None) -> str:
    return "" if date is None else date.strftime("%Y-%m-%d")
