from datetime import datetime

import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from avh_modules.services import TransformXLSXFileService


class TransformXLSXFileView(generic.ListView):
    template_name = 'avh_modules/transform_xlsx_file.html'
    context_object_name = 'transform_xlsx_file'
    transform_service = TransformXLSXFileService

    def get_queryset(self):
        return None

    def post(self, request, *args, **kwargs):
        xlsx_file = request.FILES.get('xlsx_file')
        if not xlsx_file:
            return self.transform_service.get_error(request, self.template_name, 'Загрузите файл')
        if not xlsx_file.name.endswith('.xlsx'):
            return self.transform_service.get_error(request, self.template_name, 'Файл должен быть в формате .xlsx')

        service = self.transform_service(xlsx_file)
        service.transform(request, self.template_name)
        return service.get_response()
