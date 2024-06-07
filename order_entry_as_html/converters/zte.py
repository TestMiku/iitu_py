import dataclasses
import io
import json
import mimetypes
import os
import pathlib
import tempfile
from collections.abc import Iterator

import openpyxl
import xlrd
from django.core.files.uploadedfile import UploadedFile

from .converter import Converter
from .data import Data
from .exceptions import ConvertError


@dataclasses.dataclass(slots=True)
class ExcelRow:
    number: int
    po_number: int
    purchasing_area: str
    construction_area: str
    site_code: str
    site_name: str
    logic_site_code: str
    logic_site_name: str
    item_code: int
    item_name: str
    unit: str
    po_quantity: float
    confirmed_quantity: float
    settlement_quantity: float
    line_settlement_status: str
    quantity_bill: float
    quantity_cancelled: float
    unit_price: int
    tax_rate: float
    pr_line_number: int
    description: str


@dataclasses.dataclass(slots=True)
class ExcelData(Data):
    rows: list[ExcelRow]
    order_specification: int
    order_number: str

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
                            row.number * 10,
                            "",
                            row.po_quantity,
                            row.unit_price,
                            "Без налога",
                            row.po_number * 10,
                            row.po_quantity,
                            self.order_number,
                            self.order_specification,
                            row.unit_price * row.po_quantity,
                        ]
                        for row in self.rows
                    ),
                ]
            },
            ensure_ascii=False,
            indent=4,
        )

    def __iter__(
        self,
    ) -> Iterator[
        tuple[
            str,
            str,
            str,
            str,
            str,
            str,
            str,
            str,
            int,
            str,
            str,
            str,
            str,
            str,
            str,
            str,
            str,
            int,
            str,
            int,
            str,
        ]
    ]:
        for row in self.rows:
            yield (
                str(row.number),
                str(row.po_number),
                row.purchasing_area,
                row.construction_area,
                row.site_code,
                row.site_name,
                row.logic_site_code,
                row.logic_site_name,
                str(row.item_code),
                row.item_name,
                row.unit,
                str(row.po_quantity),
                str(row.confirmed_quantity),
                str(row.settlement_quantity),
                row.line_settlement_status,
                str(row.quantity_bill),
                str(row.quantity_cancelled),
                str(row.unit_price),
                str(row.tax_rate),
                str(row.pr_line_number),
                str(row.description),
            )


class ExcelConverter(Converter):
    def to_data_list(
        self,
        bytes_io: io.BytesIO,
        /,
        *,
        uploaded_file: UploadedFile | None = None,
        **kwargs,
    ) -> list[Data]:
        assert uploaded_file is not None
        rows = []
        if uploaded_file.content_type == "application/vnd.ms-excel":
            fd, path = tempfile.mkstemp(".xls")
            with os.fdopen(fd, "wb") as file:
                file.write(bytes_io.read())
            workbook = xlrd.open_workbook(path)
            worksheet = workbook.sheet_by_index(0)
            for index in range(1, worksheet.nrows):
                row = worksheet.row(index)
                rows.append([cell.value for cell in row])
            os.remove(path)
        else:
            workbook = openpyxl.load_workbook(bytes_io)
            worksheet = workbook.active
            for row in worksheet.iter_rows(min_row=2):
                rows.append([cell.value for cell in row])

        result = []
        try:
            for row in rows:
                result.append(
                    ExcelRow(
                        int(row[0]),
                        int(row[1]),
                        row[2],
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        int(row[8]),
                        row[9],
                        row[10],
                        float(row[11]),
                        float(row[12]),
                        float(row[13]),
                        row[14],
                        float(row[15]),
                        float(row[16]),
                        int(row[17]),
                        float(row[18]),
                        int(row[22]),
                        row[23],
                    )
                )
        except (IndexError, ValueError, TypeError):
            raise ConvertError("Данные не верные")
        return [
            ExcelData(
                rows=result,
                order_number=pathlib.Path(uploaded_file.name).stem,
                order_specification=10,
            ),
        ]


excel_converter = ExcelConverter("order_entry_as_html/order_entry_template_zte.html")
converters = {
    mimetypes.types_map[".xlsx"]: excel_converter,
    mimetypes.types_map[".xls"]: excel_converter,
}
