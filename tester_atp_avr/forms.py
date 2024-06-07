from django import forms
from django.utils.translation import gettext_lazy as _

from . import models
from . import services


class TCPFileForm(forms.ModelForm):
    price_column = forms.ChoiceField(
        label=_("Столбец цен"),
        choices=services.PriceColumn.choices,
        initial=services.PriceColumn.BASE_PRICE_AFTER_DISCOUNT,
    )

    class Meta:
        model = models.TCPFile
        fields = ["file", "name"]
