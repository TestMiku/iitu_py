import abc
import dataclasses
import datetime
import io
import json
import mimetypes
import re
from collections.abc import Iterator

import bs4
import pdfplumber

from avh_services.formatters import (
    format_count,
    format_date,
    format_number,
    remove_spaces,
)
from avh_services.keys import tcp_key

from .converter import Converter, to_date, to_float
from .data import Data, TotalMixin
from .exceptions import ConvertError


@dataclasses.dataclass
class DataRow:
    tcp: str
    name: str
    type: str | None
    measuring_unit: str
    count: float
    work_cost: float
    completion_date: datetime.date | str


@dataclasses.dataclass
class GeneralData(Data, TotalMixin, abc.ABC):
    rows: list[DataRow]

    @property
    def total(self) -> float:
        return sum(row.work_cost for row in self.rows)

    def __iter__(self) -> Iterator[tuple[int, str, str, str, str, str]]:
        for index, row in enumerate(sorted(self.rows, key=lambda x: tcp_key(x.tcp)), 1):
            yield (
                index,
                row.tcp,
                row.name,
                row.measuring_unit,
                format_count(row.count),
                format_number(row.work_cost),
                row.completion_date.strftime("%d.%m.%Y")
                if isinstance(row.completion_date, datetime.date)
                else row.completion_date,
            )


@dataclasses.dataclass
class HTMLData(GeneralData):
    contractor_agreement: str
    location: str
    comment: str
    request_number: int | None = None
    order_date: datetime.date | None = None
    order_number: int | None = None

    @property
    def json(self) -> str:
        return json.dumps(
            {
                "import_data": [
                    {
                        "BS_name": self.contractor_agreement,
                        "region": 0,
                        "address": self.location,
                        "Description": self.comment,
                        "table": [
                            {
                                "number": index,
                                "number_TCP": tcp,
                                "name": name,
                                "measuer": measuring_unit,
                                "quantity": count,
                                "date": completion_date,
                                "summ": work_cost,
                            }
                            for index, tcp, name, measuring_unit, count, work_cost, completion_date in self
                        ],
                    }
                ]
            },
            ensure_ascii=False,
        )


class HTMLConverter(Converter):
    def to_data_list(
        self,
        bytes_io: io.BytesIO,
        /,
        **kwargs,
    ) -> list[Data]:
        bs = bs4.BeautifulSoup(bytes_io, "html.parser")
        html_datas = []
        try:
            order_info = bs.select("table:nth-child(1) table:nth-child(1) p")[0].text
        except IndexError:
            raise ConvertError("Информация о заказе не найдена.")
        if match := re.search(r"\d{1,2}\.\d{1,2}\.\d{4}", order_info):
            order_date = datetime.datetime.strptime(match[0], "%d.%m.%Y")
        else:
            raise ConvertError("Дата заказа не найдена")
        for b in bs.select("center > p > b"):
            text = b.text
            if match := re.search(
                r"\d+\.\s+ВЕДОМОСТЬ\s+исполнения\s+работ\s+(.+?\"(.+?)\".*?[-,]\s+(.+))",
                text,
                re.IGNORECASE,
            ):
                comment = match[1]
                contractor_agreement = match[2]
                location = match[3]
            else:
                raise ConvertError(
                    "Номер базовой станций, имя базовой станций и местоположение не найдено"
                )
            if match := re.search(
                r"Номер\s+заказа\s*:\s+\[(\d*)]\s+Регион\s*:\s+\[(.*?)]\s+Номер\s+Заявки\s+на\s+приобретение\s*:\s+\[(\d*)]",
                text,
                re.IGNORECASE,
            ):
                order_number = int(match[1]) if match[1] else None
                request_number = int(match[3]) if match[3] else None
            else:
                raise ConvertError(
                    "Номер заказа, регион, номер Заявки на приобретение не найден"
                )

            rows = []
            tables = b.select("table")
            if not tables:
                raise ConvertError("Таблица не найдена")
            new_format = None
            for row in tables[0].select("table tr"):
                columns = row.select("td")
                if new_format is None:
                    new_format = "услуга/тмц" == columns[3].text.strip().lower()
                    continue
                tcp = columns[1].text.strip()
                name = columns[2].text.strip()
                type = columns[3].text.strip() if new_format else None
                measuring_unit = columns[3 + new_format].text.strip()
                count = to_float(columns[4 + new_format].text.strip())
                work_cost = to_float(columns[5 + new_format].text.strip())
                completion_date = to_date(columns[6 + new_format].text.strip())
                rows.append(
                    DataRow(
                        tcp,
                        name,
                        type,
                        measuring_unit,
                        count,
                        work_cost,
                        completion_date,
                    )
                )

            html_datas.append(
                HTMLData(
                    comment=comment,
                    order_number=order_number,
                    request_number=request_number,
                    contractor_agreement=contractor_agreement,
                    location=location,
                    rows=rows,
                    order_date=order_date,
                )
            )
        return html_datas


@dataclasses.dataclass
class PDFData(GeneralData):
    accounting_system_number: str
    turnover_date: datetime.date | str

    @property
    def json(self) -> str:
        return json.dumps(
            {
                "import_data": {
                    "PlanDays": 20,
                    "Invoice1CNo": self.accounting_system_number,
                    "DateInvoiced": format_date(self.turnover_date),
                    "table": [
                        {
                            "M_Product_ID": row.tcp,
                            "LineNetAmt": row.work_cost,
                            "Quantity": row.count,
                        }
                        for row in self.rows
                    ],
                }
            },
            ensure_ascii=False,
        )


class PDFConverter(Converter):
    def to_data_list(
        self,
        bytes_io: io.BytesIO,
        /,
        **kwargs,
    ) -> list[Data]:
        with pdfplumber.open(bytes_io) as pdf:
            text = pdf.pages[0].extract_text()

            if match := re.search(r"Номер\s+учетной\s+системы\s+0+(\d+)", text):
                accounting_system_number = match[1]
            else:
                raise ConvertError("Номер учетной системы не найден")
            if match := re.search(
                r"Дата\s+совершения\s+оборота\s+(\d{1,2}\.\d{1,2}\.\d{4})", text
            ):
                try:
                    turnover_date = datetime.datetime.strptime(match[1], "%d.%m.%Y")
                except ValueError:
                    turnover_date = match[1]
            else:
                raise ConvertError("Дата совершения оборота не найден")
            try:
                table = []
                for page in pdf.pages[1:]:
                    page.chars[:86] = []  # Это, чтобы убрать цифровую подпись.
                    for extracted_table in page.extract_tables():
                        table.extend(
                            [column and column.replace("\n", " ") for column in row]
                            for row in extracted_table
                        )
                rows = []
                start_index = next(
                    (index for index, row in enumerate(table) if row[0].isdigit()), None
                )
                if start_index is not None:
                    for row in table[start_index:]:
                        if row[0] and not row[0].isdigit():
                            break
                        if "" in row:
                            last_row = rows[-1]
                            last_row.name += " " + row[2]
                            last_row.measuring_unit += " " + row[3]
                        else:
                            try:
                                completion_date = datetime.datetime.strptime(
                                    row[6], "%d.%m.%Y"
                                ).date()
                            except ValueError:
                                completion_date = row[6]
                            rows.append(
                                DataRow(
                                    remove_spaces(row[1]),
                                    row[2],
                                    None,
                                    row[3],
                                    to_float(row[4]),
                                    to_float(row[5]),
                                    completion_date,
                                )
                            )
            except Exception as error:
                raise ConvertError(f"Неизвестная ошибка: {error}")
            return [
                PDFData(
                    rows=rows,
                    turnover_date=turnover_date,
                    accounting_system_number=accounting_system_number,
                )
            ]


converters = {
    mimetypes.types_map[".html"]: HTMLConverter(
        "order_entry_as_html/order_entry_template_kar_tel_html.html"
    ),
    mimetypes.types_map[".pdf"]: PDFConverter(
        "order_entry_as_html/order_entry_template_kar_tel_pdf.html"
    ),
}
