import abc

from avh_services.constants import VAT
from avh_services.formatters import format_number, format_number_as_words


class Data(abc.ABC):
    @property
    @abc.abstractmethod
    def json(self) -> str:
        pass


class TotalMixin(abc.ABC):
    @property
    @abc.abstractmethod
    def total(self) -> float:
        pass

    @property
    def total_formatted(self) -> str:
        return format_number(self.total)

    @property
    def total_vat(self) -> float:
        return self.total * VAT / 100

    @property
    def total_vat_formatted(self) -> str:
        return format_number(self.total_vat)

    @property
    def total_with_vat(self) -> float:
        return self.total + self.total_vat

    @property
    def total_with_vat_formatted(self) -> str:
        return format_number(self.total_with_vat)

    @property
    def total_with_vat_as_words(self) -> str:
        return f"Всего общая стоимость работ: {format_number_as_words(self.total_with_vat)}, включая НДС {VAT}%"
