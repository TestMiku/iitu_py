from django import forms


class HTMLWidget(forms.Widget):
    template_name = "forms/html_input.html"
