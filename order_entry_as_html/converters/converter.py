import abc
import dataclasses
import datetime
import io
import pathlib
import time
import uuid

from django.core.files.storage import default_storage, Storage
from django.core.files.uploadedfile import UploadedFile
from django.template.loader import get_template

from avh_services.constants import VAT
from avh_services.formatters import remove_spaces
from .data import Data
from .exceptions import ConvertError


@dataclasses.dataclass(slots=True)
class HTML:
    id: str
    title: str
    url: str
    path: pathlib.Path


@dataclasses.dataclass(slots=True)
class Converter(abc.ABC):
    template_name: str

    @abc.abstractmethod
    def to_data_list(self, bytes_io: io.BytesIO, /, **kwargs) -> list[Data]:
        pass

    def convert(
        self,
        bytes_io: io.BytesIO,
        /,
        *,
        output_path: pathlib.Path,
        uploaded_file: UploadedFile | None = None,
        filename: str | None = None,
        storage: Storage = default_storage,
        **kwargs,
    ) -> list[HTML]:
        assert uploaded_file is not None or filename is not None
        filename = uploaded_file.name if filename is None else filename
        template = get_template(self.template_name)
        htmls = []
        for data in self.to_data_list(
            bytes_io, uploaded_file=uploaded_file, filename=filename, **kwargs
        ):
            id_ = f"html-{uuid.uuid4()}"
            output_path_with_id = output_path / str(id_)
            absolute_output_path_with_id = pathlib.Path(
                storage.path(output_path_with_id)
            )
            absolute_output_path_with_id.mkdir(parents=True)
            name = pathlib.Path(filename).with_suffix(".html")
            html_file_absolute_path = absolute_output_path_with_id / name
            with open(html_file_absolute_path, "w", encoding="utf-8") as html_file:
                html_file.write(
                    template.render(
                        {
                            "vat": VAT,
                            "json": data.json,
                            "data": data,
                            "uploaded_file": uploaded_file,
                            **kwargs,
                        }
                    )
                )
            htmls.append(
                HTML(
                    title=filename,
                    path=html_file_absolute_path,
                    url=storage.url(output_path_with_id / name),
                    id=id_,
                )
            )
        return htmls

    @staticmethod
    def clear_htmls(
        path: pathlib.Path,
        /,
        *,
        timedelta: datetime.timedelta = datetime.timedelta(minutes=5),
        storage: Storage = default_storage,
    ) -> int:
        count = 0
        absolute_path = pathlib.Path(storage.path(path))
        for path in absolute_path.rglob("*.html"):
            if time.time() - path.stat().st_mtime >= timedelta.seconds:
                count += 1
                path.unlink()
        return count


def to_float(x: str, /) -> float:
    try:
        return float(remove_spaces(x).replace(",", "."))
    except ValueError:
        raise ConvertError("Данные не верные")


def to_date(x: str, /) -> datetime.date:
    try:
        return datetime.datetime.strptime(remove_spaces(x), "%d.%m.%Y").date()
    except ValueError:
        raise ConvertError("Данные не верные, дата не указано")
