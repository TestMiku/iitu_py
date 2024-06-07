from django import template

register = template.Library()

@register.filter(name='spaceseparator')
def spaceseparator(value):
    return '{:,}'.format(value).replace(',', ' ')
