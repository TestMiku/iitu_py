from datetime import datetime, timedelta

import colorfield
from django.apps import apps
from django.contrib import admin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from main.models import AvhObject, AvhUser


class DoctrackModel(AvhObject):
    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def get_record_data(self, *args, **kwargs):
        return self.__class__.__name__, self.pk

    def get_comments(self):
        comments = DTComment.objects.filter(
            entity=self.__class__.__name__, entity_id=self.pk
        )
        if comments:
            return comments
        return ["Без комментариев"]

    def get_first_comment(self):
        comments = DTComment.objects.filter(
            entity=self.__class__.__name__, entity_id=self.pk
        )
        if comments:
            return comments.first().comment
        return ""

    def get_last_comment(self):
        comments = DTComment.objects.filter(
            entity=self.__class__.__name__, entity_id=self.pk
        )
        if comments:
            return comments.last()
        return "Без комментариев"
    
    def get_first_comment(self):
        comments = DTComment.objects.filter(
            entity=self.__class__.__name__, entity_id=self.pk
        )
        if comments:
            return comments.first().comment
        return ""

    class Meta:
        abstract = True


class DTCounter(models.Model):
    entity = models.CharField(_("Сущность"), max_length=256)
    entity_id = models.PositiveIntegerField(_("ID сущности"))
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.CharField(_("Событие"), max_length=256)
    author = models.CharField(_("Автор"), max_length=250)

    global_search_fields = ('event', 'author')

    def __str__(self) -> str:
        return f"{self.entity}#{self.entity_id}: {self.event}"


class DTProject(DoctrackModel):
    name = models.CharField(_("Имя"), max_length=256, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Проект")
        verbose_name_plural = _("1. Проекты")


class DTRegion(DoctrackModel):
    name = models.CharField(_("Имя"), max_length=256, unique=True)

    global_search_fields = ('name',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Регион")
        verbose_name_plural = _("2. Регионы")


class DTProjectRegion(DoctrackModel):
    project = models.ForeignKey(
        "doctrack.DTProject",
        on_delete=models.CASCADE,
        related_name="dtproject_projects",
        verbose_name=_("Проект"),
    )
    region = models.ForeignKey(
        "doctrack.DTRegion",
        on_delete=models.CASCADE,
        related_name="dtproject_regions",
        verbose_name=_("Регион"),
    )
    users = models.ManyToManyField(
        "main.AvhUser",
        verbose_name=_("Пользователи кому отправляются письма на почту"),
        related_name="dtproject_regions",
        blank=True,
    )

    def __str__(self):
        return f"{self.project} - {self.region}"

    class Meta:
        verbose_name = _("РегионПроект")
        verbose_name_plural = _("3. РегионПроекты")


class DTFileType(DoctrackModel):
    name = models.CharField(_("Имя"), max_length=256)

    global_search_fields = ('name',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Тип файла")
        verbose_name_plural = _("Типы файлов")


class DTWorkType(DoctrackModel):
    name = models.CharField(_("Имя"), max_length=256, unique=True)
    project = models.ForeignKey(
        "doctrack.DTProject", on_delete=models.CASCADE, related_name="dtwork_types"
    )

    global_search_fields = ('name',)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Вид работ")
        verbose_name_plural = _("6. Виды работ")


class DTDocumentType(DoctrackModel):
    name = models.CharField(_("Имя"), max_length=256)
    work_type = models.ForeignKey(
        "doctrack.DTWorkType", on_delete=models.CASCADE, related_name="dtdocument_types"
    )
    available_file_types = models.ManyToManyField(
        "doctrack.DTFileType",
        verbose_name=_("Типы файлов"),
        related_name="dtdocument_types",
        blank=True,
    )
    is_required = models.BooleanField(default=False)

    global_search_fields = ('name',)

    def get_file_types(self):
        text = ", ".join([file_type.name for file_type in self.available_file_types.all()])
        return text if text else ""

    def __str__(self):
        if self.is_required:
            return f"{self.name} (Обязательный) ({self.work_type})"

        return f"{self.name}"

    class Meta:
        verbose_name = _("Тип документа")
        verbose_name_plural = _("7. Типы документов")
        ordering = ["name"]


document_status_choices = (
    ("new", "Новый"),
    ("in_process", "Обработано"),
    ("rejected", "Отклонен"),
    ("accepted", "Принято"),
    ("accepted_by_client", "Принято клиентом"),
)


class DTDocument(DoctrackModel):
    request = models.ForeignKey(
        "doctrack.DTRequest", on_delete=models.CASCADE, related_name="dtdocuments"
    )
    document_type = models.ForeignKey(
        "doctrack.DTDocumentType",
        on_delete=models.CASCADE,
        related_name="dtdocument_types",
    )
    status = models.CharField(
        _("Статус"), max_length=256, choices=document_status_choices, default="new"
    )
    file = models.FileField(
        _("Файл"), upload_to="doctrack/documents", blank=True, null=True, max_length=1000
    )

    global_search_fields = ('status',)

    def save(self, user=None, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == "rejected" and user is not None:
            DTRejectedDocument.objects.create(
                document=self,
                reason="",
                author=user,
            )

    @property
    def status_text(self):
        return dict(document_status_choices)[self.status]

    @property
    def status_color(self):
        colors = {
            "new": "#bfc7ff",
            "rejected": "#ff6c6c",
            "in_process": "#bfc7ff",
            "accepted": "#a4ff6c",
            "accepted_by_client": "#00c049",
        }
        return colors[self.status]

    def __str__(self):
        if self.file:
            return f"{self.file.name.split('/')[-1]}"
        return f"{self.document_type.name}"

    class Meta:
        verbose_name = _("Документ")
        verbose_name_plural = _("9. Документы")


class DTGroup(DoctrackModel):
    name = models.CharField(_("Название отдела"), max_length=50)
    avh_role = models.ManyToManyField(
        "main.AvhRole", verbose_name=_("Роль"), related_name="dtgroups", blank=True
    )
    available_statuses = models.ManyToManyField(
        "doctrack.DTStatus",
        verbose_name=_("Статусы на котором можно редактировать документы"),
        related_name="dtgroups",
        blank=True,
    )

    global_search_fields = ('name',)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Отдел")
        verbose_name_plural = _("4. Отделы")


class DTStatus(DoctrackModel):
    name = models.CharField(_("Имя"), max_length=256, unique=True)
    color = colorfield.fields.ColorField(default="#fff")

    groups = models.ManyToManyField(
        "doctrack.DTGroup", verbose_name=_("Отделы"), related_name="dtstatus"
    )
    next = models.ManyToManyField(
        "self", blank=True, symmetrical=False, verbose_name=_("Следующие статусы"), related_name="dtstatus_previous"
    )
    previous = models.ManyToManyField(
        "self", blank=True, symmetrical=False, verbose_name=_("Предыдущие статусы"), related_name="dtstatus_next"
    )

    send_mail = models.BooleanField(
        _("Отправлять письмо при переходе на данный этап"),
        default=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Статус")
        verbose_name_plural = _("5. Статусы")
        ordering = ["id"]


class DTStatusChangeHistory(DoctrackModel):
    request = models.ForeignKey(
        "doctrack.DTRequest",
        verbose_name=_("Заявка"),
        on_delete=models.CASCADE,
        related_name="dtstatus_change_histories",
    )
    status = models.ForeignKey(
        "doctrack.DTStatus",
        verbose_name=_("Статус"),
        on_delete=models.CASCADE,
        related_name="dtstatus_change_histories",
    )
    author = models.ForeignKey(
        "main.AvhUser",
        verbose_name=_("Автор"),
        on_delete=models.CASCADE,
        related_name="dtstatus_change_histories",
    )
    changed_at = models.DateTimeField(_("Дата изменения"), auto_now_add=True)

    def __str__(self):
        return f"{self.request} - {self.status}"

    class Meta:
        verbose_name = _("История изменения статуса")
        verbose_name_plural = _("11. История изменения статусов")
        ordering = ["-created_at"]


class DTRejectedDocument(DoctrackModel):
    document = models.ForeignKey(
        "doctrack.DTDocument",
        verbose_name=_("Документ"),
        on_delete=models.CASCADE,
        related_name="dtrejected_documents",
    )
    reason = models.TextField(_("Причина отклонения"))
    author = models.ForeignKey(
        "main.AvhUser",
        verbose_name=_("Автор"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="dtrejected_documents",
    )
    rejected_at = models.DateTimeField(_("Дата отклонения"), auto_now_add=True)

    global_search_fields = ('reason',)

    def __str__(self):
        return f"{self.document} - {self.reason}"

    class Meta:
        verbose_name = _("Отклоненный документ")
        verbose_name_plural = _("10. Отклоненные документы")
        ordering = ["-rejected_at"]


class DTRequest(DoctrackModel):
    region = models.ForeignKey(
        "doctrack.DTRegion",
        verbose_name=_("Регион"),
        on_delete=models.CASCADE,
        related_name="dtrequests",
    )
    project = models.ForeignKey(
        "doctrack.DTProject",
        verbose_name=_("Проект"),
        on_delete=models.CASCADE,
        related_name="dtrequests",
        blank=True,
        null=True,
    )
    work_type = models.ForeignKey(
        "doctrack.DTWorkType",
        verbose_name=_("Вид работ"),
        on_delete=models.CASCADE,
        related_name="dtrequests",
    )
    status = models.ForeignKey(
        "doctrack.DTStatus",
        verbose_name=_("Статус"),
        on_delete=models.CASCADE,
        related_name="dtrequests",
    )
    creator = models.ForeignKey(
        "main.AvhUser",
        verbose_name=_("Создатель"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="dtrequests",
    )

    is_partial = models.BooleanField(_("Частичное закрытие"), default=False)

    order_bs_name = models.CharField(
        _("Название базовой станции"), max_length=255, blank=True, null=True
    )
    order_number = models.CharField(
        _("Номер заказа"), max_length=255, blank=True, null=True
    )
    order_date = models.DateField(_("Дата заказа"), blank=True, null=True)
    comment = models.TextField(
        _("Комментарий при создании заявки"), blank=True, null=True
    )
    rejected_comment = models.TextField(
        _("Причина отклонения"), blank=True, null=True
    )

    subscribers = models.ManyToManyField(
        "main.AvhUser",
        verbose_name=_("Пользователи кому отправляются письма"),
        related_name="subscribe_dtrequests",
        blank=True,
        symmetrical=False,
    )

    global_search_fields = ('order_bs_name', 'order_number', 'order_date', 'comment', 'rejected_comment')

    history = HistoricalRecords()



    def __str__(self):

        name = f"Заявка#{self.pk}"
        if self.is_deleted:
            name = f"⟳ {name}"
        return name

    def get_order_creator(self):
        try:
            return self.creator.get_name
        except:
            return ""

    def get_bs(self):
        order_number = f"№{self.order_number} " if self.order_number else ""
        return f"{self.order_bs_name} {order_number}от {self.get_order_date_format()}"

    def order_date_format(self):
        order_date_formatted = self.created_at.strftime("%d.%m.%Y")
        order_date_encoded = order_date_formatted.encode("utf-16le")
        return order_date_encoded.decode("utf-16le")

    def get_order_date_format(self):
        order_date_formatted = self.order_date.strftime("%d.%m.%Y")
        order_date_encoded = order_date_formatted.encode("utf-16le")
        return order_date_encoded.decode("utf-16le")

    def save(self, *args, **kwargs):
        author = "Anonymous"  # Значение по умолчанию

        # Проверяем, есть ли 'request' в аргументах
        if "request" in kwargs:
            request = kwargs.pop("request")
            # Проверяем, аутентифицирован ли пользователь
            if request.user.is_authenticated:
                author = request.user

        old_status = None
        if self.pk:
            old_instance = DTRequest.objects.get(pk=self.pk)
            old_status = old_instance.status

        super().save(*args, **kwargs)
        if old_status != self.status:
            DTCounter.objects.create(
                entity=self.__class__.__name__,
                entity_id=self.pk,
                event=f"new status {self.status}",
                author=author,
            )

        subject = f"{self.status.name} №{self.pk}"
        message = f'<strong style="font-size: 18px;">Системное уведомление портала https://portal.avh.kz/mp/doctrack/?request_id={self.pk}</strong><br><br>' + \
            f"БС {self.order_bs_name} №{self.order_number} от {self.order_date_format()} статус изменен на {self.status.name} <br><br> " + \
            f"что бы посмотреть подробности нажмите <a href='https://portal.avh.kz/mp/doctrack/?request_id={self.pk}'>ссылку</a>"
        
        author_email = None
        if author.__class__ == AvhUser:
            author_email = author.email

        emails_to_send = [] 
        subscribers = self.subscribers.all()
        if subscribers:
            for subscriber in subscribers:
                if author_email != subscriber.email:
                    emails_to_send.append(subscriber.email)
                    
        if emails_to_send:
            send_mail(
                subject,
                message,
                "portal@avh.kz",
                emails_to_send,
                html_message=message,
            )

    def is_have_documents(self):
        documents = DTDocument.objects.filter(request=self.pk)
        if documents:
            return True
        return False

    def get_number_of_adjustments(self):
        counter = DTCounter.objects.filter(
            entity="DTRequest", entity_id=self.pk, event="new status Корректировка (ТехДок)"
        ).count()
        return counter

    def get_rejection_reason(self):
        documents = DTDocument.objects.filter(request=self.pk)
        if documents:
            return documents.last().get_last_comment()
        return ""

    def get_documents_by_type(self) -> list:
        document_types = self.work_type.dtdocument_types.all().order_by("id")
        print(document_types)
        result = []

        for document_type in document_types:
            documents = DTDocument.objects.filter(request=self.pk, document_type=document_type)
            result.append({
                "type": document_type,
                "documents": documents,
            })

        return result

    def send_email(self):
        subject = f"{self.status.name} №{self.pk}"
        message = f'<strong style="font-size: 18px;">Системное уведомление портала https://portal.avh.kz/mp/doctrack/?request_id={self.pk}</strong><br><br>' + \
            f"К закрытию {self.work_type.name} БС {self.order_bs_name} №{self.order_number} от {self.order_date_format()}"
        
        emails_to_send = [] 
        project_regions = DTProjectRegion.objects.filter(
            project=self.project,
            region=self.region,
        )
        if project_regions:
            for project_region in project_regions:
                users = project_region.users.all()
                if users:
                    for user in users:
                        emails_to_send.append(user.email)
        if emails_to_send:
            send_mail(
                subject,
                message,
                "portal@avh.kz",
                emails_to_send,
                html_message=message,
            )

        return True

    def get_file_statuses(self):
        all_statuses = DTDocument.objects.filter(request=self.pk).values("status").distinct()

        return all_statuses

    class Meta:
        verbose_name = _("Заявка")
        verbose_name_plural = _("8. Заявки")
        ordering = ["-created_at"]


class DTComment(DoctrackModel):
    entity = models.CharField(_("Сущность (class_name)"), max_length=50)
    entity_id = models.IntegerField(_("ID сущности"))

    attached_entity = models.CharField(
        _("Прикрепленная сущность (class_name)"), max_length=50, null=True, blank=True
    )
    attached_entity_id = models.IntegerField(
        _("ID прикрепленной сущности"), null=True, blank=True
    )

    user = models.ForeignKey(AvhUser, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()

    global_search_fields = ('comment',)

    def is_last_5(self):
        comments = DTComment.objects.filter(
            entity=self.entity, entity_id=self.entity_id
        )
        if comments and len(comments) > 5:
            return self in comments[:5]
        return True

    @property
    def created_at_utc_64(self):
        original_time = self.created_at
        original_time_utc = original_time.astimezone(timezone.utc)
        adjusted_time_utc = original_time_utc + timedelta(hours=6)

        return adjusted_time_utc

    def get_date(self):
        return format_date_as_condition(self.created_at_utc_64)

    def __str__(self):
        entity_info = ""
        if self.attached_entity and self.attached_entity_id:
            attached_entity = get_entity_by_id(
                self.attached_entity, self.attached_entity_id
            )
            entity_info = f" (Прикреплено к {attached_entity})"
        if self.user:
            try:
                return f"{self.user.get_name} {format_date_as_condition(self.created_at)}: {self.comment}{entity_info}"
            except:
                pass
        return f"Anonimous User {format_date_as_condition(self.created_at)}: {self.comment}{entity_info}"

    def get_comment_text_preview(self):
        try:
            return f"{self.comment[:20]}..."
        except:
            return f"{self.comment}"

    def get_comment_text(self):
        entity_info = ""
        if self.attached_entity and self.attached_entity_id:
            attached_entity: DTDocument = get_entity_by_id(
                self.attached_entity, self.attached_entity_id
            )
            if attached_entity.document_type:
                entity_info = f"{attached_entity.document_type.name}: "
        return f"{entity_info}{self.comment}"

    def get_attached_entity(self):
        if self.attached_entity and self.attached_entity_id:
            return get_entity_by_id(self.attached_entity, self.attached_entity_id)
        return None

    def get_attached_comment(self):
        if (
            self.attached_entity
            and self.attached_entity_id
            and self.attached_entity == "DTComment"
        ):
            attached_comment = get_entity_by_id(
                self.attached_entity, self.attached_entity_id
            )
            if attached_comment:
                return attached_comment
        return None

    def save(self, *args, **kwargs):
        res = super().save(*args, **kwargs)
        print("savenator")
        if self.attached_entity == "DTComment" and self.attached_entity_id:
            print("savenator")
            attached_comment = get_entity_by_id(self.attached_entity, self.attached_entity_id)
            entity = get_entity_by_id(self.entity, self.entity_id)
            if attached_comment.user != self.user and attached_comment.user.send_notifications_to_email:
                print("savenator")
                subject='Новый комментарий на портале AVH',
                message=f'',
                message = f'<strong style="font-size: 18px;">Системное уведомление портала https://portal.avh.kz/mp/doctrack/?request_id={self.entity_id}</strong><br><br>' + \
                    f"Пользователь {self.user.get_name} ответил(а) на ваш комментарий: {self.comment} <br><br>" + \
                    f"Для: {entity}"
                print(attached_comment.user.email)

                emails_to_send = [] 
                emails_to_send.append(attached_comment.user.email)
                send_mail(
                    subject,
                    message,
                    "portal@avh.kz",
                    emails_to_send,
                    html_message=message,
                )   
                print("send mail")
        return res


    class Meta:
        ordering = ["-created_at"]


def format_date_as_condition(date_input):
    current_datetime = timezone.now() + timedelta(hours=6)

    if isinstance(date_input, datetime):
        target_datetime = date_input
    elif isinstance(date_input, str):
        target_datetime = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")

    delta_days = (current_datetime - target_datetime).days

    if delta_days == 0:
        return f"Сегодня в {target_datetime.strftime('%H:%M')}"
    elif delta_days == 1:
        return f"Вчера в {target_datetime.strftime('%H:%M')}"
    else:
        return target_datetime.strftime("%Y-%m-%d %H:%M")


def get_entity_by_id(entity_name, entity_id):
    try:
        entity_model = apps.get_model(app_label="doctrack", model_name=entity_name)
        entity = entity_model.objects.get(id=entity_id)
        return entity
    except entity_model.DoesNotExist:
        return None
