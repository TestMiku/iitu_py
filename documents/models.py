import itertools
import pathlib
import shutil

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from hurry.filesize import size, alternative

from main.models import AvhObject
from .services import get_path, set_path, get_absolute_path


class Object(AvhObject):
    uploaded_by = models.ForeignKey("main.AvhUser", verbose_name=_("Загрузил"), on_delete=models.CASCADE)
    parent = models.ForeignKey(
        "Folder", on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(_("Имя"), max_length=256, unique=True)
    description = models.TextField(_("Описание"), null=True, blank=True)
    for_roles = models.ManyToManyField("main.AvhRole", verbose_name=_("Для ролей"), related_name="+", blank=True)
    path = models.TextField(_("Путь"), blank=True)

    def __str__(self) -> str:
        return self.get_name()

    @property
    def relative_path(self) -> pathlib.Path:
        return get_path(str(self.uploaded_by), self.path)

    @property
    def absolute_path(self) -> pathlib.Path:
        return get_absolute_path(str(self.uploaded_by), self.path)

    def get_name(self) -> str:
        return self.name

    def get_real_name(self) -> str:
        return self.get_name()

    def get_size(self) -> int:
        return 0

    def get_size_as_str(self) -> str:
        return size(self.get_size(), alternative)

    def back_url(self) -> str:
        return (
            reverse("documents:list")
            if self.parent is None
            else self.parent.get_absolute_url()

        )

    def get_absolute_url(self):
        return reverse("documents:list_with_path", kwargs={"path": self.path})

    def get_update_url(self) -> str:
        return ""

    def get_delete_url(self) -> str:
        return ""

    def save(self, *args, **kwargs) -> None:
        set_path(self)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True


class Folder(Object):
    def get_update_url(self) -> str:
        return reverse("documents:update_folder", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("documents:delete_folder", kwargs={"pk": self.pk})

    def get_size(self) -> int:
        return sum(
            i.get_size()
            for i in itertools.chain(
                P1Document.objects.filter(parent=self),
                Folder.objects.filter(parent=self)
            )
        )

    def update_children_path(self) -> None:
        documents = P1Document.objects.filter(parent=self)

        for document in documents:
            set_path(document)
            document.document_file.name = get_path(str(document.uploaded_by), document.path).as_posix()
            document.save()

        folders = Folder.objects.filter(parent=self)

        for folder in folders:
            set_path(folder)
            folder.save()
            folder.update_children_path()


@receiver(post_delete, sender=Folder)
def folder_post_delete(sender: type[Folder], instance: Folder, **kwargs) -> None:
    shutil.rmtree(instance.absolute_path, ignore_errors=True)


def document_file_upload_to(instance: "P1Document", filename: str) -> str:
    return str(
        get_path(str(instance.uploaded_by), '' if instance.parent is None else instance.parent.path,
                 filename))


class P1Document(Object):
    name = models.CharField(_("Имя"), max_length=256, unique=True, null=True, blank=True)
    document_file = models.FileField(_("Файл документа"), upload_to=document_file_upload_to, unique=True)

    def get_name(self) -> str:
        return self.name or self.get_real_name()

    def get_size(self) -> int:
        return self.document_file.size

    def get_real_name(self) -> str:
        return pathlib.Path(self.document_file.name).name

    def get_update_url(self) -> str:
        return reverse("documents:update_document", kwargs={"pk": self.pk})

    def get_delete_url(self) -> str:
        return reverse("documents:delete_document", kwargs={"pk": self.pk})


@receiver(post_delete, sender=P1Document)
def document_post_delete(sender: type[P1Document], instance: P1Document, **kwargs) -> None:
    instance.absolute_path.unlink(missing_ok=True)
