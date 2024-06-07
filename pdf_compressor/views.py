import datetime
import pathlib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import generic
from hurry.filesize import alternative, size

from reporter.models import Report

from . import services


class CompressFormView(LoginRequiredMixin, generic.TemplateView):
    template_name = "pdf_compressor/compress.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        files = request.FILES.getlist("files")
        archive = len(files) > 1
        percent = (100 - int(request.POST.get("percent", 50))) / 100
        start = datetime.datetime.now()
        output_path = pathlib.Path("p1/pdf_files")
        compressed_files: list[tuple[str, pathlib.Path]] = services.compress(
            files,
            percent=percent,
            output_path=output_path,
        )
        time = datetime.datetime.now() - start

        result = []
        for file, (url, compressed_file_path) in zip(files, compressed_files):
            result.append(
                {
                    "filename": file.name,
                    "sizeBefore": size(file.size, alternative),
                    "sizeAfter": size(compressed_file_path.stat().st_size, alternative),
                    "url": url,
                }
            )

        archive_url = None
        if archive:
            archive_url, _ = services.archive(
                [compressed_file_path for _, compressed_file_path in compressed_files],
                output_path=output_path,
            )
        Report.objects.create(responsible='', process="pdf_compressor - Обработано", text="pdf_compressor.handled")
        return JsonResponse(
            {
                "time": time.total_seconds(),
                "compressedFiles": result,
                "archive": archive_url,
            }
        )
