from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class DocumentForm(forms.ModelForm):
    class Meta:
        model = models.P1Document
        fields = ["name", "description", "document_file", "for_roles"]


class FolderForm(forms.ModelForm):
    class Meta:
        model = models.Folder
        fields = ["name", "description", "for_roles"]


class CompressForm(forms.Form):
    percent = forms.TypedChoiceField(label=_("Степень сжатие в процентах"), coerce=int,
                                     choices=zip(range(10, 91, 10), range(10, 91, 10)), initial=50)


class DocumentUpdateForm(forms.ModelForm):
    name = forms.CharField(required=False)

    class Meta:
        model = models.Folder
        fields = ["name", "description", "for_roles"]
