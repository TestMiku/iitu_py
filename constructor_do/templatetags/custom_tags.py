from django import template

register = template.Library()

@register.filter
def add_one(value):
    try:
        return int(value) + 1
    except (TypeError, ValueError):
        return value