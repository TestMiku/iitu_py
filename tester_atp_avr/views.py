import pathlib
import time
import traceback
import uuid

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from reporter.models import Report

from . import forms, services
from .models import ContratcNumberAndDate, TCPCategory, TCPFile, WorkType
from .services import (
    get_tables_as_html_from_docx,
    get_tables_as_html_from_pdf,
    get_tables_as_html_from_excel,
    parse_html_table,
    parse_html_table_test,
    get_values_from_pdf_text,
    load_tcp,
    calculate_additional_data

)


@method_decorator(csrf_exempt, name="dispatch")
class ATPAVRFormView(generic.TemplateView):
    template_name = "p1/tester_atp_avr/form.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            **kwargs,
            tcp_files=TCPFile.objects.all(),
            contract_number_and_dates=ContratcNumberAndDate.objects.all(),
            work_types=WorkType.objects.all(),
        )

    def post(self, request, *args, **kwargs) -> JsonResponse:
        electro_montazh = bool(int(self.request.POST.get("electro_montazh")))

        bs_order = self.request.POST.get("bs_order")
        bs_date = self.request.POST.get("bs_date")
        bs_number = self.request.POST.get("bs_number")
        bs_name = self.request.POST.get("bs_name")
        bs1_name = self.request.POST.get("bs1_name")
        bs_address = self.request.POST.get("bs_address")

        contract_number_and_date = self.request.POST.get("contract_number_and_date")
        work_type = self.request.POST.get("work_type")

        akt_montaz = services.get_tables_as_list(
            self.request.POST.get("akt_montaz_input")
        )
        akt_montaz2 = services.get_tables_as_list(
            self.request.POST.get("akt_montaz2_input")
        )
        akt_montaz1 = services.get_tables_as_list(
            self.request.POST.get("akt_montaz1_input")
        )

        smeta_value = self.request.POST.get("id_smeta_input")
        try:
            smeta_value = request.FILES["smeta_input"]
        except KeyError:
            pass
        smeta = services.get_tables_as_list_smeta(smeta_value)
        if not electro_montazh:
            atp_rows, atp_errors = services.validate_atp(self.request.POST.get("atp"))
            avr_rows, avr_errors = services.validate_avr(self.request.POST.get("avr"))
            if atp_errors or avr_errors:
                return JsonResponse(
                    {"errors": [], "atp": atp_errors, "avr": avr_errors}, status=400
                )
            difference_sum = self.request.POST.get("difference-sum")
            difference_sum = float(difference_sum) if difference_sum else None



            try:
                urls = services.ComparerAndProcessor(
                    bs_order=bs_order,
                    bs_date=bs_date,
                    bs_number=bs_number,
                    bs_name=bs_name,
                    bs1_name=bs1_name,
                    akt_montaz=akt_montaz,
                    akt_montaz1=akt_montaz1,
                    akt_montaz2=akt_montaz2,
                    smeta=smeta,
                    contract_number_and_date=contract_number_and_date,
                    work_type=work_type,
                    avr_rows=avr_rows,
                    atp_rows=atp_rows,
                    difference_sum=difference_sum,
                    output_path=pathlib.Path("p1")
                    / (
                        str(self.request.user)
                        if self.request.user.is_authenticated
                        else str(uuid.uuid4())
                    ),
                ).compare_and_process()

                Report.objects.create(text=f'https://portal.avh.kz{urls["html"]}',process="tester-atp-avr - Создание документов",responsible=request.user)
            except Exception as exception:
                return JsonResponse(
                    {"errors": [str(exception)], "atp": [], "avr": []}, status=400
                )
            return JsonResponse(urls)
        else:
            # try:
            avr_html = self.request.POST.get("avr")
            avr_materials_html = self.request.POST.get("avr-materials")
            avr=parse_html_table_test(avr_html)
            avr_materials=parse_html_table_test(avr_materials_html)
            total_work,total_materials,total_overall,total_vat,total_with_vat = calculate_additional_data(avr_work=avr, avr_materials=avr_materials)
            print("total_work",total_work)
            print("total_materials",total_materials)
            print("total_overall",total_overall)
            print("total_vat",total_vat)
            print("total_with_vat",total_with_vat)
            from num2words import num2words
            context = {
                "bs_order": bs_order,
                "bs_date": bs_date,
                "contract_number_and_date": contract_number_and_date,
                "bs_name": bs_name,
                "bs_address":bs_address,
                "rows_work": avr,
                "total_work": "{:,.2f}".format(total_work).replace(',', ' ').replace('.', ','),
                "rows_materials": avr_materials,
                "total_materials": "{:,.2f}".format(total_materials).replace(',', ' ').replace('.', ','),
                "total_overall": "{:,.2f}".format(total_overall).replace(',', ' ').replace('.', ','),
                "total_vat": "{:,.2f}".format(total_vat).replace(',', ' ').replace('.', ','),
                "total_with_vat": "{:,.2f}".format(total_with_vat).replace(',', ' ').replace('.', ','),
                "total_with_vat_str": num2words(int(total_with_vat), lang='ru'),
            }

            processor = services.WordTemplateProcessor(output_path=pathlib.Path("p1") / (
                str(self.request.user) if self.request.user.is_authenticated else str(uuid.uuid4())
            ))
            urls = processor.process_template(context)
            # except:
            #     return JsonResponse(
            #         {"errors": [], "atp": [], "avr": ["убедитесь что все таблицы выделены"]}, status=400
            #     )
            return JsonResponse(urls, status=200)

class TCPFileForm(generic.CreateView):
    form_class = forms.TCPFileForm
    template_name = "p1/tester_atp_avr/load_tcp.html"
    success_url = reverse_lazy("tester-atp-avr:atp-avr-form")

    def form_valid(self, form):
        response = super().form_valid(form)
        try:
            load_tcp(self.object, form.cleaned_data["price_column"])
        except services.LoadTCPError as error:
            form.add_error(None, f"Не удалось загрузить цены ТЦП: {error}")
        except Exception as exception:
            form.add_error(None, f"Неизвестная ошибка: {exception}")
        else:
            return response
        self.object.delete()
        self.extra_context = {"form": form}
        return self.get(self.request)


class TCPFileList(generic.ListView):
    template_name = "p1/tester_atp_avr/tcps.html"
    queryset = TCPFile.objects.all()


@require_POST
@csrf_exempt
def get_tables_as_html(request: HttpRequest) -> JsonResponse:
    file = request.FILES.get("file")
    id_ = "tables-" + str(time.time_ns())
    if file is None:
        return JsonResponse({"detail": _("Вы должны передать файл")}, status=400)
    if file.content_type == "application/pdf":
        tables, text = get_tables_as_html_from_pdf(
            file, line_scale=int(request.POST.get("line-scale", "54"))
        )

        additional_values = {}
        try:
            # Additional values
            additional_values = get_values_from_pdf_text(" ".join(text.strip().split()))
        except:
            traceback.print_exc()

        if tables is None:
            return JsonResponse(
                {
                    "detail": _(
                        "Таблица не найдена, возможно у таблицы нету четких границ."
                    )
                },
                status=400,
            )

        return JsonResponse(
            {"id": id_, "tables": tables, "additional_values": additional_values}
        )

    elif (
        file.content_type
        == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ):
        tables, text = get_tables_as_html_from_docx(
            file, line_scale=int(request.POST.get("line-scale", "54"))
        )

        additional_values = {}
        try:
            # Additional values
            additional_values = get_values_from_pdf_text(" ".join(text.strip().split()))
        except:
            traceback.print_exc()

        if tables is None:
            return JsonResponse(
                {
                    "detail": _(
                        "Таблица не найдена, возможно у таблицы нету четких границ."
                    )
                },
                status=400,
            )

        return JsonResponse(
            {"id": id_, "tables": tables, "additional_values": additional_values}
        )
    elif file.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        try:
            from tempfile import NamedTemporaryFile
            with NamedTemporaryFile(delete=False, suffix='.xlsx') as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name

            tables, numbered_data, additional_data = get_tables_as_html_from_excel(temp_file_path)

            if not tables:
                return JsonResponse(
                    {"detail": _("Таблица не найдена, возможно у таблицы нету четких границ.")},
                    status=400,
                )

            return JsonResponse({"id": id_, "tables": tables})
        except Exception as e:
            return JsonResponse({"detail": _("Ошибка при обработке файла")}, status=500)

    return JsonResponse(
        {
            "detail": _("Такой тип файлов не поддерживается")
            + f", content_type: {file.content_type}"
        },
        status=400,
    )


@require_GET
@csrf_exempt
def get_tcps(request: HttpRequest) -> JsonResponse:
    if "pk" not in request.GET:
        return JsonResponse({"detail": _("Нужно указать pk")}, status=400)
    tcp_category = get_object_or_404(TCPCategory, pk=request.GET["pk"])
    return JsonResponse(
        [
            dict(
                id=tcp.id,
                tcpId=tcp.tcp_id,
                tcpCategoryId=tcp_category.tcp_category_id,
                name=tcp.name,
                price=tcp.price,
                measuringUnit=tcp.measuring_unit,
            )
            for tcp in tcp_category.tcp_set.all()
        ],
        safe=False,
    )


@require_GET
@csrf_exempt
def get_tcp_categories(request: HttpRequest) -> JsonResponse:
    if "pk" not in request.GET:
        return JsonResponse({"detail": _("Нужно указать pk")}, status=400)
    tcp_file = get_object_or_404(TCPFile, pk=request.GET["pk"])
    return JsonResponse(
        [
            dict(
                id=tcp_category.id,
                tcpCategoryId=tcp_category.tcp_category_id,
                name=tcp_category.name,
            )
            for tcp_category in tcp_file.tcpcategory_set.all()
        ],
        safe=False,
    )


def create_form(request, form_class: WorkType | ContratcNumberAndDate, pk=None):
    if request.method == "POST":
        name = request.POST.get("name")
        if pk:
            obj = form_class.objects.get(pk=pk)
            obj.name = name
            obj.save()
            return {
                "redirect": "/p1/tester-atp-avr/list-wt"
                if form_class == WorkType
                else "/p1/tester-atp-avr/list-cnd",
                "obj": obj,
            }
        else:
            obj = form_class.objects.create(name=name)
            obj.save()
            return {
                "redirect": "/p1/tester-atp-avr/list-wt"
                if form_class == WorkType
                else "/p1/tester-atp-avr/list-cnd",
                "obj": obj,
            }

    context = {
        "redirect": False,
        "page_name": f"Изменить договор id:{pk}" if pk else "Добавить договор",
        "back_page_url": "/p1/tester-atp-avr/list-cnd",
        "obj": form_class.objects.get(pk=pk) if pk else None,
    }

    if form_class == WorkType:
        context = {
            "redirect": False,
            "page_name": f"Изменить тип работы id:{pk}"
            if pk
            else "Добавить тип работы",
            "back_page_url": "/p1/tester-atp-avr/list-wt",
            "obj": form_class.objects.get(pk=pk) if pk else None,
        }

    return context


def add_wt(request):
    context = create_form(request, WorkType)
    if context["redirect"]:
        return redirect(context["redirect"])
    return render(request, "p1/tester_atp_avr/add.html", context)


def add_cnd(request):
    context = create_form(request, ContratcNumberAndDate)
    if context["redirect"]:
        return redirect(context["redirect"])
    return render(request, "p1/tester_atp_avr/add.html", context)


def edit_wt(request, pk):
    context = create_form(request, WorkType, pk)
    if context["redirect"]:
        return redirect(context["redirect"])
    return render(request, "p1/tester_atp_avr/add.html", context)


def edit_cnd(request, pk):
    context = create_form(request, ContratcNumberAndDate, pk)
    if context["redirect"]:
        return redirect(context["redirect"])
    return render(request, "p1/tester_atp_avr/add.html", context)


def list_wt(request):
    context = {
        "obj_list": WorkType.objects.all(),
        "obj_url": "/p1/tester-atp-avr/edit-wt/",
        "add_url": "/p1/tester-atp-avr/add-wt",
        "page_name": "Список типов работы",
    }
    return render(request, "p1/tester_atp_avr/list.html", context)


def list_cnd(request):
    context = {
        "obj_list": ContratcNumberAndDate.objects.all(),
        "obj_url": "/p1/tester-atp-avr/edit-cnd/",
        "add_url": "/p1/tester-atp-avr/add-cnd",
        "page_name": "Список договоров",
    }
    return render(request, "p1/tester_atp_avr/list.html", context)


def del_wt(request, pk):
    obj = WorkType.objects.get(pk=pk)
    obj.delete()
    return redirect("/p1/tester-atp-avr/list-wt")


def del_cnd(request, pk):
    obj = ContratcNumberAndDate.objects.get(pk=pk)
    obj.delete()
    return redirect("/p1/tester-atp-avr/list-cnd")
