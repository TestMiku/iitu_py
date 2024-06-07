from django import template

register = template.Library()


@register.filter
def getvalue(dictinary, key):
    return dictinary[key]
