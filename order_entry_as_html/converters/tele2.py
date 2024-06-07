import dataclasses
import datetime
import io
import itertools
import json
import mimetypes
import os
import re
import tempfile
from collections.abc import Iterator
from contextlib import suppress

import pandas
from camelot import read_pdf
from pypdf import PdfReader

from avh_services.constants import VAT
from avh_services.formatters import (
    format_count,
    format_number,
    remove_spaces,
    format_date,
)
from avh_services.keys import tcp_key
from .converter import Converter, to_float, to_date
from .data import Data, TotalMixin
from .exceptions import ConvertError
from ..models import OrderRegion


@dataclasses.dataclass(slots=True, frozen=True)
class Row:
    tcp: str
    name: str
    measuring_unit: str
    count: float
    work_cost: float
    material_price: float
    coefficient: float
    site: "Site"

    @property
    def material_price_with_vat(self) -> float:
        return self.material_price * (1 + VAT / 100)


@dataclasses.dataclass
class Site:
    name: str
    rows: list[Row] = dataclasses.field(default_factory=list)

    @property
    def total(self) -> float:
        return sum(row.material_price for row in self.rows)


@dataclasses.dataclass
class PDFData(Data, TotalMixin):
    order_number: int
    order_date: datetime.date
    contractor_agreement: str
    customer: str
    contactor: str
    work_type: str
    work_type_by_order: str
    start_work_date: datetime.date
    end_work_date: datetime.date
    critical_delinquency: datetime.timedelta
    sites: list[Site]
    region: int | None
    contract_date: datetime.date | None = None
    integration_date: datetime.date | None = None

    @property
    def title(self) -> str:
        return f"Заказ №{self.order_date} от {self.order_date.strftime('%d.%m.%Y')}г. к Договору подряда {self.contractor_agreement}"

    @property
    def completion_date(self) -> datetime.timedelta:
        return self.end_work_date - self.start_work_date

    @property
    def json(self) -> str:
        return json.dumps(
            {
                "import_data": [
                    {
                        "BS_name": self.contractor_agreement,
                        "datesignagreement3": format_date(self.order_date),
                        "datesignagreement2": format_date(self.contract_date),
                        "agreement3": self.order_number,
                        "region": self.region,
                        "address": "",
                        "table": [
                            {
                                "number": index,
                                "number_TCP": tcp,
                                "name": name,
                                "measuer": measuring_unit,
                                "quantity": count,
                                "date": self.completion_date.days,
                                "summ": material_price_with_vat,
                            }
                            for index, _, tcp, name, measuring_unit, count, _, _, _, material_price_with_vat in self
                        ],
                    }
                ]
            },
            ensure_ascii=False,
        )

    @property
    def total(self) -> float:
        return sum(site.total for site in self.sites)

    def __iter__(
        self,
    ) -> Iterator[tuple[int, tuple[int, str], str, str, str, str, str, str, str]]:
        rows = sorted(
            itertools.chain.from_iterable(site.rows for site in self.sites),
            key=lambda x: (x.site.name, tcp_key(x.tcp)),
        )

        for index, row in enumerate(rows, 1):
            yield index, (
                len(row.site.rows),
                row.site.name,
            ), row.tcp, row.name, row.measuring_unit, format_count(
                row.count
            ), format_number(
                row.work_cost
            ), format_number(
                row.material_price
            ), format_count(
                row.coefficient
            ), format_number(
                row.material_price_with_vat
            )


class StopTake(Exception):
    pass


class PDFConverter(Converter):
    def to_data_list(
        self,
        bytes_io: io.BytesIO,
        /,
        *,
        region: OrderRegion | None = None,
        contract_date: datetime.date | None = None,
        **kwargs,
    ) -> list[Data]:
        if region is None:
            raise ConvertError("Выберете регион")
        if contract_date is None:
            raise ConvertError("Выберете дата подписание контракта")
        fd, path = tempfile.mkstemp(".pdf")
        with os.fdopen(fd, "wb") as temporary_file:
            temporary_file.write(bytes_io.read())
        try:
            table_list = read_pdf(path, pages="all", line_scale=45)
        except Exception:
            raise ConvertError("Возможно у таблицы нету четких границ")
        sites = []

        with suppress(StopTake):
            for table in table_list:
                dataframe: pandas.DataFrame = table.df
                for index, row in dataframe.iterrows():
                    if len(row) != 9:
                        raise StopTake
                    if index == 0:
                        continue
                    if site_name := remove_spaces(row[0]):
                        sites.append(Site(site_name))

                    if not sites:
                        raise ConvertError("Имя сайта не найдена")
                    sites[-1].rows.append(
                        Row(
                            remove_spaces(row[1]),
                            row[2].strip(),
                            remove_spaces(row[3]),
                            to_float(row[4]),
                            to_float(row[5]),
                            to_float(row[6]),
                            to_float(row[7]),
                            sites[-1],
                        )
                    )
        pdf_reader = PdfReader(path)
        page1_text = pdf_reader.pages[0].extract_text()
        if order := re.search(
            r"Заказ\s*№(\d+)\s*от\s*(\d{1,2}\.\d{1,2}\.\d{4}).*?\s*к\s*Договору\s*подряда\s*(.+)",
            page1_text,
        ):
            order_number = int(order[1])
            order_date = to_date(order[2])
            contractor_agreement = order[3].rstrip()
        else:
            raise ConvertError("Заказ не найден")
        if customer := re.search(r"Заказчик:\s*(.+)", page1_text):
            customer = customer[1].rstrip()
        else:
            raise ConvertError("Заказчик не найден")
        if contactor := re.search(r"Подрядчик:\s*(.+)", page1_text):
            contactor = contactor[1].rstrip()
        else:
            raise ConvertError("Подрядчик не найден")
        if work_type := re.search(r"Тип\s+работ:\s*(.+)", page1_text):
            work_type = work_type[1].rstrip()
        else:
            raise ConvertError("Тип работ не найден")
        if work_type_by_order := re.search(
            r"Вид\s+работ\s+по\s+заказу:\s*(.+)", page1_text
        ):
            work_type_by_order = work_type_by_order[1].rstrip()
        else:
            raise ConvertError("Вид работ по заказу не найден")
        if start_work_date := re.search(
            r"Дата\s+начала\s+выполнения\s+работ:\s*(\d{1,2}\.\d{1,2}\.\d{4})",
            page1_text,
        ):
            start_work_date = datetime.datetime.strptime(
                start_work_date[1], "%d.%m.%Y"
            ).date()
        else:
            raise ConvertError("Дата начала выполнения работ не найден")
        integration_date = None
        if integration_date := re.search(
            r"Дата\s+выполнения\s+интеграции:\s*(\d{1,2}\.\d{1,2}\.\d{4})", page1_text
        ):
            integration_date = datetime.datetime.strptime(
                integration_date[1], "%d.%m.%Y"
            ).date()
        if end_work_date := re.search(
            r"Дата\s+окончания\s+работ:\s*(\d{1,2}\.\d{1,2}\.\d{4})", page1_text
        ):
            end_work_date = datetime.datetime.strptime(
                end_work_date[1], "%d.%m.%Y"
            ).date()
        else:
            raise ConvertError("Дата окончания работ не найден")
        if critical_delinquency := re.search(
            r"Критическая\s+просрочка\s+\(дней\):\s*(\d+)", page1_text
        ):
            critical_delinquency = datetime.timedelta(days=int(critical_delinquency[1]))
        else:
            raise ConvertError("Критическая просрочка (дней) не найден")

        os.remove(path)
        return [
            PDFData(
                order_number=order_number,
                order_date=order_date,
                contractor_agreement=contractor_agreement,
                customer=customer,
                contactor=contactor,
                work_type=work_type,
                region=None if region is None else region.code,
                work_type_by_order=work_type_by_order,
                start_work_date=start_work_date,
                integration_date=integration_date,
                end_work_date=end_work_date,
                critical_delinquency=critical_delinquency,
                sites=sites,
                contract_date=contract_date,
            )
        ]


converters = {
    mimetypes.types_map[".pdf"]: PDFConverter(
        "order_entry_as_html/order_entry_template_tele2.html"
    )
}
