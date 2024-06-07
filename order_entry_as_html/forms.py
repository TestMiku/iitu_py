from django import forms
from django.utils.translation import gettext_lazy as _

from . import converters
from .models import OrderRegion


class OrderEntryForm(forms.Form):
    project = forms.ChoiceField(
        label=_("Проект"),
        choices=zip(converters.supported_projects(), converters.supported_projects()),
        widget=forms.Select({"class": "custom-select"}),
    )
    region = forms.ModelChoiceField(
        label=_("Регион"),
        queryset=OrderRegion.objects.all(),
        widget=forms.Select({"class": "selectpicker", "data-live-search": "true"}),
        empty_label=_("Выберете регион"),
        required=False,
    )
    contract_date = forms.DateField(
        label=_("Дата подписание контракта"),
        widget=forms.DateInput({"class": "form-control", "type": "date"}),
        required=False,
    )
