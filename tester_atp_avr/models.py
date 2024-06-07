from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AvhObject


class TCPFile(models.Model):
    name = models.CharField(max_length=256, unique=True)
    file = models.FileField(
        upload_to="p1/tester_atp_avr/tcp_files",
        validators=[FileExtensionValidator(["xlsx"])],
    )
    loaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name}"


class TCPCategory(AvhObject):
    tcp_category_id = models.IntegerField(_("№ п/п"))
    tcp_file = models.ForeignKey(TCPFile, on_delete=models.CASCADE, null=True)
    name = models.TextField()
    note = models.TextField(_("Примечание"), null=True, blank=True)

    class Meta:
        ordering = ["tcp_category_id"]

    def __str__(self) -> str:
        return f"{self.tcp_category_id} - {self.name}"


class TCP(AvhObject):
    tcp_id = models.IntegerField(_("№ п/п"))
    tcp_category = models.ForeignKey(TCPCategory, on_delete=models.CASCADE, null=True)
    name = models.TextField(_("Наименование работ"))
    price = models.IntegerField(_("Цена ТЦП, тг за ед., без НДС"))

    measuring_unit = models.CharField(_("Единица измерения"), max_length=256, blank=True)
    note = models.TextField(_("Примечание"), null=True, blank=True)

    class Meta:
        ordering = ["tcp_category__tcp_category_id", "tcp_id"]

    @property
    def number(self) -> str:
        return f"{self.tcp_category.tcp_category_id}.{self.tcp_id}"

    def __str__(self) -> str:
        return f"{self.number} - {self.name}"


class WorkType(AvhObject):
    name = models.CharField(_("Вид работ"), max_length=550)
    default_checked = models.BooleanField(_("По умолчанию"), default=False)

    def __str__(self) -> str:
        return f"{self.name}"

class ContratcNumberAndDate(AvhObject):
    name = models.CharField(_("Номер и дата договора"), max_length=550)
    default_checked = models.BooleanField(_("По умолчанию"), default=False)

    def __str__(self) -> str:
        return f"{self.name}"