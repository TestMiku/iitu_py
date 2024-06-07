
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import DTComment, DTDocument, DTProject, DTRegion, DTRequest, DTStatus, DTWorkType


class ChangeStatusForm(forms.ModelForm):
    class Meta:
        model = DTRequest
        fields = ["status"]

    def save(self, request):
        self.request = request
        super().save(commit=False)


class DTRequestForm(forms.ModelForm):
    class Meta:
        model = DTRequest
        fields = [
            "region",
            "project",
            "work_type",
            "is_partial",
            "order_bs_name",
            "order_number",
            "order_date",
            "comment",
            "creator"
        ]


class DTDocumentForm(forms.ModelForm):
    class Meta:
        model = DTDocument
        fields = ["document_type", "file", "request"]


class DTDocumentEditForm(forms.ModelForm):
    class Meta:
        model = DTDocument
        fields = ["file"]


DTDocumentFormSet = forms.inlineformset_factory(
    DTRequest,
    DTDocument,
    form=DTDocumentForm,
    extra=1,  # количество дополнительных форм
    can_delete=True,  # позволяет удалять связанные объекты
)


class DTCommentForm(forms.ModelForm):
    class Meta:
        model = DTComment
        fields = [
            "entity",
            "entity_id",
            "attached_entity",
            "attached_entity_id",
            "user",
            "comment",
        ]



class DTRequestFilterForm(forms.Form):
    filter_by_region = forms.ModelMultipleChoiceField(
        queryset=DTRegion.objects.all(),
        label=_("Регион"),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    filter_by_project = forms.ModelMultipleChoiceField(
        queryset=DTProject.objects.all(),
        label=_("Проект"),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    filter_by_work_type = forms.ModelMultipleChoiceField(
        queryset=DTWorkType.objects.all(),
        label=_("Вид работ"),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    filter_by_status = forms.ModelMultipleChoiceField(
        queryset=DTStatus.objects.all(),
        label=_("Статус"),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
