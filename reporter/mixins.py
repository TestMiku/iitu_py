import abc
import re
from collections import OrderedDict
from functools import cache
from typing import TypedDict

import django.db.models


class SortField(TypedDict):
    verbose_name: str
    as_query_parameter: str
    order: str | None


class SortMixin(abc.ABC):
    @abc.abstractmethod
    def get_sort_field_names(self) -> set[str]:
        pass

    @abc.abstractmethod
    def get_query_parameters(self) -> dict[str, str]:
        pass

    @abc.abstractmethod
    def get_model_class(self) -> type[django.db.models.Model]:
        pass

    @cache
    def _get_sort_fields(self) -> tuple[OrderedDict[str, SortField], OrderedDict[str, SortField]]:
        selected_sort_fields = OrderedDict()
        query_parameters = self.get_query_parameters()
        model_class = self.get_model_class()
        for query_parameter in query_parameters:
            if match := re.match(r"sort-(?P<field>[a-z][-a-z0-9]+)", query_parameter):
                field = match.group("field").replace("-", "_")
                if field not in self.get_sort_field_names():
                    continue

                selected_sort_fields[field] = {
                    "verbose_name": model_class._meta.get_field(field).verbose_name,
                    "as_query_parameter": query_parameter,
                    "order": query_parameters[query_parameter]
                }

        non_selected_sort_fields = OrderedDict()
        for field in self.get_sort_field_names() - set(selected_sort_fields):
            non_selected_sort_fields[field] = {
                "verbose_name": model_class._meta.get_field(field).verbose_name,
                "as_query_parameter": "sort-" + field.replace("_", "-"),
                "order": None
            }
        return selected_sort_fields, non_selected_sort_fields

    @cache
    def get_selected_sort_fields(self) -> OrderedDict[str, SortField]:
        return self._get_sort_fields()[0]

    @cache
    def get_non_selected_sort_fields(self) -> OrderedDict[str, SortField]:
        return self._get_sort_fields()[1]

    @cache
    def get_selected_sort_fields_for_order_by(self) -> list[str]:
        return [("-" if value["order"] == "desc" else "") + key for key, value in
                self.get_selected_sort_fields().items()]

    def get_sorted_queryset(self):
        return self.get_model_class().objects.order_by(*self.get_selected_sort_fields_for_order_by())

    def get_sort_mixin_context_data(self) -> dict:
        selected_sort_fields = self.get_selected_sort_fields()
        return {
            "selected_sort_fields": selected_sort_fields,
            "non_selected_sort_fields": self.get_non_selected_sort_fields(),
            "selected_sort_fields_as_query_parameters": "&".join(
                f'{value["as_query_parameter"]}={value["order"]}' for value in selected_sort_fields.values())
        }
