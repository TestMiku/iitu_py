from django import forms
from .models import MainModel

class UploadFileForm(forms.Form):
    file = forms.FileField(label='Select an Excel file')

