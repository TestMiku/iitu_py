import decimal

from django import template

register = template.Library()

@register.filter
def format_number(value: str | float | decimal.Decimal | int, arg: str | int = 0) -> str:
    value = value or 0
    value = float("".join(value.split()).replace(",", ".") if isinstance(value, str) else value)
    return f"{value:,.{int(arg)}f}".replace(",", " ").replace(".", ",")


@register.filter
def format_percent(value: str | float | decimal.Decimal | int) -> str:
    value = value or 0
    value = float("".join(value.split()).replace(",", ".") if isinstance(value, str) else value)
    return f"{value:,.2f}".replace(",", " ").replace(".", ",") + "%"
