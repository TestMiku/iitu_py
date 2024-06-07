import collections.abc

from . import tele2, kar_tel, zte, kcell, old
from .converter import Converter

_converters: collections.abc.Mapping[str, collections.abc.Mapping[str, Converter]] = {
    "ЗТЕ": zte.converters,
    "Теле2": tele2.converters,
    "Кселл": kcell.converters,
    "КаР-Тел": kar_tel.converters,
    "Старые": old.converters,
}


def get_converter(project: str, content_type: str) -> Converter | None:
    if project not in _converters or content_type not in _converters[project]:
        return None
    return _converters[project][content_type]


def supported_projects() -> list[str]:
    return list(_converters)
