import collections.abc
import functools
import json
import typing

import django.db.models
import rest_framework.serializers
from django.db.models import Count, DateField, DateTimeField, Q, QuerySet, Sum
from django.db.models.functions import Cast, TruncDate
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import URLPattern, path, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


class FieldValues(typing.TypedDict):
    field: str
    exclude: list[typing.Any]
    include: list[typing.Any]


class FieldSort(typing.TypedDict):
    sort: typing.Literal["asc", "desc"]
    field: str


def filter_queryset(
    queryset: QuerySet,
    /,
    *,
    field_values_list: list[FieldValues],
    field: str | None = None,
    field_new_field: dict[str, str] | None = None,
) -> QuerySet:
    for field_values in field_values_list:
        if field is not None and field_values["field"] == field:
            break
        method, type_ = (
            (QuerySet.exclude, "exclude")
            if field_values["exclude"]
            else (QuerySet.filter, "include")
        )
        filter_ = Q(
            **{
                f"{get_field(field_values['field'], field_new_field)}__in": filter(
                    None, field_values[type_]
                )
            }
        )
        if "" in field_values[type_]:
            filter_ = filter_ | Q(
                **{f"{get_field(field_values['field'], field_new_field)}__isnull": True}
            )
        queryset = method(queryset, filter_)
    return queryset


def annotate_queryset_field_with_new_type(
    queryset: QuerySet, /, *, field: str, type: str | None
) -> tuple[QuerySet, str]:
    new_field = field
    if type == "date":
        new_field = f"{field}_date"
        queryset = queryset.annotate(**{new_field: Cast(field, DateField())})
    return queryset, new_field


def convert_queryset(
    queryset: QuerySet, /, *, field_type: dict[str, str]
) -> tuple[QuerySet, dict[str, str]]:
    field_new_field = {}
    for field, type in field_type.items():
        queryset, new_field = annotate_queryset_field_with_new_type(
            queryset, field=field, type=type
        )
        field_new_field[field] = new_field
    return queryset, field_new_field


def get_field(field: str, field_new_field: dict[str, str] | None) -> str:
    return field_new_field.get(field, field) if field_new_field else field


def order_queryset(
    queryset: QuerySet,
    /,
    *,
    order: list[FieldSort] | None = None,
    field_new_field: dict[str, str] | None = None,
) -> QuerySet:
    if order:
        order.append({"field": "pk", "sort": "desc"})
        queryset = queryset.order_by(
            *(
                (
                    get_field(fieldSort["field"], field_new_field)
                    if fieldSort["sort"] == "asc"
                    else "-" + get_field(fieldSort["field"], field_new_field)
                )
                for fieldSort in order
            )
        )
    return queryset


def smart_table_get_values(
    model: type[django.db.models.Model],
) -> collections.abc.Callable[
    [collections.abc.Callable[[HttpRequest, QuerySet], QuerySet]],
    collections.abc.Callable[[HttpRequest], HttpResponse],
]:
    def decorator(
        function: collections.abc.Callable[
            [HttpRequest, QuerySet, str | None], QuerySet
        ],
    ) -> collections.abc.Callable[[HttpRequest], HttpResponse]:
        @csrf_exempt
        @require_POST
        @functools.wraps(function)
        def api_get_values(request: HttpRequest) -> JsonResponse:
            data = json.loads(request.body)
            field = data["field"]
            field_type = data["fieldType"]
            field_values_list = data["fieldValuesList"]
            queryset = function(request, model.objects.all(), field)
            queryset, field_new_field = convert_queryset(
                queryset, field_type=field_type
            )
            queryset = filter_queryset(
                queryset,
                field_values_list=field_values_list,
                field=field,
                field_new_field=field_new_field,
            )
            return JsonResponse(
                {
                    "values": list(
                        queryset.values_list(
                            field_new_field[field], flat=True
                        ).distinct()
                    )
                }
            )

        return api_get_values

    return decorator


def smart_table_get_rows(
    model: type[django.db.models.Model],
    serializer: type[rest_framework.serializers.Serializer],
) -> collections.abc.Callable[
    [collections.abc.Callable[[HttpRequest, QuerySet, str | None], QuerySet]],
    collections.abc.Callable[[HttpRequest], HttpResponse],
]:
    def decorator(
        function: collections.abc.Callable[
            [HttpRequest, QuerySet, str | None], QuerySet
        ],
    ) -> collections.abc.Callable[[HttpRequest], HttpResponse]:
        @csrf_exempt
        @functools.wraps(function)
        @require_POST
        def wrapper(request: HttpRequest) -> JsonResponse:
            data = json.loads(request.body)
            field_values_list = data["fieldValuesList"]
            field_type = data["fieldType"]
            order = data["order"]
            queryset = model.objects.all()
            queryset = function(request, queryset, None)
            queryset, field_new_field = convert_queryset(
                queryset, field_type=field_type
            )
            queryset = filter_queryset(
                queryset,
                field_values_list=field_values_list,
                field_new_field=field_new_field,
            )
            queryset = order_queryset(
                queryset, order=order, field_new_field=field_new_field
            )
            page = int(request.GET.get("page", 0))
            limit = int(request.GET.get("limit", 30))

            next_ = None
            count = queryset.count()
            if page * limit < count:
                queryset = queryset[page * limit : page * limit + limit]
                if (page + 1) * limit < count:
                    next_ = (
                        f"{reverse(request.resolver_match.view_name)}?page={page + 1}"
                    )
            else:
                queryset = None
            return JsonResponse(
                {
                    "rows": serializer(queryset, many=True).data,
                    "next": next_,
                }
            )

        return wrapper

    return decorator


def smart_table_get_subtotals(
    model: type[django.db.models.Model],
) -> collections.abc.Callable[
    [collections.abc.Callable[[HttpRequest, QuerySet, str | None], QuerySet]],
    collections.abc.Callable[[HttpRequest], HttpResponse],
]:
    def decorator(
        function: collections.abc.Callable[
            [HttpRequest, QuerySet, str | None], QuerySet
        ],
    ) -> collections.abc.Callable[[HttpRequest], HttpResponse]:
        @csrf_exempt
        @require_POST
        @functools.wraps(function)
        def api_get_subtotals(request: HttpRequest) -> JsonResponse:
            data = json.loads(request.body)
            field_values_list = data["fieldValuesList"]
            field_subtotal = data["fieldSubtotal"]
            field_type = data["fieldType"]
            queryset = model.objects.all()
            queryset = function(request, queryset, None)
            queryset, field_new_field = convert_queryset(
                queryset, field_type=field_type
            )
            queryset = filter_queryset(
                queryset,
                field_values_list=field_values_list,
                field_new_field=field_new_field,
            )
            field_result = {}
            for field, subtotal in field_subtotal.items():
                if subtotal == 2:
                    field_result[field] = queryset.aggregate(
                        Count(field_new_field[field])
                    )[f"{field_new_field[field]}__count"]
                elif subtotal == 9:
                    field_result[field] = queryset.aggregate(
                        Sum(field_new_field[field])
                    )[f"{field_new_field[field]}__sum"]
                else:
                    field_result[field] = 0
            return JsonResponse({"fieldResult": field_result})

        return api_get_subtotals

    return decorator


def smart_table(
    prefix: str,
    model: type[django.db.models.Model],
    serializer: type[rest_framework.serializers.Serializer],
) -> collections.abc.Callable[
    [collections.abc.Callable[[HttpRequest, QuerySet, str | None], QuerySet]],
    collections.abc.Callable[[HttpRequest], HttpResponse],
]:
    def decorator(
        function: collections.abc.Callable[
            [HttpRequest, QuerySet, str | None], QuerySet
        ],
    ) -> list[URLPattern]:
        return [
            path(
                f"{prefix}-get-values",
                smart_table_get_values(model)(function),
                name=f"{prefix}_get_values",
            ),
            path(
                f"{prefix}-get-rows",
                smart_table_get_rows(model, serializer)(function),
                name=f"{prefix}_get_rows",
            ),
            path(
                f"{prefix}-get-subtotals",
                smart_table_get_subtotals(model)(function),
                name=f"{prefix}_get_subtotals",
            ),
        ]

    return decorator
