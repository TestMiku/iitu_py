from django import template

register = template.Library()


@register.filter
def to_dot(value: str):
    val = int(float(value))
    if val < 0:
        return 0
    return val

@register.filter
def index(indexable, i):
    return indexable[i]