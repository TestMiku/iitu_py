from datetime import datetime
from django.utils import timezone

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from main.models import AvhObject, AvhUser


class Project(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class DocType(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="doc_types"
    )

    def __str__(self):
        return self.name


class WorkRentType(models.Model):
    name = models.CharField(max_length=255)
    doc_type = models.ForeignKey(
        DocType, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


class WorkType(models.Model):
    name = models.CharField(max_length=255)
    doc_type = models.ForeignKey(
        DocType, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.name


STATUS_CHOICES = (
    ("pending", "В ожиданий у отдела аренды и выкупа"),
    ("pending-none", "Подготовка документов"),
    ("pending2", "На рассмотрении у финансового отдела для частичной закрытий"),
    ("pending3", "На рассмотрении у финансового отдела для полной закрытий"),
    ("approved", "Заявка завершена частично"),
    ("rejected", "Отклонено финансовым отделом"),
    (
        "rejected_both",
        "В ожидании корректировок у отдела технической документации и аренды и выкупа",
    ),
    ("rejected_docs", "В ожидании корректировок у отдела технической документации"),
    ("rejected_rent", "В ожидании корректировок у отдела аренды и выкупа"),
    ("approved_full", "Заявка завершена полностью"),
    ("close", "Закрыто финансовыми отделом"),
)

STATUS_COLORS = {
    "pending": "#b3ffb3",
    "pending-none": "#ffccff",
    "pending2": "#ffff99",
    "pending3": "#99ccff",
    "approved": "#33cc33",
    "rejected": "#ff9980",
    "rejected_both": "#ff471a",
    "rejected_docs": "#ffcc00",
    "rejected_rent": "#ffe066",
    "approved_full": "#00ff00",
    "close": "#dcdeef",
}


class Request(AvhObject):
    request_number = models.AutoField(primary_key=True)
    region = models.CharField(max_length=255)
    doc_type = models.ForeignKey(
        DocType, on_delete=models.CASCADE, null=True, blank=True
    )
    bis_name = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="pending2"
    )
    comment = models.TextField(blank=True)
    isapproved = models.BooleanField(default=False)
    comment_reject = models.TextField(blank=True)
    history_count = models.IntegerField(default=0)
    history = HistoricalRecords()
    order_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Заявка {self.request_number}"

    def get_comment_reject(self):
        result = ""
        if self.comment_reject:
            result = f"{self.comment_reject}; "
        documents: list[Document] = self.document_set.all()
        if documents:
            for document in documents:
                if document.comment:
                    result += f"{document.work_type}: {document.comment}; "
        return result

    @property
    def get_bs_num_date(self):
        formatted_date = None
        if self.order_date:
            formatted_date = self.order_date.strftime("%d.%m.%Y")
        return f" {self.bis_name} №{self.order_number} от {formatted_date}"

    @property
    def color(self):
        return STATUS_COLORS.get(self.status, "#fff")
    
    @property
    def get_comments(self):
        return []
        # comments = Comment.objects.filter(entity="Request", entity_id=self.request_number)
        # comments_list = [comment for comment in comments]
        # print(comments_list)
        # return comments_list
    


class Region(models.Model):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(
        "main.AvhUser",
        related_name="regions",
        related_query_name="region",
    )

    def __str__(self):
        return self.name


# class RequestHistory(models.Model):
#     request = models.ForeignKey('Request', on_delete=models.CASCADE, related_name='history_entries')
#     status = models.CharField(max_length=255, choices=STATUS_CHOICES)
#     timestamp = models.DateTimeField(default=timezone.now)
#     user = models.ForeignKey(AvhUser, on_delete=models.SET_NULL, null=True, blank=True)
#
#     def __str__(self):
#         return f'История заявки {self.request.request_number}'
#
#     class Meta:
#         ordering = ['-timestamp']


class DocumentRent(AvhObject):
    documentRent = models.FileField(upload_to="p2/")
    workRent_type = models.ForeignKey(WorkRentType, on_delete=models.CASCADE, null=True)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="pending2"
    )
    comment = models.TextField(blank=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)

    def clean(self):
        if self.status == "rejected" and not self.comment:
            raise ValidationError("Комментарий обязателен при отклонении документа.")

    def __str__(self):
        return self.documentRent.name


class Document(AvhObject):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    work_type = models.ForeignKey(WorkType, on_delete=models.CASCADE)
    doc_type = models.ForeignKey(
        DocType, on_delete=models.CASCADE, null=True, blank=True
    )
    request = models.ForeignKey(Request, on_delete=models.CASCADE, null=True)
    document = models.FileField(
        upload_to="p2/",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(
        max_length=255, choices=STATUS_CHOICES, default="pending2"
    )
    comment = models.TextField(blank=True)

    def get_rejection_reason(self):
        return

    def __str__(self):
        return self.document.name

    def get_name(self):
        name = f"{self.document.name}".replace("\\", "/").split("/")[-1]
        return name

    def clean(self):
        if self.status == "rejected" and not self.comment:
            raise ValidationError("Комментарий обязателен при отклонении документа.")


class RejectedDocument(AvhObject):
    documentRent = models.ForeignKey(
        DocumentRent, on_delete=models.SET_NULL, null=True, blank=True
    )
    document = models.ForeignKey(
        Document, on_delete=models.SET_NULL, null=True, blank=True
    )
    rejection_reason = models.TextField()
    request_number = models.IntegerField()

    def __str__(self):
        return f"Отклоненный документ заявки: {self.request_number}"


# class Comment(AvhObject):
#     entity = models.CharField(_("Сущность (class_name)"), max_length=50)
#     entity_id = models.IntegerField(_("ID сущности"))

#     attached_entity = models.CharField(
#         _("Прикрепленная сущность (class_name)"), max_length=50, null=True, blank=True
#     )
#     attached_entity_id = models.IntegerField(
#         _("ID прикрепленной сущности"), null=True, blank=True
#     )

#     user = models.ForeignKey(AvhUser, on_delete=models.CASCADE, null=True, blank=True)
#     comment = models.TextField()

#     def __str__(self):
#         entity_info = ""
#         if self.attached_entity and self.attached_entity_id:
#             attached_entity = get_entity_by_id(self.attached_entity, self.attached_entity_id)
#             entity_info = f" (Прикреплено к {attached_entity})"
#         try:
#             print(format_date_as_condition(self.created_at))
#         except Exception as e:
#             print(e)
#         if self.user:
#             return f"{self.user.get_name} {format_date_as_condition(self.created_at)}: {self.comment}{entity_info}"
#         return f"Anonimous User {format_date_as_condition(self.created_at)}: {self.comment}{entity_info}"

# def format_date_as_condition(date_input):
#     current_datetime = timezone.now()

#     if isinstance(date_input, datetime):
#         target_datetime = date_input
#     elif isinstance(date_input, str):
#         target_datetime = datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
    
#     delta_days = (current_datetime - target_datetime).days
    
#     if delta_days == 0:
#         return f"{target_datetime.strftime('%H:%M')}"
#     elif delta_days == 1:
#         return f"Вчера в {target_datetime.strftime('%H:%M')}"
#     else:
#         return target_datetime.strftime("%Y-%m-%d %H:%M")


# def get_entity_by_id(entity_name, entity_id):
#     try:
#         entity_model = apps.get_model(app_label='p2', model_name=entity_name)
#         entity = entity_model.objects.get(id=entity_id)
#         return entity
#     except entity_model.DoesNotExist:
#         return None
