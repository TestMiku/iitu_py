import datetime
import decimal
import typing

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404, HttpRequest, HttpResponse
from django.utils import timezone
from django.views import generic

from finance_module.services import mandatory_payments_service
from main.models import AvhUser

from .. import models, services
from .accrual_unload_service import unloading_accrual
from .serzure_unload_service import unloading_seizure


class CreaetAccessToOthersExceptionForProjectManagerTemplateView(generic.TemplateView):
    template_name = "finance_module/mandatory_payments/create_access_to_others_exception_for_project_manager.html"

    def get_context_data(self, **kwargs):
        today = timezone.localdate()
        return super().get_context_data(
            project_managers=AvhUser.objects.filter(
                id__in=models.ProjectRegion.objects.values_list(
                    "users__id", flat=True
                ).distinct()
            ),
            create_access_to_others_exception_for_project_managers=models.AccessToOthersExceptionForProjectManager.objects.filter(
                datetime__year=today.year, datetime__month=today.month, datetime__day=today.day
            ),
            **kwargs,
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        post_type = request.POST.get("post-type")
        if post_type == "create-access-to-others-exception-for-project-manager":
            project_manager_id = request.POST.get("project-manager-id")
            project_manager = AvhUser.objects.get(id=project_manager_id)
            today = timezone.localdate()
            if not models.AccessToOthersExceptionForProjectManager.objects.filter(
                project_manager=project_manager, datetime__year=today.year, datetime__month=today.month, datetime__day=today.day
            ).exists():
                models.AccessToOthersExceptionForProjectManager.objects.create(
                    project_manager=project_manager, created_by=request.user
                )
        else:
            raise Http404
        return self.get(request)


class ImportMandatoryPaymentsTemplateView(generic.TemplateView):
    template_name = "finance_module/mandatory_payments/import_mandatory_payments.html"

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        file = self.request.FILES.get("file")
        mandatory_payments_service.import_mandatory_payments(
            bytes_io=file,
            import_mandatory_payment_accruals=request.POST.get(
                "import-mandatory-payment-accruals"
            )
            == "on",
            import_mandatory_payment_seizures=request.POST.get(
                "import-mandatory-payment-seizures"
            )
            == "on",
        )
        return self.get(request)


class AccrualCalculatorTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "finance_module/mandatory_payments/accrual_calculator.html"

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        return super().get_context_data(
            mandatory_payments=models.MandatoryPayment.objects.all(),
            project_regions=models.ProjectRegion.objects.all(),
            mandatory_payment_accrual_calculators=models.MandatoryPaymentAccrualCalculator.objects.all(),
            **kwargs,
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        mandatory_payment_id = request.POST.get("mandatory-payment-id")
        mandatory_payment = None
        if mandatory_payment_id:
            mandatory_payment = models.MandatoryPayment.objects.get(
                id=mandatory_payment_id
            )
        mandatory_payment_accrual_calculator_id = request.POST.get(
            "mandatory-payment-accrual-calculator-id"
        )
        mandatory_payment_accrual_calculator = None
        if mandatory_payment_accrual_calculator_id:
            try:
                mandatory_payment_accrual_calculator = (
                    models.MandatoryPaymentAccrualCalculator.objects.get(
                        id=mandatory_payment_accrual_calculator_id
                    )
                )
            except models.MandatoryPaymentAccrualCalculator.DoesNotExist:
                pass

        mandatory_payment_accrual_calculator_name = request.POST.get(
            "mandatory-payment-accrual-calculator-name"
        )
        mandatory_payment_accrual_calculator_type = request.POST.get(
            "mandatory-payment-accrual-calculator-type"
        )

        try:
            if mandatory_payment_accrual_calculator:
                mandatory_payment_accrual_calculator.name = (
                    mandatory_payment_accrual_calculator_name
                )
            else:
                mandatory_payment_accrual_calculator = (
                    models.MandatoryPaymentAccrualCalculator.objects.get(
                        name=mandatory_payment_accrual_calculator_name
                    )
                )
            mandatory_payment_accrual_calculator.type = (
                mandatory_payment_accrual_calculator_type
            )
            mandatory_payment_accrual_calculator.mandatory_payment_accrual_calculator_project_regions.all().delete()
        except models.MandatoryPaymentAccrualCalculator.DoesNotExist:
            mandatory_payment_accrual_calculator = (
                models.MandatoryPaymentAccrualCalculator(
                    name=mandatory_payment_accrual_calculator_name,
                    type=mandatory_payment_accrual_calculator_type,
                )
            )

        mandatory_payment_accrual_calculator_project_regions = []
        mandatory_payment_accruals = []
        mandatory_payment_accrual_group = None
        for coefficient, project_region_id, sum in zip(
            request.POST.getlist("coefficient"),
            request.POST.getlist("project-region-id"),
            request.POST.getlist("sum"),
        ):
            project_region = models.ProjectRegion.objects.get(id=project_region_id)
            mandatory_payment_accrual_calculator_project_regions.append(
                models.MandatoryPaymentAccrualCalculatorProjectRegion(
                    mandatory_payment_accrual_calculator=mandatory_payment_accrual_calculator,
                    project_region=project_region,
                    coefficient=coefficient,
                )
            )
            if mandatory_payment and sum and (sum := decimal.Decimal(sum)):
                if not mandatory_payment_accrual_group:
                    mandatory_payment_accrual_group = (
                        models.MandatoryPaymentAccrualGroup(
                            mandatory_payment=mandatory_payment,
                            accrual_amount=request.POST.get("total-sum"),
                            was_accrued=sum,
                            responsible=request.user,
                        )
                    )
                else:
                    mandatory_payment_accrual_group.was_accrued += sum
                mandatory_payment_accruals.append(
                    models.MandatoryPaymentAccrual(
                        sum=sum,
                        project_region=project_region,
                        mandatory_payment=mandatory_payment,
                        deadline=mandatory_payment.get_deadline(timezone.localdate()),
                        group=mandatory_payment_accrual_group,
                    )
                )
        mandatory_payment_accrual_group.save()
        mandatory_payment_accrual_calculator.save()
        models.MandatoryPaymentAccrualCalculatorProjectRegion.objects.bulk_create(
            mandatory_payment_accrual_calculator_project_regions
        )
        models.MandatoryPaymentAccrual.objects.bulk_create(mandatory_payment_accruals)
        return self.get(request)


class UnloadingMandatoryPaymentsListView(generic.ListView):
    model = models.MandatoryPayment
    template_name = (
        "finance_module/mandatory_payments/unloading_mandatory_payments.html"
    )

    def get_queryset(self):
        return models.MandatoryPayment.objects.filter(
            mandatory_payment_accrual__deadline__gte=timezone.localdate()
        )

    def get(self, request, *args, **kwargs):
        accrual = request.GET.get("accrual")
        seizure = request.GET.get("seizure")

        if accrual == "":
            file = unloading_accrual()
            return FileResponse(file, filename="unloading_paid.xlsx")
        elif seizure == "":
            file = unloading_seizure()
            return FileResponse(file, filename="unloading_logistic.xlsx")

        return super().get(request, *args, **kwargs)


class ListTemplateView(generic.TemplateView):
    template_name = "finance_module/mandatory_payments/list.html"

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        return super().get_context_data(
            deadline_templates=models.MandatoryPayment.objects.exclude(
                deadline_template__isnull=True
            )
            .values_list("deadline_template", flat=True)
            .distinct(),
            categories=models.MandatoryPaymentCategory.objects.all(),
            mandatory_payments=models.MandatoryPayment.objects.all(),
            **kwargs,
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        post_type = request.POST.get("post-type")
        if post_type == "create-mandatory-payment":
            name = request.POST.get("name")
            monthly_payments = decimal.Decimal(request.POST.get("monthly-payments", 0))
            category_id = request.POST.get("category-id")
            category = None
            if category_id:
                category = models.MandatoryPaymentCategory.objects.get(id=category_id)
            deadline_template = request.POST.get("deadline-template")
            models.MandatoryPayment.objects.create(
                name=name,
                deadline_template=deadline_template,
                monthly_payments=monthly_payments,
                category=category,
                exception=request.POST.get("exception") == "on"
            )
        elif post_type == "delete-mandatory-payment":
            id = request.POST.get("id")
            models.MandatoryPayment.objects.get(id=id).delete()
        else:
            raise Http404
        return self.get(request)
