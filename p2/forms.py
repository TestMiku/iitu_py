from django import forms
from .models import Document, Request, DocumentRent

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['project', 'doc_type', 'work_type', 'document', "request",]

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['region', 'bis_name', 'order_number', 'comment', 'doc_type', "order_date"]
        widgets = {
            'order_date': forms.DateInput(format='%d.%m.%Y'),
        }


class DocumentRentForm(forms.ModelForm):
    class Meta:
        model = DocumentRent
        fields = ['documentRent', 'workRent_type']

