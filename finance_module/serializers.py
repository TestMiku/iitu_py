import pathlib

from django.contrib.auth import get_user_model
from rest_framework import serializers

from finance_module.services import common_service

from . import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avh_user_id = serializers.ReadOnlyField(source="avh_user_id_from_email")

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "avh_user_id"]


class SubdivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subdivision
        fields = ["id", "name"]


class StatementReconciliationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StatementReconciliationResult
        fields = ["id", "created_date", "date"]


class AccountSerializer(serializers.ModelSerializer):
    subdivision = SubdivisionSerializer()

    class Meta:
        model = models.Account
        fields = ["id", "number", "name", "subdivision", "is_cash_register"]


class AccountWithBalanceSerializer(serializers.ModelSerializer):
    def __init__(self, *args, project_region: models.ProjectRegion, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._project_region = project_region

    class Meta:
        model = models.Account
        fields = ["id", "name"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["balance"] = common_service.get_account_balance(
            instance, self._project_region
        )
        return representation


class UnpaidInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UnpaidInvoice
        fields = [
            "id",
            "number",
            "date",
            "invoice_number",
            "invoice_date",
            "project",
            "responsible_user_id",
            "approver",
            "llc",
            "contractor",
            "comment",
            "currency",
            "invoice_category",
            "revenue_expense_articles",
            "sales_order",
            "bin_or_iin",
            "iic",
            "contract_number",
            "invoice_amount",
            "paid_amount_1c",
            "bank",
            "payment_type",
            "status",
            "pm_sum",
            "creator_user_id",
            "department",
            "due_date",
            "document_number",
            "document_date",
            "document_amount",
            "closing_document_amount",
            "work_status",
            "paid",
            "remainder",
            "today_paid",
            "allowed_payment_amount",
            "payment_decision",
            "is_paid",
            "paid_as_percent",
            "can_pay",
            "has_exception",
            "payment_destination_code",
        ]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class DirectorWithBalanceSerializer(serializers.ModelSerializer):
    def __init__(self, *args, user: User, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._user: User = user

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["balance"] = common_service.get_director_balance(
            instance, self._user
        )
        return representation


class ProjectRegionWithBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectRegion
        fields = ["id", "name"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["balance"] = common_service.get_project_region_balance(instance)
        return representation


class ProjectRegionApproverProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectRegionApproverProject
        fields = ["number"]


class ProjectRegionApproverSerializer(serializers.ModelSerializer):
    projects = ProjectRegionApproverProjectSerializer(many=True)
    user = UserSerializer()

    class Meta:
        model = models.ProjectRegionApprover
        fields = ["user", "projects"]


class ProjectRegionSerializer(serializers.ModelSerializer):
    subdivision = SubdivisionSerializer()
    approvers = ProjectRegionApproverSerializer(many=True)

    class Meta:
        model = models.ProjectRegion
        fields = [
            "id",
            "name",
            "director_display",
            "manager_display",
            "project_manager_display",
            "subdivision",
            "percent",
            "approvers",
        ]


class MandatoryPaymentAccrualCalculatorProjectRegionSerializer(
    serializers.ModelSerializer
):
    project_region = ProjectRegionSerializer()

    class Meta:
        model = models.MandatoryPaymentAccrualCalculatorProjectRegion
        fields = ["project_region", "coefficient"]


class MandatoryPaymentAccrualCalculatorSerializer(serializers.ModelSerializer):
    mandatory_payment_accrual_calculator_project_regions = (
        MandatoryPaymentAccrualCalculatorProjectRegionSerializer(many=True)
    )

    class Meta:
        model = models.MandatoryPaymentAccrualCalculator
        fields = [
            "mandatory_payment_accrual_calculator_project_regions",
            "name",
            "type",
        ]


class MandatoryPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MandatoryPayment
        fields = ["id", "deadline_template", "name", "get_short_deadline_template"]


class MandatoryPaymentSeizureStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MandatoryPaymentSeizureStatus
        fields = ["id", "name"]


class MandatoryPaymentSeizureSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    project_region = ProjectRegionSerializer()
    responsible = UserSerializer()
    mandatory_payment = MandatoryPaymentSerializer()
    sum = serializers.FloatField()
    status = MandatoryPaymentSeizureStatusSerializer()

    class Meta:
        model = models.MandatoryPaymentSeizure
        fields = [
            "id",
            "sum",
            "account",
            "mandatory_payment",
            "project_region",
            "datetime",
            "responsible",
            "status",
        ]


class PaidInvoiceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaidInvoiceStatus
        fields = ["id", "name"]


class PaidInvoiceSerializer(serializers.ModelSerializer):
    project_region = ProjectRegionSerializer()
    account = AccountSerializer()
    status = PaidInvoiceStatusSerializer()

    class Meta:
        model = models.PaidInvoice
        fields = [
            "id",
            "number",
            "date",
            "project_region",
            "invoice_number",
            "invoice_date",
            "project",
            "responsible_user_id",
            "approver",
            "llc",
            "contractor",
            "comment",
            "currency",
            "invoice_category",
            "revenue_expense_articles",
            "sales_order",
            "bin_or_iin",
            "document_amount",
            "account",
            "iic",
            "contract_number",
            "invoice_amount",
            "paid_amount_1c",
            "payment_destination_code",
            "paid",
            "sum",
            "commission",
            "at",
            "status",
        ]


class DebtTranslateGroupStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DebtTranslateGroupStatus
        fields = ["id", "name"]


class DebtSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, object: models.Debt) -> str | None:
        return (
            object.group.status.name if object.group and object.group.status else None
        )

    from_whom_project_manager = serializers.SerializerMethodField()

    def get_from_whom_project_manager(self, object: models.Debt) -> str | None:
        from_whom = object.from_whom_as_project_region
        return (
            f"{from_whom.project_manager.last_name} {from_whom.project_manager.first_name}"
            if from_whom and from_whom.project_manager
            else None
        )

    from_whom_director = serializers.SerializerMethodField()

    def get_from_whom_director(self, object: models.Debt) -> str | None:
        from_whom = object.from_whom_as_project_region
        return (
            f"{from_whom.director.last_name} {from_whom.director.first_name}"
            if from_whom and from_whom.director
            else None
        )

    to_whom_project_manager = serializers.SerializerMethodField()

    def get_to_whom_project_manager(self, object: models.Debt) -> str | None:
        to_whom = object.to_whom_as_project_region
        return (
            f"{to_whom.project_manager.last_name} {to_whom.project_manager.first_name}"
            if to_whom and to_whom.project_manager
            else None
        )

    to_whom_director = serializers.SerializerMethodField()

    def get_to_whom_director(self, object: models.Debt) -> str | None:
        to_whom = object.to_whom_as_project_region
        return (
            f"{to_whom.director.last_name} {to_whom.director.first_name}"
            if to_whom and to_whom.director
            else None
        )

    class Meta:
        model = models.Debt
        fields = [
            "from_whom",
            "from_whom_project_manager",
            "from_whom_director",
            "to_whom",
            "to_whom_project_manager",
            "to_whom_director",
            "sum",
            "datetime",
            "status",
        ]


class DebtTranslateGroupSerializer(serializers.ModelSerializer):
    from_account = AccountSerializer()
    to_account = AccountSerializer()
    status = DebtTranslateGroupStatusSerializer()
    debts = DebtSerializer(many=True)
    responsible = UserSerializer()

    class Meta:
        model = models.DebtTranslateGroup
        fields = [
            "id",
            "from_whom",
            "to_whom",
            "from_account",
            "responsible",
            "to_account",
            "sum",
            "datetime",
            "status",
            "debts",
            "type",
        ]


class InflowSerializer(serializers.ModelSerializer):
    project_region = ProjectRegionSerializer()
    account = AccountSerializer()
    remainder = serializers.DecimalField(max_digits=19, decimal_places=2)
    reserve = serializers.DecimalField(max_digits=19, decimal_places=2)

    class Meta:
        model = models.Inflow
        fields = [
            "project_region",
            "account",
            "date",
            "sum",
            "remainder",
            "reserve",
            "reserve_percent",
        ]


class SutochnyeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SutochnyeStatus
        fields = ["id", "name"]


class SutochnyeFileSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = models.SutochnyeFile
        fields = ["file"]

    def to_representation(self, instance: models.SutochnyeFile):
        representation = super().to_representation(instance)
        file = {
            "url": representation.pop("file"),
            "size": instance.file.size,
            "name": pathlib.Path(instance.file.name).name,
        }
        representation["file"] = file
        return representation


class SutochnyeSerializer(serializers.ModelSerializer):
    project_region = ProjectRegionSerializer()
    account = AccountSerializer()
    subdivision = SubdivisionSerializer()
    status = SutochnyeStatusSerializer()
    files = SutochnyeFileSerilaizer(many=True)

    class Meta:
        model = models.Sutochnye
        fields = [
            "id",
            "project_region",
            "account",
            "subdivision",
            "name",
            "days",
            "sum",
            "project",
            "responsible",
            "business_trip_start_date",
            "business_trip_end_date",
            "destination_point",
            "status",
            "files",
            "created_at",
        ]


class TransferStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TransferStatus
        fields = ["id", "name"]


class TransferSerializer(serializers.ModelSerializer):
    from_whom = ProjectRegionSerializer()
    to_whom = ProjectRegionSerializer()
    responsible = UserSerializer()
    from_account = AccountSerializer()
    to_account = AccountSerializer()
    status = TransferStatusSerializer()

    class Meta:
        model = models.Transfer
        fields = [
            "id",
            "to_whom",
            "from_whom",
            "responsible",
            "from_account",
            "to_account",
            "sum",
            "datetime",
            "status",
        ]


class PaymentConfirmationSerializer(serializers.ModelSerializer):
    responsible = UserSerializer()

    class Meta:
        model = models.PaymentConfirmationHistory
        fields = [
            "model_name",
            "model_id",
            "rejected_comment",
            "status",
            "responsible",
            "created_at",
        ]


class AdministrativeTransferStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdministrativeTransferStatus
        fields = ["name"]


class AdministrativeTransferSerializer(serializers.ModelSerializer):
    project_region = ProjectRegionSerializer()
    account = AccountSerializer()
    status = AdministrativeTransferStatusSerializer()
    responsible = UserSerializer()

    class Meta:
        model = models.AdministrativeTransfer
        fields = [
            "id",
            "project_region",
            "account",
            "sum",
            "created_at",
            "note",
            "status",
            "responsible",
            "name",
        ]


class CHSISerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CHSI
        fields = [
            "llc",
            "recipient",
            "bin_or_iin",
            "iik",
            "executive_inscription",
            "retention_type",
            "collaborator",
            "iin",
            "actual_retention_rate",
            "sum",
            "executive_order_receipt_date",
        ]


class CHSIGroupStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CHSIGroupStatus
        fields = ["name"]


class CHSIGroupSerializer(serializers.ModelSerializer):
    project_region = ProjectRegionSerializer()
    account = AccountSerializer()
    chsi_set = CHSISerializer(many=True)
    status = CHSIGroupStatusSerializer()
    sum = serializers.DecimalField(max_digits=25, decimal_places=10)

    class Meta:
        model = models.CHSIGroup
        fields = ["id", "project_region", "account", "sum", "chsi_set", "status"]


class RaschetnyeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RaschetnyeStatus
        fields = ["name"]


class RaschetnyeSerializer(serializers.ModelSerializer):
    project_region = ProjectRegionSerializer()
    account = AccountSerializer()
    status = RaschetnyeStatusSerializer()

    class Meta:
        model = models.Raschetnye
        fields = [
            "name",
            "layoff_date",
            "raschetnye_by_1c",
            "subreport",
            "percent_15",
            "created_at",
            "account",
            "status",
            "project_region"
        ]
