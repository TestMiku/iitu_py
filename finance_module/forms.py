from django import forms

from . import models


class ProjectManagerForm(forms.ModelForm):
    class Meta:
        model = models.ProjectManager
        fields = ["user"]


class ProjectRegionForm(forms.ModelForm):
    class Meta:
        model = models.ProjectRegion
        fields = ["name", "project_manager"]
