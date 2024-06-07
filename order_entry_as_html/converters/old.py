import dataclasses
import io
import json
import mimetypes
from collections.abc import Iterator

import openpyxl

from avh_services.formatters import format_count, format_number
from .converter import Converter
from .data import Data
from .exceptions import ConvertError


@dataclasses.dataclass(slots=True)
class ExcelRow:
    nomenclature: str
    count: float
    entered_cost: float
    entered_count: float
    order_number: str
    order_specification: int


@dataclasses.dataclass(slots=True)
class ExcelData(Data):
    rows: list[ExcelRow]

    @property
    def json(self) -> str:
        return json.dumps(
            {
                "import_data": [
                    [
                        "Номер строки",
                        "Номенклатура",
                        "Количество (в счете)",
                        "Введённая цена",
                        "Налог",
                        "Строка счёта",
                        "Количество введённое",
                        "Заказ",
                        "Спецификация заказа",
                        "Итоговая сумма",
                    ],
                    *(
                        [
                            index * 10,
                            row.nomenclature,
                            row.count,
                            row.entered_count,
                            "Без налога",
                            index * 10,
                            row.entered_count,
                            row.order_number,
                            row.order_specification,
                            row.count * row.entered_cost,
                        ]
                        for index, row in enumerate(self.rows, 1)
                    ),
                ]
            },
            ensure_ascii=False,
        )

    def __iter__(
        self,
    ) -> Iterator[tuple[str, str, str, str, str, str, str, str, str, str]]:
        for index, row in enumerate(self.rows, 1):
            yield (
                index * 10,
                row.nomenclature,
                format_count(row.count),
                format_number(row.entered_cost),
                "Без налога",
                index * 10,
                format_count(row.entered_count),
                row.order_number,
                row.order_specification,
                format_number(row.count * row.entered_cost),
            )


class ExcelConverter(Converter):
    def to_data_list(
        self,
        bytes_io: io.BytesIO,
        /,
        **kwargs,
    ) -> list[Data]:
        workbook = openpyxl.load_workbook(bytes_io.read(), data_only=True)
        worksheet = workbook.active

        rows = []
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            try:
                if row[0] is None:
                    break
                rows.append(
                    ExcelRow(
                        nomenclature=row[1],
                        count=float(row[2]),
                        entered_cost=int(row[3]),
                        entered_count=float(row[6]),
                        order_number=row[7],
                        order_specification=int(row[8]),
                    )
                )
            except (KeyError, ValueError, TypeError) as error:
                raise ConvertError(f"Данные не верные: {error}")
        return [ExcelData(rows=rows)]


converters = {
    mimetypes.types_map[".xlsx"]: ExcelConverter(
        "order_entry_as_html/order_entry_template_old.html"
    )
}
