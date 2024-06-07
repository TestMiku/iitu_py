from django import template

register = template.Library()

@register.filter
def to_float(value: str):
    val = str(value)
    if '-' in val:
        return 0
    return val