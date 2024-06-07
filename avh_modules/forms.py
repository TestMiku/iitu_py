from django import forms


class TransformXLSXFileForm(forms.Form):
    file = forms.FileField()
