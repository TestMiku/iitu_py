import datetime
import decimal
import re
import typing
from ast import mod
from functools import cached_property

from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import OuterRef, QuerySet, Subquery, Sum
from django.db.models.fields import DecimalField
from django.db.models.functions import Coalesce, TruncDate
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

User: typing.TypeAlias = get_user_model()
# TODO: Надо перенести всё связанное с логикой в services.


class TableCellColorCategory(models.Model):
    name = models.CharField(max_length=512)
    parent = models.ForeignKey(
        "TableCellColorCategory",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children_categories",
        related_query_name="children_category",
    )
    key = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.key

    class Meta:
        verbose_name = "Категория цветов ячеек"
        verbose_name_plural = "Категорий цветов ячеек"


def get_table_cell_color_category_key(instance: TableCellColorCategory) -> str:
    return (
        f"{get_table_cell_color_category_key(instance.parent)}.{instance.name}"
        if instance.parent
        else instance.name
    )


def get_table_cell_color_key(instance: "TableCellColor") -> str:
    return f"{instance.category.key}.{instance.name}"


def update_keys(instance: TableCellColorCategory) -> None:
    instance.key = get_table_cell_color_category_key(instance)
    try:
        for child_color in instance.children_colors.all():
            child_color.key = get_table_cell_color_key(child_color)
            child_color.save()
        for child_category in instance.children_categories.all():
            update_keys(child_category)
            child_category.save()
    except ValueError:
        pass


@receiver(pre_save, sender=TableCellColorCategory)
def _(
    sender: type[TableCellColorCategory], instance: TableCellColorCategory, **kwargs
) -> None:
    update_keys(instance)


class TableCellColor(models.Model):
    name = models.CharField(max_length=512)
    color = ColorField()
    category = models.ForeignKey(
        TableCellColorCategory,
        on_delete=models.CASCADE,
        related_name="children_colors",
        related_query_name="children_color",
    )
    key = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.key

    class Meta:
        verbose_name = "Цвет ячейки"
        verbose_name_plural = "Цвета ячеек"


@receiver(pre_save, sender=TableCellColor)
def _(sender: type[TableCellColor], instance: TableCellColor, **kwargs) -> None:
    instance.key = get_table_cell_color_key(instance)


class Subdivision(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
        ordering = ["name"]


class ProjectRegion(models.Model):
    name = models.CharField(max_length=256)
    director_display = models.CharField(max_length=128, null=True, blank=True)
    director = models.ForeignKey(
        User,
        related_name="project_regions",
        related_query_name="project_region",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )  # Директор

    manager_display = models.CharField(max_length=128, null=True, blank=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )  # Руководитель

    project_manager_display = models.CharField(max_length=128, null=True, blank=True)
    project_manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )  # ПМ
    users = models.ManyToManyField(User, blank=True)
    subdivision = models.ForeignKey(
        Subdivision, on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def percent(self) -> decimal.Decimal:
        from .services import mandatory_payments_service

        try:
            mandatory_payment_accrual_calculator_project_region = mandatory_payments_service.get_coefficient_1().mandatory_payment_accrual_calculator_project_regions.get(
                project_region=self
            )
        except MandatoryPaymentAccrualCalculatorProjectRegion.DoesNotExist:
            return decimal.Decimal()
        else:
            return mandatory_payment_accrual_calculator_project_region.coefficient

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Регион проекта"
        verbose_name_plural = "Регионы проектов"
        ordering = ["director_display"]


class ProjectRegionApprover(models.Model):
    user: User = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+", related_query_name="+"
    )
    project_region = models.ForeignKey(
        ProjectRegion,
        on_delete=models.RESTRICT,
        related_name="approvers",
        related_query_name="approver",
    )

    def __str__(self) -> str:
        return f"{self.project_region} - {self.user.get_full_name()}"

    class Meta:
        unique_together = ["user", "project_region"]


class ProjectRegionApproverProject(models.Model):
    number = models.IntegerField()
    approver = models.ForeignKey(
        ProjectRegionApprover,
        on_delete=models.RESTRICT,
        related_name="projects",
        related_query_name="project",
    )

    def __str__(self) -> str:
        return f"{self.approver} - {self.number}"

    class Meta:
        unique_together = ["approver", "number"]


class TransferStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Статус перевода между р/с"
        verbose_name_plural = "Статусы перевода между р/с"


def default_transfer_status() -> TransferStatus:
    return TransferStatus.objects.get_or_create(name="Отправлено на подтверждение")[0]


def get_default_transfer_status_id():
    status, created = TransferStatus.objects.get_or_create(
        name="Отправлено на подтверждение"
    )
    return status.id


def default_transfer_status_id() -> int:
    return default_transfer_status().id


def completed_transfer_status() -> TransferStatus:
    return TransferStatus.objects.get_or_create(name="Подтверждено")[0]


def rejected_transfer_status() -> TransferStatus:
    return TransferStatus.objects.get_or_create(name="Отклонено")[0]


class Transfer(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    from_whom = models.ForeignKey(
        "ProjectRegion", on_delete=models.CASCADE, related_name="+"
    )
    from_account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, related_name="+"
    )
    to_account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, related_name="+"
    )
    to_whom = models.ForeignKey(ProjectRegion, on_delete=models.CASCADE, related_name="+", null=True)
    responsible = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    sum = models.DecimalField(max_digits=25, decimal_places=10)
    status = models.ForeignKey(
        TransferStatus,
        on_delete=models.SET_DEFAULT,
        default=get_default_transfer_status_id,
    )

    def complete(self, *, responsible: User | None = None) -> None:
        self.status = completed_transfer_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.TRANSFER,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def reject(
        self, *, responsible: User | None = None, reject_comment: str | None = None
    ) -> None:
        self.status = rejected_transfer_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.TRANSFER,
            responsible=responsible,
            status=self.status.name,
            rejected_comment=reject_comment,
        )
        self.save()

    def __str__(self) -> str:
        return f"Перевод между р/с {self.from_whom}, с р/с {self.from_account} в р/с {self.to_account}, сумма {self.sum}"

    class Meta:
        verbose_name = "Перевод между р/с проект региона"
        verbose_name_plural = "Переводы между р/с проект регионов"


class Account(models.Model):
    number = models.CharField(max_length=20)
    name = models.CharField(max_length=256)
    subdivision = models.ForeignKey(
        Subdivision, on_delete=models.RESTRICT, null=True, blank=True
    )
    is_cash_register = models.BooleanField(default=False)
    available_for = models.ManyToManyField(
        ProjectRegion, related_name="accounts", related_query_name="account", blank=True
    )

    def balance(
        self, project_region: ProjectRegion | None = None, /
    ) -> decimal.Decimal:
        from .services import common_service

        return common_service.get_account_balance(self, project_region)

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = ["name", "number"]
        verbose_name = "Расчётный счёт"
        verbose_name_plural = "Расчётные счёта"
        ordering = ["name"]


class InflowManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return (
            super()
            .get_queryset()
            .annotate(
                reserve=models.F("sum") * (models.F("reserve_percent") / 100),
                remainder=models.F("sum") - models.F("reserve"),
            )
        )


class Inflow(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="inflows",
        related_query_name="inflow",
    )
    project_region = models.ForeignKey(
        ProjectRegion,
        on_delete=models.CASCADE,
        related_name="inflows",
        related_query_name="inflow",
    )
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    reserve_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=decimal.Decimal(),
        validators=[MinValueValidator(-1), MaxValueValidator(101)],
    )
    date = models.DateField(default=timezone.localdate)
    imported_from_file = models.BooleanField(default=False, editable=False)
    objects = InflowManager()

    def __str__(self) -> str:
        return f"{self.account} {self.project_region} {self.sum}"

    class Meta:
        verbose_name = "Поступление"
        verbose_name_plural = "Поступлений"


class PaymentConfirmationHistory(models.Model):
    model_id = models.IntegerField()

    class ModelName(models.TextChoices):
        MANDATORY_PAYMENT_SEIZURE = "MandatoryPaymentSeizure"
        PAID_INVOICE = "PaidInvoice"
        DEBT_TRANSLATE_GROUP = "DebtTranslateGroup"
        TRANSFER = "Transfer"
        SUTOCHNYE = "Sutochnye"
        ADMINISTRATIVE_TRANSFER = "AdministrativeTransfer"

    model_name = models.CharField(
        max_length=max(len(i[0]) for i in ModelName.choices),
        choices=ModelName.choices,
    )
    status = models.CharField(max_length=256)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rejected_comment = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        model_instance = self.get_model_instance()
        return f"{self.responsible} изменил статус {model_instance} на {self.status}, {self.created_at}"

    def get_model_instance(
        self,
    ) -> typing.Optional[
        typing.Union["MandatoryPaymentSeizure", "PaidInvoice", "DebtTranslateGroup"]
    ]:
        try:
            model_class: type[models.Model] = eval(self.model_name)
        except NameError:
            return None
        if not issubclass(model_class, models.Model):
            return None
        try:
            return model_class.objects.get(id=self.model_id)
        except model_class.DoesNotExist:
            return None

    class Meta:
        verbose_name = "История подтвежденного платежа"
        verbose_name_plural = "История подтвежденных платежей"


class DebtTranslateGroupStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Статус долга"
        verbose_name_plural = "Статусы долгов"


def default_debt_translate_group_status() -> DebtTranslateGroupStatus:
    return DebtTranslateGroupStatus.objects.get_or_create(
        name="Отправлено на подтверждение"
    )[0]


def default_debt_translate_group_status_id() -> int:
    return default_debt_translate_group_status().id


def completed_debt_translate_group_status() -> DebtTranslateGroupStatus:
    return DebtTranslateGroupStatus.objects.get_or_create(name="Подтверждено")[0]


REJECTED_DEBT_TRANSLATE_GROUP_STATUS_NAME: typing.Final[str] = "Отклонено"


def rejected_debt_translate_group_status() -> DebtTranslateGroupStatus:
    return DebtTranslateGroupStatus.objects.get_or_create(
        name=REJECTED_DEBT_TRANSLATE_GROUP_STATUS_NAME
    )[0]


class Setoff(models.Model):
    responsible = models.ForeignKey(
        User, null=True, blank=True, related_name="+", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Взаимозачёт {self.responsible} {self.created_at}"

    class Meta:
        verbose_name = "Взаимозачёт"
        verbose_name_plural = "Взаимозачёты"


class DebtTranslateGroup(models.Model):
    from_whom = models.CharField(max_length=512)
    from_account = models.ForeignKey(
        Account,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
    )
    to_whom = models.CharField(max_length=512)
    to_account = models.ForeignKey(
        Account,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
    )
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    TYPE_CHOICES: typing.Final[list[tuple[str, str]]] = [
        ("plus_minus", "Прямой долг"),
        ("minus_plus", "Погашение долга"),
        ("plus_minus_plus", "Взаимозачёт (+, -, +)"),
        ("minus_plus_minus", "Взаимозачёт (-, +, -)"),
        ("plus_new_minus_to_plus", "Взаимозачёт (+, -, +) и новая ячейка"),
        ("minus_new_plus_to_minus", "Взаимозачёт (-, +, -) и новая ячейка"),
        (
            "minus_plus_and_plus_minus_plus",
            "Полное погашение долгов и взаимозачёт (+, -, +)",
        ),
    ]
    status = models.ForeignKey(
        DebtTranslateGroupStatus,
        on_delete=models.SET_NULL,
        null=True,
        default=default_debt_translate_group_status_id,
    )
    type = models.CharField(
        max_length=max(len(i[0]) for i in TYPE_CHOICES), choices=TYPE_CHOICES
    )
    datetime = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    common_director = models.BooleanField()
    setoff = models.ForeignKey(
        Setoff,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="debt_translate_groups",
        related_query_name="debt_translate_group",
    )

    def complete(self, *, responsible: User | None = None) -> None:
        self.status = completed_debt_translate_group_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.DEBT_TRANSLATE_GROUP,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def reject(
        self, *, responsible: User | None = None, reject_comment: str | None = None
    ) -> None:
        self.status = rejected_debt_translate_group_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.DEBT_TRANSLATE_GROUP,
            responsible=responsible,
            status=self.status.name,
            rejected_comment=reject_comment,
        )
        self.save()

    def __str__(self) -> str:
        return f'{self.get_type_display()}, перевод от {self.from_whom} с р/с {self.from_account} к {self.to_whom} на р/с {self.to_account}, сумма {self.sum}, общий директор: {"Да" if self.common_director else "Нет"}, ответсвенный {self.responsible}'

    class Meta:
        verbose_name = "Перевод долгов"
        verbose_name_plural = "Переводы долгов"


class Debt(models.Model):
    datetime = models.DateTimeField(default=timezone.localtime, null=True)
    from_whom = models.CharField(max_length=512)
    to_whom = models.CharField(max_length=512)
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    responsible = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    additional_properties = models.JSONField(null=True)
    note = models.TextField(null=True, blank=True)
    imported_from_file = models.BooleanField(default=False)
    renewed = models.BooleanField(default=False)
    group = models.ForeignKey(
        DebtTranslateGroup,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="debts",
        related_query_name="debt",
    )

    def __str__(self) -> str:
        return f'"{self.from_whom}" перевёл "{self.to_whom}" сумму {self.sum}'

    class Meta:
        verbose_name = "Долг"
        verbose_name_plural = "Долги"

    @cached_property
    def from_whom_as_project_region(self) -> ProjectRegion | None:
        try:
            return ProjectRegion.objects.get(name=self.from_whom)
        except ProjectRegion.DoesNotExist:
            return None

    @cached_property
    def to_whom_as_project_region(self) -> ProjectRegion | None:
        try:
            return ProjectRegion.objects.get(name=self.to_whom)
        except ProjectRegion.DoesNotExist:
            return None


class RenewableDebt(models.Model):
    from_whom = models.CharField(max_length=512)
    to_whom = models.CharField(max_length=512)
    sql = models.TextField()

    def __str__(self) -> str:
        return f'Обновляемый долг от "{self.from_whom}" к "{self.to_whom}"'

    class Meta:
        verbose_name = "Обновляемый долг"
        verbose_name_plural = "Обновляемые долги"


MONTHS: typing.Final[list[str]] = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


class MandatoryPaymentCategory(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    parent = models.ForeignKey(
        "MandatoryPaymentCategory", null=True, blank=True, on_delete=models.SET_NULL
    )
    color = ColorField(null=True, blank=True)

    def get_color(self) -> str | None:
        return self.color or self.parent and self.parent.get_color()

    def get_name(self) -> str:
        return self.name or f"ID: {self.id}"

    def __str__(self) -> str:
        return f"{self.parent} / {self.get_name()}" if self.parent else self.get_name()

    class Meta:
        ordering = ["parent__name", "name"]
        verbose_name = "Категория Обязательного платежа"
        verbose_name_plural = "Категорий Обязательных платежей"


class MandatoryPayment(models.Model):
    name = models.CharField(max_length=256, unique=True)
    deadline_template = models.CharField(max_length=256, null=True, blank=True)
    exception = models.BooleanField(default=False)
    category = models.ForeignKey(
        MandatoryPaymentCategory,
        related_name="mandatory_payments",
        related_query_name="mandatory_payment",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    monthly_payments = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    imported_from_file = models.BooleanField(default=False)

    def get_color(self) -> str | None:
        return self.category and self.category.get_color()

    def get_short_deadline_template(self) -> str:
        if self.deadline_template and (
            match := re.match(r"до \d+", self.deadline_template)
        ):
            return match[0]
        return self.deadline_template

    def get_deadline(self, date: datetime.date) -> datetime.date:
        if self.deadline_template is None:
            return date.replace(
                month=(date.month + 1) % 13 or 1, day=1
            ) - datetime.timedelta(days=1)
        elif match := re.match(
            r"до (\d+) числа каждого месяца", self.deadline_template
        ):
            try:
                return date.replace(day=int(match[1]))
            except ValueError:
                pass
        elif match := re.match(r"до (\d+) (\w+)", self.deadline_template):
            month = MONTHS.index(match[2]) + 1
            try:
                return date.replace(day=int(match[1]), month=month)
            except ValueError:
                date = date.replace(month=month)
        elif match := re.match(r"\d+", self.deadline_template):
            return date.replace(month=1, day=1) - datetime.timedelta(days=1)
        return date.replace(
            month=(date.month + 1) % 13 or 1, day=1
        ) - datetime.timedelta(days=1)

    def get_disbursements(self) -> decimal.Decimal:
        try:
            latest = self.accrual_groups.latest("datetime")
            return latest.was_accrued if latest else decimal.Decimal()
        except MandatoryPaymentAccrualGroup.DoesNotExist:
            return decimal.Decimal()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Обязательный платёж"
        verbose_name_plural = "Обязательные платежи"


class AccessToOthersExceptionForProjectManager(models.Model):
    project_manager = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="+"
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    datetime = models.DateTimeField(auto_now_add=True)


class MandatoryPaymentAccrualGroup(models.Model):
    mandatory_payment = models.ForeignKey(
        MandatoryPayment,
        on_delete=models.CASCADE,
        related_name="accrual_groups",
        related_query_name="accrual_group",
    )
    was_accrued = models.DecimalField(max_digits=25, decimal_places=10)
    accrual_amount = models.DecimalField(max_digits=25, decimal_places=10, null=True)
    datetime = models.DateField(default=timezone.now)
    responsible = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    imported_from_file = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Поступление {self.mandatory_payment} сумма {self.was_accrued}"

    class Meta:
        verbose_name = "Группа начилений"
        verbose_name_plural = "Группы начислений"


class MandatoryPaymentAccrual(models.Model):
    mandatory_payment = models.ForeignKey(
        MandatoryPayment,
        on_delete=models.CASCADE,
        related_name="accruals",
        related_query_name="accrual",
    )
    project_region = models.ForeignKey(
        ProjectRegion,
        on_delete=models.CASCADE,
        related_name="mandatory_payment_accruals",
        related_query_name="mandatory_payment_accrual",
    )
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    datetime = models.DateTimeField(default=timezone.now)
    deadline = models.DateField()
    note = models.TextField(null=True, blank=True)
    imported_from_file = models.BooleanField(default=False)
    group = models.ForeignKey(
        MandatoryPaymentAccrualGroup,
        related_name="accruals",
        related_query_name="accrual",
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.mandatory_payment} | {self.project_region} | {self.sum} | {self.deadline}"

    class Meta:
        verbose_name = "Начисление"
        verbose_name_plural = "Начисления"
        ordering = ["deadline"]


class MandatoryPaymentAccrualCalculator(models.Model):
    TYPES: typing.Final[set[str]] = [
        ("coefficient", "Коэффициент"),
        ("average", "Среднее значение"),
    ]
    name = models.CharField(max_length=256)
    type = models.CharField(
        max_length=max(len(type[0]) for type in TYPES), choices=TYPES
    )

    def __str__(self) -> str:
        return self.name


class MandatoryPaymentAccrualCalculatorProjectRegion(models.Model):
    mandatory_payment_accrual_calculator = models.ForeignKey(
        MandatoryPaymentAccrualCalculator,
        on_delete=models.CASCADE,
        related_name="mandatory_payment_accrual_calculator_project_regions",
        related_query_name="mandatory_payment_accrual_calculator_project_region",
    )
    project_region = models.ForeignKey(ProjectRegion, on_delete=models.CASCADE)
    coefficient = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MaxValueValidator(101), MinValueValidator(-1)],
        default=0,
    )


class MandatoryPaymentSeizureStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Статус изьятия"
        verbose_name_plural = "Статусы изьятий"


DEFAULT_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME: typing.Final[str] = (
    "Отправлено на первое подтверждение"
)
SENT_FOR_SECOND_CONFIRMATION_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME: typing.Final[
    str
] = "Отправлено на второе подтверждение"
COMPLETED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME: typing.Final[str] = "Подтверждено"
REJECTED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME: typing.Final[str] = "Отклонён"


def default_mandatory_payment_seizure_status() -> MandatoryPaymentSeizureStatus:
    return MandatoryPaymentSeizureStatus.objects.get_or_create(
        name=DEFAULT_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME
    )[0]


def default_mandatory_payment_seizure_status_id() -> int:
    return default_mandatory_payment_seizure_status().id


def sent_for_second_confirmation_mandatory_payment_seizure_status() -> (
    MandatoryPaymentSeizureStatus
):
    return MandatoryPaymentSeizureStatus.objects.get_or_create(
        name=SENT_FOR_SECOND_CONFIRMATION_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME
    )[0]


def completed_mandatory_payment_seizure_status() -> MandatoryPaymentSeizureStatus:
    return MandatoryPaymentSeizureStatus.objects.get_or_create(
        name=COMPLETED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME
    )[0]


def rejected_mandatory_payment_seizure_status() -> MandatoryPaymentSeizureStatus:
    return MandatoryPaymentSeizureStatus.objects.get_or_create(
        name=REJECTED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME
    )[0]


class MandatoryPaymentSeizure(models.Model):
    mandatory_payment = models.ForeignKey(
        "MandatoryPayment",
        on_delete=models.CASCADE,
        related_name="seizures",
        related_query_name="seizure",
    )
    project_region = models.ForeignKey(
        ProjectRegion,
        on_delete=models.CASCADE,
        related_name="mandatory_payment_seizures",
        related_query_name="mandatory_payment_seizure",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mandatory_payment_seizures",
        related_query_name="mandatory_payment_seizure",
    )
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    datetime = models.DateTimeField(default=timezone.now)
    responsible = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="mandatory_payment_seizures",
        related_query_name="mandatory_payment_seizure",
        null=True,
    )
    status = models.ForeignKey(
        MandatoryPaymentSeizureStatus,
        on_delete=models.SET_DEFAULT,
        default=default_mandatory_payment_seizure_status_id,
    )
    imported_from_file = models.BooleanField(default=False)

    def complete(self, *, responsible: User | None = None) -> None:
        self.status = completed_mandatory_payment_seizure_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.MANDATORY_PAYMENT_SEIZURE,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def send_for_second_confirmation(self, *, responsible: User | None = None) -> None:
        self.status = sent_for_second_confirmation_mandatory_payment_seizure_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.MANDATORY_PAYMENT_SEIZURE,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def reject(
        self, *, responsible: User | None = None, reject_comment: str | None = None
    ) -> None:
        self.status = rejected_mandatory_payment_seizure_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.MANDATORY_PAYMENT_SEIZURE,
            rejected_comment=reject_comment,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def is_rejected(self) -> bool:
        return self.status.name == REJECTED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME

    def __str__(self) -> str:
        return f"{self.sum} из {self.account}, {self.datetime}"

    class Meta:
        verbose_name = "Изьятие"
        verbose_name_plural = "Изьятий"
        ordering = ["datetime", "sum"]


class RejectedMandatoryPaymentSeizureStatus(models.Model):
    mandatory_payment_seizure = models.OneToOneField(
        "MandatoryPaymentSeizure",
        null=True,
        on_delete=models.SET_NULL,
        related_name="rejected_mandatory_payment_seizure_status",
    )
    who_rejected = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="+"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(null=True)


class Invoice(models.Model):
    document_basis = models.IntegerField(unique=True)
    date = models.DateField()

    class Meta:
        abstract = True


class UnpaidInvoice(models.Model):
    number = models.IntegerField(unique=True)  # ДО | пример значения: 1254105
    date = models.DateField()  # Дата | пример значения: 19.05.2022
    invoice_number = models.CharField(
        max_length=255, null=True, blank=True
    )  # № счёта | пример значения: 160
    invoice_date = models.DateField()  # Дата счёта | пример значения: 13.05.2022
    project = models.CharField(
        max_length=255, null=True, blank=True
    )  # Проект | пример значения: 7-0197 -Мобайл Телеком - Сервис, ТОО-08-2016
    responsible_user_id = models.CharField(
        max_length=255, null=True, blank=True
    )  # Ответственный | пример значения: 798
    approver = models.CharField(
        max_length=255, null=True, blank=True
    )  # Утвердитель | пример значения: 798 - Маратов Олжас Бауыржанович_СД_798_Инженер проектировщик
    llc = models.CharField(
        max_length=255, null=True, blank=True
    )  # ТОО | пример значения: Аврора Сервис, ТОО
    contractor = models.CharField(
        max_length=255, null=True, blank=True
    )  # Контрагент | пример значения: Hit Market, ИП
    comment = models.TextField(
        null=True, blank=True
    )  # Комментарий | пример значения: Обследование AS5530 счет на 960 000тг, но ДО на 120 000тг
    currency = models.CharField(
        max_length=3, default="KZT", null=True, blank=True
    )  # Валюта | пример значения: KZT
    invoice_category = models.CharField(
        max_length=255, null=True, blank=True
    )  # Категория счёта | пример значения: Обследование
    revenue_expense_articles = models.CharField(
        max_length=255, null=True, blank=True
    )  # Статьи доходов/расходов | пример значения:
    sales_order = models.CharField(
        max_length=255, null=True, blank=True
    )  # Заказ на продажу | пример значения: П-54769-19
    bin_or_iin = models.CharField(
        max_length=12, null=True, blank=True
    )  # БИН/ИИН | пример значения: 881215450978
    iic = models.CharField(
        max_length=24, null=True, blank=True
    )  # Расчетный счет (ИИК) | пример значения: KZ61 6017 1310 0005
    contract_number = models.CharField(
        max_length=36, null=True, blank=True
    )  # Фактический номер договора | пример значения: 8/978
    invoice_amount = models.DecimalField(
        max_digits=25, decimal_places=2, null=True, blank=True
    )  # Сумма по счёту | пример значения: 120000
    paid_amount_1c = models.DecimalField(
        max_digits=25, decimal_places=2, null=True, blank=True
    )  # Оплаченная сумма(1С) | пример значения:
    bank = models.CharField(
        max_length=255, null=True, blank=True
    )  # Банк | пример значения: АО "Народный Банк Казахстана" г. Алматы_HSBKKZKX
    payment_type = models.CharField(
        max_length=255, null=True, blank=True
    )  # ТИП | пример значения: Работы
    status = models.CharField(
        max_length=255, null=True, blank=True
    )  # Статус ДО | пример значения: Исполнен
    creator_user_id = models.CharField(
        max_length=255, null=True, blank=True
    )  # Создатель счёта | пример значения: 21123
    department = models.CharField(
        max_length=255, null=True, blank=True
    )  # Подразделение | пример значения: 7
    due_date = models.DateField(
        null=True, blank=True
    )  # Оплатить до(дата) | пример значения: 13.05.2022
    document_number = models.CharField(
        max_length=255, null=True, blank=True
    )  # Номер документа | пример значения: 314
    document_date = models.CharField(
        null=True, blank=True, max_length=400
    )  # Дата документа | пример значения: 13.05.2022
    document_amount = models.DecimalField(
        max_digits=25, decimal_places=10, null=True, blank=True
    )  # Сумма документа | пример значения: 600000
    closing_document_amount = models.DecimalField(
        max_digits=25, decimal_places=10, null=True, blank=True
    )  # Закрывающий документ представлен на сумму | пример значения: 120000
    work_status = models.CharField(max_length=256, null=True, blank=True)
    payment_destination_code = models.CharField(max_length=36, null=True, blank=True)
    has_in_document_debts = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Неоплаченный счёт"
        verbose_name_plural = "Неоплаченные счёта"
        ordering = ["-date"]

    def __str__(self) -> str:
        return f"{self.number} - {self.date}"

    @property
    def today_exceptions(self) -> QuerySet | None:
        today = timezone.localdate()
        queryset = UnpaidInvoiceException.objects.annotate(
            created_date=TruncDate("created_at")
        ).filter(number=self.number, created_date=today)
        return queryset

    @property
    def has_exception(self) -> bool:
        return self.today_exceptions.exists()

    def create_exception(
        self, creator: User | None = None
    ) -> tuple["UnpaidInvoiceException", bool]:
        today = timezone.localdate()
        return (
            UnpaidInvoiceException.objects.annotate(
                created_date=TruncDate("created_at")
            )
            .filter(created_date=today)
            .get_or_create({"created_by": creator}, number=self.number)
        )

    def delete_today_exceptions(self) -> None:
        self.today_exceptions.delete()

    @property
    def today_paid(self) -> decimal.Decimal:
        today = timezone.localdate()
        return (
            PaidInvoice.objects.exclude(status=rejected_paid_invoice_status())
            .annotate(at_date=TruncDate("at"))
            .filter(
                number=self.number,
                at_date__lte=today,
            )
            .aggregate(sum=Coalesce(Sum("sum"), 0, output_field=DecimalField()))["sum"]
        )

    @property
    def planned_payment(self) -> decimal.Decimal:
        today = timezone.localdate()
        return (
            PaidInvoice.objects.exclude(status=rejected_paid_invoice_status())
            .annotate(at_date=TruncDate("at"))
            .filter(number=self.number, at_date__gt=today)
            .aggregate(sum=Coalesce(Sum("sum"), 0, output_field=DecimalField()))["sum"]
        )

    @property
    def paid(self) -> decimal.Decimal:
        return (self.paid_amount_1c or 0) + self.today_paid + self.planned_payment

    @property
    def remainder(self) -> decimal.Decimal:
        return self.invoice_amount - self.paid

    @property
    def pm_sum(self) -> decimal.Decimal | None:
        try:
            pm_sum = UnpaidInvoicePMSum.objects.get(
                number=self.number, date=timezone.localdate()
            )
        except UnpaidInvoicePMSum.DoesNotExist:
            return None
        else:
            return pm_sum.sum

    @property
    def allowed_payment_percent(self) -> decimal.Decimal:
        if self.has_exception:
            return decimal.Decimal(1)
        elif (
            self.invoice_category
            in (
                "Строительно-монтажные работы",
                "Обследование",
                "Оптика",
                "Электромонтажные работы",
            )
            and self.paid < self.invoice_amount / 2
        ):
            return decimal.Decimal(0.5)
        return decimal.Decimal(1)

    @property
    def allowed_payment_amount(self) -> decimal.Decimal:
        """
        "Можно оплатить" = (
            Тут "можно оплатить" расчитывается таким образом:
                x представлен как "можно оплатить"

                x = "self.invoice_amount" - "self.paid_amount_1c" - "Оплачено сегодня" - "Планируемая оплата"

                если "Закрывающий документ предоставлен на сумму" == "invoice_amount": x = x
                иначе если "Категория счёта" == "Строительно-монтажные работы" или "Категория счёта" == "Обследование":
                    если "Закрывающий документ предоставлен на сумму" больше или равно половины "invoice_amount": x = весь остаток
                    иначе: x = x*0.5 (Половина)
                иначе если "Категория счёта" == "Оптика" или "Категория счёта" == "Электромонтажные работы":
                    если уже оплачено больше 70% надо заплатить остаток: x = весь остаток
                    иначе: x = x*0.7 (70%)

                x = x - Округленный до 2 цифр после запятой
        )

        **Оплачено сегодня** - Надо как то связать "ИмтортТаня03.10" и оттуда брать оплаченные
        **Планируемая оплата** - Надо как то связать "ИмтортТаня03.10" и оттуда брать опланируемые на будущее
        """
        return self.invoice_amount * self.allowed_payment_percent - self.paid

    @property
    def payment_decision(self) -> str:
        if self.has_exception or self.invoice_category == "ТМЦ":
            return "OK"
        if (
            self.invoice_category
            in (
                "Строительно-монтажные работы",
                "Обследование",
                "Оптика",
                "Электромонтажные работы",
            )
            and self.paid >= self.invoice_amount * decimal.Decimal(0.5)
        ) and not self.closing_document_amount:
            return "Предоставьте закрывающий документ!"
        elif self.has_in_document_debts:
            if not self.work_status:
                return "Отказ! Заполнить статус работ"
            elif self.work_status in (
                "завершено (проблемный)",
                "не выполнялось (проблемный)",
            ):
                return "Отказ! проблемный"
        return "OK"

    def is_paid(self) -> bool:
        return not self.remainder

    def paid_as_percent(self) -> decimal.Decimal:
        return round(self.paid / self.invoice_amount * 100, 2)

    def can_pay(self):
        """Можно ли платить или нет. Тут должна быть ранее уазанная операция

        Решение по оплате = (
            Если "Статус работ" не указан = "Отказ! Заполнить статус работ"
            Иначе если "Статус работ" = "завершено (проблемный)" = "Отказ! проблемный"
            Иначе если "Статус работ" = "не выполнялось (проблемный)" = "Отказ! проблемный"
            (Не нужно так как он всегда не заполнен) Иначе если контрагент в стоплисте то = "Стоп лист!"
            Иначе если сумма self.allowed_payment_amount будет больше или равно чем сумма от ПМ то = "ОК"
            Иначе "Изменить сумму!"
        )

        Можно оплатить реестр если Решение по оплате == "OK" иначе нельзя оплачивать
        Статус работ берем из GoogleSheets - https://docs.google.com/spreadsheets/d/1nT3voM4t7BI2NKfotHS1TQqvGmXwuPl3zERE_wGaaw0/edit#gid=0&fvid=1558466895
        """
        return self.payment_decision == "OK"


class UnpaidInvoicePMSum(models.Model):
    number = models.IntegerField()
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    date = models.DateField()


class UnpaidInvoiceException(models.Model):
    number = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UnpaidInvoicesAccessTime(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="unpaid_invoices_access_time",
        related_query_name="unpaid_invoices_access_time",
    )
    updated_at = models.DateField(auto_now=True)
    access_time = models.TimeField(default=datetime.time(hour=16))

    class Meta:
        ordering = ["-access_time", "user"]
        verbose_name = "Время доступа к неоплаченным счетам"


class PaidInvoiceStatus(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Статус оплаченного счета"
        verbose_name_plural = "Статусы оплаченных счетов"


def default_paid_invoice_status() -> PaidInvoiceStatus:
    return PaidInvoiceStatus.objects.get_or_create(name="Отправлен на подтверждение")[0]


def default_paid_invoice_status_id() -> int:
    return default_paid_invoice_status().id


def completed_paid_invoice_status() -> PaidInvoiceStatus:
    return PaidInvoiceStatus.objects.get_or_create(name="Подтверждено")[0]


def rejected_paid_invoice_status() -> PaidInvoiceStatus:
    return PaidInvoiceStatus.objects.get_or_create(name="Отклонено")[0]


#  [MIDDLEWARE]
#  [AUTHENTICATION]
#  [0, 1, 2, 3, 4, 5]

#  [SELECT]


class PaidInvoice(models.Model):
    unpaid_invoice = models.ForeignKey(
        UnpaidInvoice,
        related_name="+",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    number = models.IntegerField()
    date = models.DateField(null=True, blank=True)  # Дата | пример значения: 19.05.2022
    invoice_number = models.CharField(
        max_length=255, null=True, blank=True
    )  # № счёта | пример значения: 160
    invoice_date = models.DateField(
        null=True, blank=True
    )  # Дата счёта | пример значения: 13.05.2022
    project = models.CharField(
        max_length=255, null=True, blank=True
    )  # Проект | пример значения: 7-0197 -Мобайл Телеком - Сервис, ТОО-08-2016
    responsible_user_id = models.CharField(
        max_length=255, null=True, blank=True
    )  # Ответственный | пример значения: 798
    approver = models.CharField(
        max_length=255, null=True, blank=True
    )  # Утвердитель | пример значения: 798 - Маратов Олжас Бауыржанович_СД_798_Инженер проектировщик
    llc = models.CharField(
        max_length=255, null=True, blank=True
    )  # ТОО | пример значения: Аврора Сервис, ТОО
    contractor = models.CharField(
        max_length=255, null=True, blank=True
    )  # Контрагент | пример значения: Hit Market, ИП
    comment = models.TextField(
        null=True, blank=True
    )  # Комментарий | пример значения: Обследование AS5530 счет на 960 000тг, но ДО на 120 000тг
    currency = models.CharField(
        max_length=3, default="KZT", null=True, blank=True
    )  # Валюта | пример значения: KZT
    invoice_category = models.CharField(
        max_length=255, null=True, blank=True
    )  # Категория счёта | пример значения: Обследование
    revenue_expense_articles = models.CharField(
        max_length=255, null=True, blank=True
    )  # Статьи доходов/расходов | пример значения:
    sales_order = models.CharField(
        max_length=255, null=True, blank=True
    )  # Заказ на продажу | пример значения: П-54769-19
    bin_or_iin = models.CharField(
        max_length=12, null=True, blank=True
    )  # БИН/ИИН | пример значения: 881215450978
    document_amount = models.DecimalField(
        max_digits=25, decimal_places=10, null=True, blank=True
    )  # Сумма документа | пример значения: 600000

    iic = models.CharField(
        max_length=24, null=True, blank=True
    )  # Расчетный счет (ИИК) | пример значения: KZ61 6017 1310 0005
    contract_number = models.CharField(
        max_length=10, null=True, blank=True
    )  # Фактический номер договора | пример значения: 8/978
    invoice_amount = models.DecimalField(
        max_digits=25, decimal_places=10, null=True, blank=True
    )  # Сумма по счёту | пример значения: 120000
    paid_amount_1c = models.DecimalField(
        max_digits=25, decimal_places=10, null=True, blank=True
    )  # Оплаченная сумма(1С) | пример значения:
    payment_destination_code = models.CharField(
        max_length=10, null=True, blank=True
    )  # КНП

    paid = models.DecimalField(
        max_digits=25, decimal_places=10, null=True, blank=True
    )  # Оплаченная ранее сумма

    commission = models.DecimalField(max_digits=25, decimal_places=10, default=0)
    commission_date = models.DateField(blank=True, null=True)
    sum = models.DecimalField(
        max_digits=25, decimal_places=10
    )  # Оплачено | Сумма для таблицы
    at = models.DateTimeField(default=timezone.now)  # Дата оплаты
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
    )
    project_region = models.ForeignKey(
        ProjectRegion,
        on_delete=models.CASCADE,
    )  # ПМ

    responsible = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.ForeignKey(
        PaidInvoiceStatus,
        on_delete=models.SET_DEFAULT,
        default=default_paid_invoice_status_id,
    )

    def __str__(self) -> str:
        return f"{self.number}"

    def complete(self, *, responsible: User | None = None) -> None:
        self.status = completed_paid_invoice_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.PAID_INVOICE,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def reject(
        self, *, responsible: User | None = None, reject_comment: str | None = None
    ) -> None:
        self.status = rejected_paid_invoice_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.PAID_INVOICE,
            responsible=responsible,
            status=self.status.name,
            rejected_comment=reject_comment,
        )
        self.save()

    @cached_property
    def binded(self) -> UnpaidInvoice | None:
        return self.unpaid_invoice

    class Meta:
        verbose_name = "Оплаченный счет"
        verbose_name_plural = "Оплаченные счета"


STATUS_CHOICES = (
    ("oncashier", "У кассира, к оплате"),
    ("offcahsier", "Не у кассира"),
)


class Runner(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="offcashier"
    )
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    appointment = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"Бегунок для {self.user.email}"

    class Meta:
        verbose_name = "Бегунок"
        verbose_name_plural = "Бегунки"


class CashRegister(models.Model):
    sum = models.DecimalField(max_digits=25, decimal_places=10, default=0)


class RaschetnyeStatus(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Статус "Расчётные"'
        verbose_name_plural = 'Статусы "Расчётные"'


def default_raschetnye_status() -> RaschetnyeStatus:
    return RaschetnyeStatus.objects.get_or_create(name="не оплачено")[0]


def default_raschetnye_status_id() -> int:
    return default_raschetnye_status().id


def rejected_raschetnye_status() -> RaschetnyeStatus:
    return RaschetnyeStatus.objects.get_or_create(name="отклонено")[0]


def completed_raschetnye_status() -> RaschetnyeStatus:
    return RaschetnyeStatus.objects.get_or_create(name="оплачено")[0]


class Raschetnye(models.Model):
    project_region = models.ForeignKey(
        ProjectRegion, on_delete=models.RESTRICT, related_name="+"
    )
    account = models.ForeignKey(Account, on_delete=models.RESTRICT, related_name="+")

    # subdivision = models.ForeignKey(
    #     Subdivision, on_delete=models.RESTRICT, related_name="+"
    # )
    name = models.CharField(max_length=512)
    layoff_date = models.DateField()
    raschetnye_by_1c = models.DecimalField(max_digits=25, decimal_places=10)
    subreport = models.DecimalField(max_digits=25, decimal_places=10)
    percent_15 = models.DecimalField(max_digits=25, decimal_places=10)
    status = models.ForeignKey(
        RaschetnyeStatus,
        related_name="+",
        on_delete=models.RESTRICT,
        default=default_raschetnye_status_id,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = verbose_name_plural = "Расчётные"


class SutochnyeStatus(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Статус "Суточные"'
        verbose_name_plural = 'Статусы "Суточные"'


def default_sutochnye_status() -> SutochnyeStatus:
    return SutochnyeStatus.objects.get_or_create(name="не оплачено")[0]


def default_sutochnye_status_id() -> int:
    return default_sutochnye_status().id


def rejected_sutochnye_status() -> SutochnyeStatus:
    return SutochnyeStatus.objects.get_or_create(name="отклонено")[0]


def completed_sutochnye_status() -> SutochnyeStatus:
    return SutochnyeStatus.objects.get_or_create(name="подтверждено")[0]


class Sutochnye(models.Model):
    project_region = models.ForeignKey(
        ProjectRegion, on_delete=models.RESTRICT, related_name="+"
    )
    account = models.ForeignKey(Account, on_delete=models.RESTRICT, related_name="+")
    status = models.ForeignKey(
        SutochnyeStatus,
        on_delete=models.RESTRICT,
        related_name="+",
        default=default_sutochnye_status_id,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=512)
    days = models.IntegerField()
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    subdivision = models.ForeignKey(
        Subdivision, on_delete=models.RESTRICT, related_name="+"
    )
    project = models.IntegerField()
    responsible = models.CharField(max_length=512)
    business_trip_start_date = models.DateField()
    business_trip_end_date = models.DateField()
    destination_point = models.TextField()

    def complete(self, *, responsible: User | None = None) -> None:
        self.status = completed_sutochnye_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.SUTOCHNYE,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def reject(
        self, *, responsible: User | None = None, reject_comment: str | None = None
    ) -> None:
        self.status = rejected_sutochnye_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.SUTOCHNYE,
            responsible=responsible,
            status=self.status.name,
            rejected_comment=reject_comment,
        )
        self.save()

    class Meta:
        verbose_name = verbose_name_plural = "Суточные"


class SutochnyeFile(models.Model):
    sutochnye = models.ForeignKey(
        Sutochnye,
        on_delete=models.CASCADE,
        related_name="files",
        related_query_name="file",
    )
    file = models.FileField(upload_to="finance-module/sutochnye-files")

    def __str__(self) -> str:
        return self.file.name

    class Meta:
        verbose_name = "Суточные - файл"
        verbose_name_plural = "Суточные - файлы"


class CHSIGroupStatus(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        verbose_name = 'Статус "Суточные"'
        verbose_name_plural = 'Статусы "Суточные"'


def default_chsi_group_status() -> CHSIGroupStatus:
    return CHSIGroupStatus.objects.get_or_create(name="не оплачено")[0]


def default_chsi_group_status_id() -> int:
    return default_chsi_group_status().id


def rejected_chsi_group_status() -> CHSIGroupStatus:
    return CHSIGroupStatus.objects.get_or_create(name="отклонено")[0]


def completed_chsi_group_status() -> CHSIGroupStatus:
    return CHSIGroupStatus.objects.get_or_create(name="оплачено")[0]


class CHSIGroupManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        queryset = super().get_queryset()
        return queryset.annotate(
            sum=Subquery(
                CHSI.objects.filter(group_id=OuterRef("id"))
                .values("group_id")
                .annotate(total_chsi_sum=Sum("sum"))
                .values("total_chsi_sum")
            )
        )


class CHSIGroup(models.Model):
    project_region = models.ForeignKey(
        ProjectRegion, on_delete=models.RESTRICT, related_name="+"
    )
    account = models.ForeignKey(Account, on_delete=models.RESTRICT, related_name="+")
    status = models.ForeignKey(
        CHSIGroupStatus,
        on_delete=models.RESTRICT,
        related_name="+",
        default=default_chsi_group_status_id,
    )
    date = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = CHSIGroupManager()

    class Meta:
        verbose_name = verbose_name_plural = "Группа ЧСИ"


class CHSI(models.Model):
    group = models.ForeignKey(CHSIGroup, on_delete=models.CASCADE)

    llc = models.CharField(max_length=512)
    recipient = models.CharField(max_length=512)
    bin_or_iin = models.CharField(max_length=12)
    iik = models.CharField(max_length=1024)
    executive_inscription = models.CharField(max_length=512)
    retention_type = models.CharField(max_length=512)
    collaborator = models.CharField(max_length=512)
    iin = models.CharField(max_length=12)
    actual_retention_rate = models.CharField(max_length=128)
    sum = models.DecimalField(max_digits=19, decimal_places=2)
    executive_order_receipt_date = models.DateField(null=True)

    class Meta:
        verbose_name = verbose_name_plural = "ЧСИ"


class StatementReconciliationResult(models.Model):
    created_date = models.DateField()
    date = models.DateField()
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    result = models.JSONField()

    class Meta:
        verbose_name = "Результат сверки"
        verbose_name_plural = "Результаты сверок"
        ordering = ["-created_date"]


# class StatusCategory(models.Model):
#     name = models.CharField(max_length=512)


# class Status(models.Model):
#     state = models.CharField(max_length=128)
#     name = models.CharField(max_length=512)
#     category = models.ForeignKey(StatusCategory, on_delete=models.CASCADE)
class AdministrativeTransferStatus(models.Model):
    name = models.CharField(max_length=512)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Статус "Перевод на АДМ"'
        verbose_name_plural = 'Статусы "Перевод на АДМ"'


def default_administrative_transfer_status() -> AdministrativeTransferStatus:
    return AdministrativeTransferStatus.objects.get_or_create(
        name="Отправлено на подтверждение"
    )[0]


def default_administrative_transfer_status_id() -> int:
    return default_administrative_transfer_status().id


def rejected_administrative_transfer_status() -> AdministrativeTransferStatus:
    return AdministrativeTransferStatus.objects.get_or_create(name="Отклонён")[0]


def completed_administrative_transfer_status() -> AdministrativeTransferStatus:
    return AdministrativeTransferStatus.objects.get_or_create(name="Подтверждено")[0]


class AdministrativeTransfer(models.Model):
    project_region = models.ForeignKey(
        ProjectRegion, on_delete=models.RESTRICT, related_name="+"
    )
    account = models.ForeignKey(Account, on_delete=models.RESTRICT, related_name="+")
    name = models.CharField(max_length=1024)
    sum = models.DecimalField(max_digits=25, decimal_places=10)
    note = models.TextField(null=True)
    status = models.ForeignKey(
        AdministrativeTransferStatus,
        on_delete=models.RESTRICT,
        related_name="+",
        default=default_administrative_transfer_status_id,
    )
    responsible = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    raschetnye = models.ForeignKey(Raschetnye, on_delete=models.CASCADE, null=True)

    def complete(self, *, responsible: User | None = None) -> None:
        self.status = completed_administrative_transfer_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.ADMINISTRATIVE_TRANSFER,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    def reject(
        self, *, responsible: User | None = None, reject_comment: str | None = None
    ) -> None:
        self.status = rejected_administrative_transfer_status()
        PaymentConfirmationHistory.objects.create(
            model_id=self.id,
            model_name=PaymentConfirmationHistory.ModelName.ADMINISTRATIVE_TRANSFER,
            rejected_comment=reject_comment,
            responsible=responsible,
            status=self.status.name,
        )
        self.save()

    class Meta:
        verbose_name = "Перевод на АДМ"
        verbose_name_plural = "Переводы на АДМ"
