from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.


class StaticApp(models.Model):
    name = models.CharField(_("Название"), max_length=50)
    preview_description = models.TextField(_("Короткое описание"))


    instruction = models.TextField(_("Инструкция"))
    
    file_field = models.FileField(_("Файл"), upload_to='uploads/', blank=True, null=True)  # upload_to определяет директорию для сохранения файлов



    roles = models.ManyToManyField("main.AvhRole", verbose_name=_("Роли"))

    class Meta:
        verbose_name = _("Скрипт")
        verbose_name_plural = _("Скрипты")

    def __str__(self):
        return f'{self.name} #{self.id}'

    def get_absolute_url(self):
        return reverse("StaticApp_detail", kwargs={"pk": self.pk})

    def html_instruction(self):
        text = self.instruction

        # Приобразователь заголовки
        text = text.replace("-!", "<h3>")
        text = text.replace("!-", "</h3>")
        
        # Приобразователь в неупорядоченные строки
        text = text.replace("-*", "<ul>")
        text = text.replace("*-", "</ul>")
        
        # Приобразователь в упорядоченные строки
        text = text.replace("-1", "<ol>")
        text = text.replace("1-", "</ol>")

        # Приобразователь в строки порядка
        text = text.replace("-.", "<li>")
        text = text.replace(".-", "</li>")

        # Приобразователь в строки порядка
        text = text.replace("-ж", "<b>")
        text = text.replace("ж-", "</b>")

        # Приобразователь ссылки
        text = text.replace("-/", '<a href=">')
        text = text.replace("/-", '" target="_blank" >Ссылка</a>')

        text = text.replace("\n", "<br>")
        text = text.replace("___", "<hr>")

        return text
