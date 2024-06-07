from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return round((float(value) * float(arg)), 2)
