import ast

import django.db.models
from django.http import JsonResponse
import rest_framework.viewsets
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from . import mixins, models, serializers
from .models import get_report_count_by_process


@method_decorator(csrf_exempt, name="dispatch")
class ReportViewSet(
    rest_framework.viewsets.GenericViewSet,
    rest_framework.viewsets.mixins.CreateModelMixin,
):
    serializer_class = serializers.ReportSerializer
    queryset = models.Report.objects.values("process").distinct()


class ReportListView(mixins.SortMixin, generic.ListView):
    template_name = "p1/reporter/list.html"
    paginate_by = 30

    def get_sort_field_names(self) -> set[str]:
        return {"id", "process", "created_at", "responsible", "text"}

    def get_query_parameters(self) -> dict[str, str]:
        return self.request.GET

    def get_model_class(self) -> type[django.db.models.Model]:
        return models.Report

    def get_queryset(self):
        return self.get_sorted_queryset()

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs) | self.get_sort_mixin_context_data()


def chart_page(request):
    return render(
        request, "p1/reporter/chart.html", {"data": get_report_count_by_process()}
    )


@api_view(["GET"])
def search_by_process(request: Request) -> Response:
    acc_num = request.GET.get("process")
    res = ast.literal_eval(acc_num)
    print(res)
    filters: dict[str, str] = {}
    if acc_num:
        filters["process__in"] = res
        data = models.Report.objects.filter(**filters).values("process", "created_at")
        return Response(serializers.processSerializer(data, many=True).data)
    return Response({})


@csrf_exempt
def powerbi(request):   
    data = models.Report.objects.all()
    return JsonResponse({"results" : list(data.values())}, status=200)