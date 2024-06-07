from django import template

register = template.Library()


@register.filter(name='index')
def index(sequence, position):
    try:
        return sequence[position]
    except (IndexError, TypeError):
        return ''


@register.filter(name='format_number')
def format_number(value):
    try:
        value = float(value)
        return f'{value:,.2f}'.replace(',', ' ').replace('.', ',')
    except (ValueError, TypeError):
        return value


@register.filter
def split(value, delimiter=' '):
    return value.split(delimiter)[0]
