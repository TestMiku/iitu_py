import copy
import datetime
from json import JSONDecoder, JSONEncoder

import colorfield
from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AvhObject


# Create your models here.
class DebtChangesHistory(AvhObject):
    debt_document = models.ForeignKey(
        "document_debts.DebtDocument",
        on_delete=models.CASCADE,
        related_name="unclosedbalance_change_history",
    )
    old = models.JSONField(encoder=JSONEncoder, decoder=JSONDecoder)
    new = models.JSONField(encoder=JSONEncoder, decoder=JSONDecoder)

    def __str__(self):
        return self.debt_document.documentno


class DebtDocument(models.Model):
    debt_supplier = models.ForeignKey(
        "document_debts.DebtSupplier",
        verbose_name=_("debt_supplier"),
        on_delete=models.CASCADE,
        related_name="debt_documents",
        blank=True,
        null=True,
    )

    # Даты
    dateinvoiced = models.DateTimeField(
        _("dateinvoiced"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    datascheta = models.DateTimeField(
        _("datascheta"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    daterefund = models.DateTimeField(
        _("daterefund"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    docdate = models.DateTimeField(
        _("docdate"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    dateprocessed = models.DateTimeField(
        _("dateprocessed"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    paydate1c = models.DateTimeField(
        _("paydate1c"), auto_now=False, auto_now_add=False, blank=True, null=True
    )

    # Суммы и числа
    totallines = models.FloatField(_("totallines"), blank=True, null=True)
    payamt1c = models.FloatField(_("payamt1c"), blank=True, null=True)
    notpayamt1c = models.FloatField(_("notpayamt1c"), blank=True, null=True)
    sumpaid = models.FloatField(_("sumpaid"), blank=True, null=True)
    c_currency_id = models.FloatField(_("c_currency_id"), blank=True, null=True)
    refundamt = models.FloatField(_("refundamt"), blank=True, null=True)
    quantity = models.FloatField(_("quantity"), blank=True, null=True)
    amount = models.FloatField(_("amount"), blank=True, null=True)
    invoiceamount = models.FloatField(_("invoiceamount"), blank=True, null=True)
    refundamtkzt = models.FloatField(_("refundamtkzt"), blank=True, null=True)
    totallineskzt = models.FloatField(_("totallineskzt"), blank=True, null=True)
    payamt1ckzt = models.FloatField(_("payamt1ckzt"), blank=True, null=True)
    notpayamt1ckzt = models.FloatField(_("notpayamt1ckzt"), blank=True, null=True)
    notpayamt1ckztcross = models.FloatField(
        _("notpayamt1ckztcross"), blank=True, null=True
    )
    unclosedbalance = models.FloatField(_("unclosedbalance"), blank=True, null=True)
    c_invoice_id = models.FloatField(_("c_invoice_id"), blank=True, null=True)

    # Строки
    colgroup = models.CharField(_("Группа"), max_length=5000, blank=True, null=True)
    documentno = models.CharField(
        _("documentno"), max_length=5000, blank=True, null=True, db_index=True
    )
    name = models.TextField(_("name"), blank=True, null=True)
    nscheta = models.CharField(_("nscheta"), max_length=5000, blank=True, null=True)
    dogovor = models.CharField(_("dogovor"), max_length=5000, blank=True, null=True)
    coment = models.TextField(_("coment"), blank=True, null=True)
    status = models.CharField(_("status"), max_length=5000, blank=True, null=True)
    too = models.CharField(_("too"), max_length=5000, blank=True, null=True)
    postavshik = models.CharField(
        _("postavshik"), max_length=5000, blank=True, null=True
    )
    bin = models.CharField(_("bin"), max_length=5000, blank=True, null=True)
    accountno = models.CharField(_("accountno"), max_length=5000, blank=True, null=True)
    bank = models.CharField(_("bank"), max_length=5000, blank=True, null=True)
    otvzakup = models.CharField(_("otvzakup"), max_length=5000, blank=True, null=True)
    utverditel = models.CharField(
        _("utverditel"), max_length=5000, blank=True, null=True
    )
    gruppa_proekrov = models.TextField(
        _("gruppa_proekrov"), blank=True, null=True
    )
    valyuta = models.CharField(_("valyuta"), max_length=5000, blank=True, null=True)
    napravlenie = models.CharField(
        _("napravlenie"), max_length=5000, blank=True, null=True
    )
    error_txt = models.CharField(_("error_txt"), max_length=5000, blank=True, null=True)
    dname = models.CharField(_("dname"), max_length=5000, blank=True, null=True)
    docstatus = models.CharField(_("docstatus"), max_length=5000, blank=True, null=True)
    icname = models.CharField(_("icname"), max_length=5000, blank=True, null=True)
    chname = models.CharField(_("chname"), max_length=5000, blank=True, null=True)
    createdby = models.CharField(_("createdby"), max_length=5000, blank=True, null=True)
    nomdocument1 = models.CharField(
        _("nomdocument1"), max_length=5000, blank=True, null=True
    )
    datadoc = models.CharField(_("datadoc"), max_length=5000, blank=True, null=True)
    komment = models.CharField(_("komment"), max_length=5000, blank=True, null=True)
    nepredorigdoc = models.CharField(
        _("nepredorigdoc"), max_length=5000, blank=True, null=True
    )
    isattached = models.CharField(
        _("isattached"), max_length=5000, blank=True, null=True
    )
    factnumdoc = models.CharField(
        _("factnumdoc"), max_length=5000, blank=True, null=True
    )
    doc_number = models.CharField(
        _("doc_number"), max_length=5000, blank=True, null=True
    )
    site = models.CharField(_("site"), max_length=5000, blank=True, null=True)
    actdocno = models.CharField(_("actdocno"), max_length=5000, blank=True, null=True)
    docserviceact = models.CharField(
        _("docserviceact"), max_length=5000, blank=True, null=True
    )
    region = models.CharField(_("region"), max_length=5000, blank=True, null=True)
    security_agreed = models.CharField(
        _("security_agreed"), max_length=5000, blank=True, null=True
    )
    last_unclosedbalance_change = models.FloatField(
        _("last_unclosedbalance_change"), blank=True, null=True
    )

    def __str__(self):
        return f"{self.documentno}"

    def get_last_unclosedbalance_change(self):
        change_history = self.unclosedbalance_change_history.all().order_by(
            "-created_at",
        )
        if change_history:
            change_history = change_history.first()
            try:
                return float(change_history.new["unclosedbalance"]) - float(
                    change_history.old["unclosedbalance"]
                )
            except (KeyError, ValueError):
                return 0
        return 0

    @property
    def unclosedbalance_changes(self):
        change_history = self.unclosedbalance_change_history.all().order_by(
            "-created_at",
        )
        return change_history


class DebtSupplier(AvhObject):
    too = models.CharField(
        verbose_name="ТОО",
        max_length=255,
        null=True,
        blank=True,
        default="Неизвестный контрагент",
    )
    bin = models.CharField(verbose_name="БИН", max_length=30, unique=True)
    postavshik = models.CharField(
        verbose_name="Поставщик",
        max_length=255,
        null=True,
        blank=True,
        default="Неизвестный поставщик",
    )

    responsible = models.ForeignKey(
        "main.AvhUser",
        verbose_name="Ответственный",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="debt_supplier_responsible",
    )

    is_problematic = models.BooleanField(
        verbose_name="Проблемный контрагент", default=False
    )
    is_excluded = models.BooleanField(verbose_name="Исключен", default=False)
    exception_reason = models.TextField(
        verbose_name="Причина исключения", null=True, blank=True
    )
    supplier_status = models.ForeignKey(
        "document_debts.DebtStatus",
        verbose_name="Статус поставщика",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="debt_supplier_status",
    )
    debts_total_unclosedbalance = models.FloatField(
        verbose_name="Общая задолженность", default=0
    )

    def __str__(self):
        return self.postavshik

    def get_debts_total_unclosedbalance(self):
        debt_documents = self.debt_documents.all()
        total_summ = 0
        for doc in debt_documents:
            total_summ += doc.unclosedbalance if doc.unclosedbalance else 0
        return total_summ

    last_unclosedbalance_change = models.FloatField(
        _("last_unclosedbalance_change"), blank=True, null=True
    )

    def get_last_unclosedbalance_change(self):
        try:
            documents = self.debt_documents.all()
            total_summ = 0
            for doc in documents:
                total_summ += (
                    doc.last_unclosedbalance_change
                    if doc.last_unclosedbalance_change
                    else 0
                )
            return total_summ
        except ValueError:
            print("VALUE ERROR")
            return 0

    def debt_documents_ordered(self):
        return self.debt_documents.order_by("-unclosedbalance")


class DebtImportError(models.Model):
    error_traceback = models.TextField(_("error_traceback"), null=True, blank=True)
    error_name = models.CharField(_("error_name"), max_length=255)
    item = models.JSONField(_("item"), encoder=JSONEncoder, decoder=JSONDecoder)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.error_name


class DebtPermanentFilter(AvhObject):
    name = models.CharField(_("name"), max_length=255)
    value = models.JSONField(_("value"), encoder=JSONEncoder, decoder=JSONDecoder)

    def __str__(self):
        return self.name


class DebtStatus(AvhObject):
    name = models.CharField(_("name"), max_length=255)
    color = colorfield.fields.ColorField(default="#4e73df")

    def __str__(self):
        return self.name


def get_dict(obj):
    fields = [
        "colgroup",
        "documentno",
        "name",
        "dateinvoiced",
        "nscheta",
        "dogovor",
        "datascheta",
        "coment",
        "status",
        "too",
        "postavshik",
        "bin",
        "accountno",
        "bank",
        "totallines",
        "payamt1c",
        "notpayamt1c",
        "otvzakup",
        "utverditel",
        "gruppa_proekrov",
        "valyuta",
        "napravlenie",
        "error_txt",
        "sumpaid",
        "dname",
        "docstatus",
        "paydate1c",
        "icname",
        "chname",
        "createdby",
        "nomdocument1",
        "datadoc",
        "komment",
        "nepredorigdoc",
        "isattached",
        "factnumdoc",
        "doc_number",
        "site",
        "c_currency_id",
        "refundamt",
        "daterefund",
        "actdocno",
        "docserviceact",
        "docdate",
        "dateprocessed",
        "quantity",
        "amount",
        "region",
        "invoiceamount",
        "security_agreed",
        "refundamtkzt",
        "totallineskzt",
        "payamt1ckzt",
        "notpayamt1ckzt",
        "notpayamt1ckztcross",
        "unclosedbalance",
        "c_invoice_id",
    ]
    return {
        field: (
            getattr(obj, field).strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(getattr(obj, field), datetime.datetime)
            else str(getattr(obj, field))
        )
        for field in fields
    }
