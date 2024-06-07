import functools
from django import template
from django.db.models import Model

from .. import models

register = template.Library()


@register.simple_tag
def get_table_cell_color(key: str, default: str | None = None) -> str | None:
    try:
        table_cell_color = models.TableCellColor.objects.get(key=key)
    except models.TableCellColor.DoesNotExist:
        return default
    else:
        return table_cell_color.color


@register.simple_tag
def get_table_cell_color_from_instance_attr(category: str, instance: Model | None, attr: str, default: str | None = None) -> str | None:
    if instance is None:
        return default
    key = f"{category}.{getattr(instance, attr)}"
    try:
        table_cell_color = models.TableCellColor.objects.get(key=key)
    except models.TableCellColor.DoesNotExist:
        return default
    else:
        return table_cell_color.color