import pathlib

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, Http404

from documents import models
from documents.services import get_absolute_path


class UserUploadedRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.instance.uploaded_by != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class PathMixin(LoginRequiredMixin):
    _is_folder: bool = False
    _is_document: bool = False
    _instance: models.Folder | models.P1Document | None = None
    kwargs: dict[str, str]
    request: HttpRequest

    def _set_instance(self) -> None:
        if self._instance is not None:
            return None
        try:
            document = models.P1Document.objects.get(for_roles=self.request.user.role, path=self.kwargs["path"])
            self._is_document = True
            self._instance = document
        except models.P1Document.DoesNotExist:
            try:
                folder = models.Folder.objects.get(for_roles=self.request.user.role, path=self.kwargs["path"])
                self._is_folder = True
                self._instance = folder
            except models.Folder.DoesNotExist:
                return None

    @property
    def instance(self) -> models.Folder | models.P1Document:
        self._set_instance()
        if self._instance is None:
            raise Http404
        return self._instance

    @property
    def is_root(self) -> bool:
        return "path" not in self.kwargs

    @property
    def is_folder(self) -> bool:
        if self.is_root:
            return True
        self._set_instance()
        return self._is_folder

    @property
    def is_document(self) -> bool:
        if self.is_root:
            return False
        self._set_instance()
        return self._is_document

    @property
    def absolute_path(self) -> pathlib.Path:
        return get_absolute_path(str(self.request.user)) if self.is_root else get_absolute_path(
            str(self.instance.uploaded_by), self.kwargs["path"])


class ChoiceMixin(PathMixin):
    folder_form_class: type[forms.Form] | None = None
    document_form_class: type[forms.Form] | None = None
    folder_template_name: str | None = None
    document_template_name: str | None = None

    def get_template_names(self) -> list[str]:
        if self.folder_template_name is None and self.document_template_name is None:
            return super().get_template_names()

        if self.is_folder:
            return [self.folder_template_name]
        return [self.document_template_name]

    def get_form_class(self) -> type[forms.Form]:
        if self.folder_form_class is None and self.document_form_class is None:
            return super().get_form_class()

        if self.is_folder:
            return self.folder_form_class
        return self.document_form_class
