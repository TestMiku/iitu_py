import io
import json
import logging
import pathlib
import uuid

from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpRequest, JsonResponse, FileResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from . import forms
from .converters import get_converter, Converter
from .converters.exceptions import ConvertError
from reporter.models import Report

class OrderEntryFormView(generic.FormView):
    form_class = forms.OrderEntryForm
    template_name = "order_entry_as_html/form.html"

    def form_valid(self, form: forms.OrderEntryForm) -> HttpResponse:
        path = pathlib.Path("p1/order_entry_as_html")
        logging.info(f"Очистка html файлов в {path}: {Converter.clear_htmls(path)}")
        htmls = []

        for uploaded_file in form.files.getlist("files"):
            try:
                region = form.cleaned_data.get("region")
                contract_date = form.cleaned_data.get("contract_date")
                converter = get_converter(
                    form.cleaned_data["project"], uploaded_file.content_type
                )
                if converter is None:
                    form.add_error(
                        None,
                        f"Такой тип файлов не поддерживается: {uploaded_file.name}",
                    )
                else:
                    htmls.extend(
                        converter.convert(
                            uploaded_file.file,
                            uploaded_file=uploaded_file,
                            output_path=path,
                            region=region,
                            contract_date=contract_date,
                        )
                    )
            except ConvertError as error:
                form.add_error(
                    None,
                    f"Ошибка при конвертаций файла {uploaded_file.name}: {error}",
                )
        self.extra_context = {"htmls": htmls, "form": form}
        return self.get(self.request)


@require_POST
@csrf_exempt
def convert_kar_tel_html(request: HttpRequest) -> JsonResponse | FileResponse:
    data = json.loads(request.body)
    html = data.get("html")
    index = int(data.get("index"))
    if index < 0:
        return JsonResponse(
            {"detail": "Индекс не может быть отрицательным"}, status=400
        )

    filename = data.get("filename") or str(uuid.uuid4())

    if not html:
        return JsonResponse({"detail": "Укажите HTML"}, status=400)
    converter = get_converter("КаР-Тел", "text/html")
    bytes_io = io.BytesIO(html.encode())
    try:
        htmls = converter.convert(
            bytes_io,
            storage=default_storage,
            filename=filename,
            output_path=pathlib.Path("p1/order_entry_as_html"),
        )
    except ConvertError as error:
        return JsonResponse({"detail": str(error)}, status=400)
    if index >= len(htmls):
        return JsonResponse(
            {
                "detail": f"Таблиц только {len(htmls)}, выберете таблицу в диапазоне [0, {len(htmls)})"
            },
            status=400,
        )
    return FileResponse(htmls[index].path.open("rb"))
