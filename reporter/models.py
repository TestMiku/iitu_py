from django.db import models
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.translation import gettext_lazy as _

from main.models import AvhObject


class Report(AvhObject):
    text = models.TextField(_("Дополнительно"))
    process = models.CharField(_("Имя процесса"), max_length=256)
    responsible = models.CharField(_("Ответственный"), max_length=128)


def get_report_count_by_process():
    # Получаем QuerySet с уникальными значениями process и их количеством
    process_counts = Report.objects.values("process").annotate(count=Count("process"))

    # Преобразуем QuerySet в словарь, где ключ - это process, а значение - количество
    process_count_dict = {item["process"]: item["count"] for item in process_counts}

    return process_count_dict


# def get_report_count_by_process():
#     # Получаем QuerySet с уникальными значениями process, created_at и их количеством
#     process_counts = Report.objects.annotate(
#         truncated_date=TruncDate('created_at')
#     ).values('process', 'truncated_date').annotate(
#         count=Count('id')
#     )

#     # Преобразуем QuerySet в словарь, где ключ - это (process, truncated_date), а значение - количество
#     process_count_dict = {(item['process'], item['truncated_date']): item['count'] for item in process_counts}

#     return process_count_dict
