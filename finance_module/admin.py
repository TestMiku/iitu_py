import decimal

from django.contrib import admin

from . import models
from .services.interdivisional_debts_service import (
    TemporaryUnpaidInvoice,
    get_balance,
    get_renewable_debt_sum,
)


class SubdivisionModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["name"]


class ProjectRegionModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "project_manager",
        "users_display",
        "balance",
        "subdivision",
    ]
    search_fields = ["name"]

    def balance(self, object: models.ProjectRegion) -> decimal.Decimal:
        return round(get_balance(object), 2)

    def users_display(self, object: models.ProjectRegion) -> str:
        return ", ".join(str(user) for user in object.users.all())


class DebtModelAdmin(admin.ModelAdmin):
    list_display = ["id", "from_whom", "to_whom", "sum"]
    search_fields = ["from_whom", "to_whom"]


class PaidInvoicesModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "approver",
        "balance_due_1c",
        "type",
        "contractor",
        "project",
        "subdivision",
        "account_category",
    ]
    search_fields = ["approver", "type", "contractor", "project"]

@admin.register(models.Inflow)
class InflowModelAdmin(admin.ModelAdmin):
    list_display = ["project_region", "account", "sum"]
    search_fields = ["project_region", "account"]


class RenewableDebtModelAdmin(admin.ModelAdmin):
    list_display = ["id", "from_whom", "to_whom", "renewable_debt_sum_display"]
    search_fields = ["from_whom", "to_whom"]

    def renewable_debt_sum_display(self, object: models.RenewableDebt) -> str:
        try:
            return f"{get_renewable_debt_sum(object):,.2f}".replace(",", " ").replace(
                ".", ","
            )
        except RuntimeError as runtime_error:
            return str(runtime_error)

    renewable_debt_sum_display.short_description = "Renewable Debt Sum"


class MandatoryPaymentAccrualGroupModelAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "mandatory_payment",
        "was_accrued",
        "accrual_amount",
        "datetime",
    ]
    search_fields = ["mandatory_payment__name", "sum"]


admin.site.register(TemporaryUnpaidInvoice, PaidInvoicesModelAdmin)
admin.site.register(models.Account)
admin.site.register(models.Debt, DebtModelAdmin)
admin.site.register(models.RenewableDebt, RenewableDebtModelAdmin)
admin.site.register(models.Subdivision, SubdivisionModelAdmin)
admin.site.register(models.ProjectRegion, ProjectRegionModelAdmin)
admin.site.register(models.MandatoryPayment)
admin.site.register(models.MandatoryPaymentAccrual)
admin.site.register(models.MandatoryPaymentSeizure)
admin.site.register(models.MandatoryPaymentSeizureStatus)
admin.site.register(models.Runner)
admin.site.register(models.UnpaidInvoice)


@admin.register(models.PaidInvoice)
class PaidInvoiceAdmin(admin.ModelAdmin):
    list_display = ["number", "contractor", "sum", "commission", "commission_date", "project_region", "account", "at"]
    search_fields = ["number", "contractor", "at"]
    ordering = ["-at", "-account", "-contractor", "-sum"]


admin.site.register(models.MandatoryPaymentCategory)
admin.site.register(models.Transfer)
admin.site.register(models.AccessToOthersExceptionForProjectManager)
admin.site.register(models.UnpaidInvoiceException)
admin.site.register(models.DebtTranslateGroup)
admin.site.register(models.DebtTranslateGroupStatus)
admin.site.register(models.PaymentConfirmationHistory)
admin.site.register(
    models.MandatoryPaymentAccrualGroup, MandatoryPaymentAccrualGroupModelAdmin
)
admin.site.register(models.TableCellColor)
admin.site.register(models.TableCellColorCategory)
admin.site.register(models.MandatoryPaymentAccrualCalculator)
admin.site.register(models.MandatoryPaymentAccrualCalculatorProjectRegion)
admin.site.register(models.StatementReconciliationResult)
admin.site.register(models.SutochnyeStatus)
admin.site.register(models.Sutochnye)
admin.site.register(models.SutochnyeFile)
admin.site.register(models.AdministrativeTransfer)
admin.site.register(models.AdministrativeTransferStatus)
admin.site.register(models.ProjectRegionApprover)
admin.site.register(models.ProjectRegionApproverProject)
admin.site.register(models.Setoff)
admin.site.register(models.CHSI)
admin.site.register(models.CHSIGroup)
admin.site.register(models.CHSIGroupStatus)
