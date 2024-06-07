from django import forms
from .models import StaticApp

class StaticAppForm(forms.ModelForm):
    class Meta:
        model = StaticApp
        fields = '__all__'  # Для использования всех полей модели в форме

    # Дополнительные настройки полей формы (если нужно)
    # Например, можно добавить виджеты или установить атрибуты
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['preview_description'].widget = forms.Textarea(attrs={'rows': 2, 'cols': 40, 'class' : 'form-control'})
        self.fields['instruction'].widget = forms.Textarea(attrs={'rows': 16, 'cols': 40, 'class' : 'form-control'})
        self.fields['file_field'].widget.attrs.update({'class': 'file-input'})

    # Можно добавить дополнительную валидацию полей формы, если необходимо


from django import forms
from main.models import Chapter

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'link', 'color', 'short_description', 'icon', 'is_default', 'roles']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control form-control-color'}),
            'short_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'cols': 40,}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            # 'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'roles': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
