from django import forms
from .models import Handbook


class HandbookModelForm(forms.ModelForm):
    CATEGORY_CHOICES = (
        ('Материал', 'Материал'),
        ('Работа', 'Работа'),
    )

    UNIT_CHOICES = (
        ('шт', 'шт'),
        ('кг', 'кг'),
        ('л', 'л'),
        ('м', 'м'),
        ('уп', 'уп'),
    )

    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    unit = forms.ChoiceField(choices=UNIT_CHOICES)
    
    class Meta:
        model = Handbook
        fields = ('code', 'quantity', 'name', 'unit', 'category')
