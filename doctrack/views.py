from datetime import time
import json

import pytz
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from doctrack import services
from doctrack.models import *

from .forms import (
    ChangeStatusForm,
    DTCommentForm,
    DTDocumentEditForm,
    DTDocumentForm,
    DTDocumentFormSet,
    DTRequestFilterForm,
    DTRequestForm,
)
from .services import get_formatted_date


# Список всех функции
#    - Таблица для просмотра данных
#        - Пагинация
#        - Поиск
#        - Фильтр
#        - Сортировка
#        - Редактирование таблицы
#             - Последовательность столбцов
#             - Скрыть/показать столбец


# - Таблица для просмотра данных


@login_required
def index(request):
    dt_requests = DTRequest.objects.filter(is_deleted=False)
    filter_form = DTRequestFilterForm(request.GET)

    # Фильтрация по удаленным
    if (is_deleted := request.GET.get("filter_by_is_deleted")) and is_deleted == "on":
        dt_requests = DTRequest.objects.filter(is_deleted=True)

    if "filter_by_created_at_from" in request.GET and request.GET["filter_by_created_at_from"]:
        created_at_from = datetime.strptime(request.GET["filter_by_created_at_from"], "%Y-%m-%d").date()
        created_at_from = datetime.combine(created_at_from, time.min)
        dt_requests = dt_requests.filter(created_at__gte=created_at_from)

    if "filter_by_created_at_to" in request.GET and request.GET["filter_by_created_at_to"]:
        created_at_to = datetime.strptime(request.GET["filter_by_created_at_to"], "%Y-%m-%d").date()
        created_at_to = datetime.combine(created_at_to, time.max)
        dt_requests = dt_requests.filter(created_at__lte=created_at_to)

    if "filter_by_updated_at_from" in request.GET and request.GET["filter_by_updated_at_from"]:
        updated_at_from = datetime.strptime(request.GET["filter_by_updated_at_from"], "%Y-%m-%d").date()
        updated_at_from = datetime.combine(updated_at_from, time.min)
        dt_requests = dt_requests.filter(modified_at__gte=updated_at_from)

    if "filter_by_updated_at_to" in request.GET and request.GET["filter_by_updated_at_to"]:
        updated_at_to = datetime.strptime(request.GET["filter_by_updated_at_to"], "%Y-%m-%d").date()
        updated_at_to = datetime.combine(updated_at_to, time.max)
        dt_requests = dt_requests.filter(modified_at__lte=updated_at_to)

    if "filter_by_order_date_from" in request.GET and request.GET["filter_by_order_date_from"]:
        order_date_from = datetime.strptime(request.GET["filter_by_order_date_from"], "%Y-%m-%d").date()
        dt_requests = dt_requests.filter(order_date__gte=order_date_from)

    if "filter_by_order_date_to" in request.GET and request.GET["filter_by_order_date_to"]:
        order_date_to = datetime.strptime(request.GET["filter_by_order_date_to"], "%Y-%m-%d").date()
        dt_requests = dt_requests.filter(order_date__lte=order_date_to)

    # Фильтрация по частичному выполнению
    if "filter_by_is_partial" in request.GET and request.GET["filter_by_is_partial"]:
        is_partial = True if request.GET.get("filter_by_is_partial") == 'on' else False
        dt_requests = dt_requests.filter(is_partial=is_partial)

    if filter_form.is_valid():

        region_filter = filter_form.cleaned_data.get('filter_by_region')
        project_filter = filter_form.cleaned_data.get('filter_by_project')
        work_type_filter = filter_form.cleaned_data.get('filter_by_work_type')
        status_filter = filter_form.cleaned_data.get('filter_by_status')

        if region_filter:
            dt_requests = dt_requests.filter(region__in=region_filter)
        if project_filter:
            dt_requests = dt_requests.filter(project__in=project_filter)
        if work_type_filter:
            dt_requests = dt_requests.filter(work_type__in=work_type_filter)
        if status_filter:
            dt_requests = dt_requests.filter(status__in=status_filter)

    # Поиск
    if "search" in request.GET and request.GET["search"]:
        search_query = request.GET["search"]
        dt_requests = dt_requests.filter(
            Q(region__name__icontains=search_query)
            | Q(work_type__name__icontains=search_query)
            | Q(status__name__icontains=search_query)
            | Q(order_bs_name__icontains=search_query)
            | Q(order_number__icontains=search_query)
            | Q(dtdocuments__file__icontains=search_query)
            | Q(dtdocuments__document_type__name__icontains=search_query)
            | Q(dtdocuments__status__icontains=search_query)
        )
        if dt_requests:
            dt_requests = dt_requests.distinct()

    # Сортировка
    if "sorted_by" in request.GET and request.GET["sorted_by"]:
        sorted_field = request.GET["sorted_by"]
        dt_requests = dt_requests.order_by(sorted_field)

    # Пагинация
    page_number = int(request.GET.get("page", 1))
    
    paginator = Paginator(dt_requests, 20)  # По 20 элементов на страницу
    try:
        dt_requests = paginator.page(page_number)
    except PageNotAnInteger:
        dt_requests = paginator.page(1)
    except EmptyPage:
        dt_requests = paginator.page(paginator.num_pages)

    if request.GET.get("request_id", False):
        dt_requests = DTRequest.objects.filter(id=request.GET.get("request_id"))

    context = {
        "requests": dt_requests,
        "paginator": paginator,
        "page_number": page_number,
        "prev_page_number": page_number - 1,
        "next_page_number": page_number + 1,

        'filter_form': filter_form,
        
        "regions": DTRegion.objects.all(),
        "work_types": DTWorkType.objects.all()
    }

    return render(request, "doctrack/index.html", context)


# @login_required
def change_status(request, request_pk):
    """Меняет этап заявки. Админу можно менять на любой статус. Если не админ то по условию"""

    dt_request = DTRequest.objects.get(pk=request_pk)
    if request.method == "POST":
        form = ChangeStatusForm(request.POST, instance=dt_request)
        if form.is_valid():
            dt_request.status = form.cleaned_data["status"]
            dt_request.save(request=request)
            return redirect("doctrack")
    else:
        form = ChangeStatusForm(instance=dt_request)

    statuses, can_change_status = services.can_change_status(request, dt_request)
    return render(
        request,
        "doctrack/change_status.html",
        {
            "form": form,
            "add_navbar": True,
            "statuses": statuses,
            "request": dt_request,
            "can_change_status": can_change_status,
        },
    )


@login_required
def request_info(request, pk):
    dt_request = DTRequest.objects.get(pk=pk)
    statuses, can_change_status = services.can_change_status(request, dt_request)

    can_update_documents = False
    user_group = services.get_user_group(request.user)
    if user_group and dt_request.status in user_group.available_statuses.all() or request.user.is_superuser:
        can_update_documents = True

    if request.method == 'POST':
        form = DTCommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('request_info', pk=dt_request.pk)
            
    comment_form = DTCommentForm()

    context = {
        "request": dt_request,
        "add_navbar": True,
        "can_change_status": can_change_status,
        "can_update_documents": can_update_documents,
        "comment_form": comment_form,
        "doc_types": DTDocumentType.objects.filter(work_type=dt_request.work_type),
        "can_view_documents": services.can_view_documents(request),
    }

    return render(request, "doctrack/info.html", context)


@login_required
@require_POST
def change_document_status(request, pk):
    data = json.loads(request.body.decode("utf-8"))
    documents = data.get("documents", [])
    request_status = data.get("request_status")
    dt_request = DTRequest.objects.all()

    if not dt_request:
        return JsonResponse({"error": "Заявка не найдена"}, status=404)

    dt_request = dt_request.filter(pk=pk).first()
    if request_status == -1 or request_status == 0:
        for document in documents:
            if document and document["status"]:
                dt_document = DTDocument.objects.get(pk=document["id"])
                dt_document.status = document["status"]
                dt_document.save(user=request.user)

                if document["comment"]:
                    DTComment.objects.create(
                        entity="DTDocument",
                        entity_id=document["id"],
                        user=request.user,
                        comment=document["comment"],
                    )
        return JsonResponse({"message": "Изменен статус документа"}, status=200)

    if request_status > 0:
        new_status = DTStatus.objects.filter(pk=request_status).first()
        if new_status and new_status != dt_request.status:
            dt_request.status = new_status
            dt_request.save()
            DTCounter.objects.create(
                entity='DTRequest', entity_id=dt_request.pk, author=request.user, event=f"Статус изменен на {dt_request.status.name}"

            )

            if new_status.send_mail:
                dt_request.send_email()

            return JsonResponse({"message": "Изменен этап"}, status=200)

    return JsonResponse({"message": "Не удалось сохранить"}, status=200)


@login_required
def get_date_current_status(request, request_pk, status_id):
    dt_request = DTRequest.objects.get(pk=request_pk)
    changed_at = get_formatted_date(dt_request.modified_at)
    return JsonResponse({"date": changed_at}, status=200)


@login_required
def is_rejected_status(request, request_pk, status_id):
    dt_request = DTRequest.objects.get(pk=request_pk)
    status = DTStatus.objects.get(pk=status_id)
    if dt_request.status != status:
        if 'корректировка' in status.name.lower() and 'техдок' in status.name.lower():
            return JsonResponse({"is_rejected": True}, status=200)

    return JsonResponse({"is_rejected": False}, status=200)


def comment_for_rejected_order(request, request_pk):
    dt_request = DTRequest.objects.get(pk=request_pk)
    if request.method == "POST":
        data = json.loads(request.body)
        comment = data.get('comment', '')
        if comment:
            try:
                with transaction.atomic():
                    dt_request.rejected_comment = comment
                    dt_request.save()

                    DTComment.objects.create(
                        entity="DTRequest",
                        entity_id=request_pk,
                        user=request.user,
                        comment=comment,
                    )

                    return JsonResponse({"message": "Комментарий сохранен"}, status=200)
            except Exception as e:
                return JsonResponse({"message": f"Ошибка: {e}"}, status=400)

    return JsonResponse({"message": "Не удалось сохранить комментарий"}, status=400)


@login_required
def update_documents(request, id):
    dt_request = DTRequest.objects.get(pk=id)

    if request.method == "POST":
        request_form = DTRequestForm(request.POST, instance=dt_request)
        document_formset = DTDocumentFormSet(
            request.POST, request.FILES, instance=dt_request
        )

        if request_form.is_valid() and document_formset.is_valid():
            request_form.save()
            document_formset.save()
            return redirect(
                "dtrequest_list"
            )  # перенаправляем пользователя на список запросов
    else:
        document_formset = DTDocumentFormSet(instance=dt_request)

    context = {"document_formset": document_formset}
    return render(request, "doctrack/edit.html", context)


@login_required
def add_document(request, request_id):
    dt_request = DTRequest.objects.get(pk=request_id)
    if request.method == "POST":
        form = DTDocumentForm(request.POST, request.FILES)
        files = request.FILES.getlist("file")
        print(files)

        if form.is_valid():
            document_type = form.cleaned_data["document_type"]
            for file in files:
                dt_document = DTDocument(
                    document_type=document_type, file=file, request=dt_request
                )
                dt_document.save()

            return HttpResponse('<h1>Сохранено</h1>')
    else:
        form = DTDocumentForm()
    return render(
        request,
        "doctrack/add_document.html",
        {
            "form": form,
            "add_navbar": True,
            "add_footer": True,
            "request": dt_request,
            "doc_types": DTDocumentType.objects.filter(work_type=dt_request.work_type),
        },
    )


def add_document_request(request, request_id):
    dt_request = DTRequest.objects.get(pk=request_id)
    if request.method == "POST":
        document_type = request.POST.get("document_type")
        files = request.FILES.getlist("file")
        doc_type = DTDocumentType.objects.get(pk=int(document_type))

        for file in files:
            dt_document = DTDocument(
                document_type=doc_type, file=file, request=dt_request
            )
            dt_document.save()

        return JsonResponse({"message": "Документ добавлен", "status": 200})

    return JsonResponse({"message": "Не удалось добавить документ"}, status=400)


@login_required
def update_document(request, request_id, document_id):
    dt_request = DTRequest.objects.get(pk=request_id)
    dt_document = DTDocument.objects.get(pk=document_id)
    if request.method == "POST":
        form = DTDocumentEditForm(request.POST, request.FILES, instance=dt_document)
        if form.is_valid():
            form.save()
            dt_document = DTDocument.objects.get(pk=document_id)
            dt_document.status = "in_process"
            dt_document.save()

            return HttpResponse(
                "<h1>Сохранено</h1>"
            )  # Перенаправляем пользователя на страницу успешного сохранения
    else:
        form = DTDocumentEditForm(instance=dt_document)
    file_name = dt_document.file.name.split("/")[-1]
    return render(
        request,
        "doctrack/edit_document.html",
        {
            "form": form,
            "add_navbar": True,
            "add_footer": True,
            "request": dt_request,
            "file_name": file_name,
        },
    )


@login_required
def delete_document(request, document_id):
    dt_document = DTDocument.objects.get(pk=document_id)
    dt_document.delete()
    return redirect(f"/mp/doctrack/info/{dt_document.request.id}")


@login_required
def request_update(request, id):
    if request.method == "POST":
        form = DTRequestForm(request.POST, instance=DTRequest.objects.get(pk=id))
        if form.is_valid():
            form.save()
            return redirect("request_info", id)
    form = DTRequestForm(instance=DTRequest.objects.get(pk=id))
    return render(request, "doctrack/edit.html", {
        "request_form" : form,
        "add_navbar": True,
        "add_footer": True
    })


@login_required
def request_add(request):
    if request.method == "POST":
        form = DTRequestForm(request.POST)
        if form.is_valid():
            # Убедитесь, что значение поля status предоставлено в форме
            status_id = DTStatus.objects.all().first().id
            form.instance.status_id = status_id
            form.instance.creator = request.user
            form.save()
            id = form.instance.id

            request = DTRequest.objects.get(pk=id)
            pm = DTProjectRegion.objects.get(
                project=form.cleaned_data["project"],
                region=form.cleaned_data["region"],
            ).users

            subject = f"Новая заявка №{id}"
            message = f"<strong style='font-size: 18px;'>Системное уведомление портала https://portal.avh.kz/mp/doctrack/?request_id={id}</strong><br><br>" + \
                f"<strong style='font-size: 16px;'>Заявка №{id} создана</strong><br>" + \
                f"<br>Название Базовой станций: {form.cleaned_data['order_bs_name']}" + \
                f"<br>Номер заказа: {form.cleaned_data['order_number']}" + \
                f"<br>Вид работ: {request.work_type}" + \
                f"<br>Регион: {request.region}" + \
                f"<br>Проект: {request.project}" + \
                f"<br>Дата создания: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            emails_to_send = [user.email for user in pm.all()]

            send_mail(
                subject=subject,
                message=message,
                from_email="portal@avh.kz",
                recipient_list=emails_to_send,
                html_message=message,
            )

            return redirect("request_info", id)
    else:
        form = DTRequestForm()

    return render(
        request,
        "doctrack/add.html",
        {
            "form": form,
            "add_navbar": True,
            "add_footer": True,
            "projects": DTProject.objects.all(),
            "work_types": DTWorkType.objects.all(),
            "regions": DTRegion.objects.all().order_by("name"),
            "statuses": DTStatus.objects.all(),
        },
)


@login_required
def request_delete(request, pk):
    dt_request = DTRequest.objects.get(pk=pk)
    dt_request.is_deleted = True
    dt_request.save()
    return redirect(f"/mp/doctrack/info/{pk}")


@login_required
def request_restore(request, pk):
    dt_request = DTRequest.objects.get(pk=pk)
    dt_request.is_deleted = False
    print(dt_request.is_deleted)
    dt_request.save()
    return redirect(f"/mp/doctrack/info/{pk}")


@login_required
def unsubscribe(request, request_pk):
    user = request.user
    dt_request = DTRequest.objects.get(pk=request_pk)
    if user in dt_request.subscribers.all():
        dt_request.subscribers.remove(user)
        dt_request.save()
    return redirect(f"/mp/doctrack/info/{request_pk}")


@login_required
def subscribe(request, request_pk):
    user = request.user
    dt_request = DTRequest.objects.get(pk=request_pk)
    if user not in dt_request.subscribers.all():
        dt_request.subscribers.add(user)
        dt_request.save()
    return redirect(f"/mp/doctrack/info/{request_pk}")


def change_type_work(request):
    data = {
        "Монтажные работы": [
            "АТП и акт монтажа в PDF",
            "АТП и акт монтажа в WORD",
            "Заявки в формате PDF",
            "Накладная на перемещение в Excel",
            "Накладная на перемещение в PDF",
            "АПП в PDF",
            "АПП в WORD",
            "Письмо согласования накладных и АПП",
            "Письмо согласования проекта",
            "Письмо принятия Листа согласования",
            "Письмо согласования гарантийного письма"
        ],
        "Строительные работы": [
            "АТП в PDF",
            "АТП в WORD",
            "Письмо принятия фотоотчета",
            "Письмо согласования проекта",
            "Письмо согласования рабочего проекта",
            "Письмо принятия Листа согласования",
            "Письмо согласования СЗ",
            "Письмо согласования о частичном закрытии",
            "Накладная на перемещение в Excel",
            "Накладная на перемещение в PDF",
            "АПП в PDF",
            "АПП в WORD",
            "Письмо о принятии накладных",
            "Письмо согласования гарантийного письма"
        ],
        "Электромонтажные работы": [
            "АТП в PDF",
            "АТП в WORD",
            "Письмо согласования фотоотчета ЭМР",
            "АПП в PDF",
            "АПП в WORD"
        ],
        "Демонтаж (ЭМР)": [
            "АТП (pdf)",
            "АТП (word)",
            "Письмо согласование ЭМР",
            "АПП (pdf, jpeg, png)"
        ],
        "Демонтаж (СР)": [
            "АТП (pdf)",
            "АТП (word)",
            "Накладная на перемещение в Excel",
            "Накладная на перемещение в PDF",
            "АПП (pdf, jpeg, png)",
            "АПП в WORD (1-5шт)",
            "Письмо согласования накладных и АПП"
        ],
        "Демонтаж (МР)": [
            "АТП в PDF",
            "АТП в WORD",
            "Накладная на перемещение в Excel (1-12шт)",
            "Накладная на перемещение в PDF(1-12шт)",
            "АПП в PDF(1-5шт)",
            "АПП в WORD (1-5шт)",
            "Письмо согласования накладных и АПП (1-10шт)"
        ]
    }

    try:
        with transaction.atomic():
            for work_type in data:
                DTDocumentType.objects.filter(work_type=DTWorkType.objects.get(name=work_type)).delete()

            for work_type in data:
                for document_type in data[work_type]:
                    work_type_obj = DTWorkType.objects.get(name=work_type)
                    DTDocumentType.objects.create(name=document_type, work_type=DTWorkType.objects.get(name=work_type))
    except Exception as e:
        return HttpResponse(f"Ошибка: {e}")

    return HttpResponse("ok")
