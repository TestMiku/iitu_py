from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from main import models


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        fields = ('old_password', 'new_password1', 'new_password2')


class ChapterGroupForm(forms.ModelForm):
    class Meta:
        model = models.ChapterGroup
        fields = ["title", "color", "is_default", "short_description"]
