import shutil
import typing

from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.views import generic

from . import models, forms, mixins


class ChoiceTemplateView(mixins.ChoiceMixin, generic.TemplateView):
    folder_template_name = "p1/documents/folder.html"
    document_template_name = "p1/documents/document.html"

    def get_chain(self, parent=None):
        folders = models.Folder.objects.filter(parent=parent, for_roles=self.request.user.role), "folder"
        documents = models.P1Document.objects.filter(parent=parent, for_roles=self.request.user.role), "file"
        if self.request.GET.get("first") == "documents":
            return [documents, folders]
        return [folders, documents]

    def get_sort_fields(self) -> dict[str, str]:
        return {"name": "Имя", "created_at": "Дата создание/загрузки", "uploaded_by": "Загружен/создан",
                "size": "Размер", "description": "Описание"}

    def get_context_data(self, **kwargs) -> dict[str, typing.Any]:
        # TODO: Надо сделать короче.
        context = {}
        if self.is_root:
            context["chain"] = self.get_chain()
            context["sort_fields"] = self.get_sort_fields()
        else:
            instance = self.instance
            if self.is_folder:
                context["folder"] = instance
                context["chain"] = self.get_chain(parent=instance)
                context["sort_fields"] = self.get_sort_fields()
            else:
                context["document"] = self.instance
        return super().get_context_data(**context, **kwargs)


class ChoiceCreateView(mixins.ChoiceMixin, generic.CreateView):
    folder_template_name = "p1/documents/add_folder.html"
    document_template_name = "p1/documents/upload_document.html"
    folder_form_class = forms.FolderForm
    document_form_class = forms.DocumentForm

    @property
    def is_folder(self) -> bool:
        return self.type == "folder"

    @property
    def is_document(self) -> bool:
        return self.type == "document"

    @property
    def type(self) -> str:
        return self.request.GET.get("type", "folder")

    def exists_response(self, form: forms.DocumentForm | forms.FolderForm) -> HttpResponse:
        if self.is_folder:
            form.add_error("name", _("Такая папка уже существует."))
        else:
            form.add_error("document_file", _("Такой документ уже существует."))
        self.extra_context = {"form": form}
        return self.get(self.request)

    def user_role_not_in_roles(self, folder: forms.FolderForm,
                               form: forms.DocumentForm | forms.FolderForm) -> HttpResponse:
        roles = ", ".join(map(str, folder.for_roles.all())) + "."
        if self.is_folder:
            form.add_error(None, _("Вы не можете создать папку в этой папке, так как оно для ролей: ") + roles)
        else:
            form.add_error(None, _("Вы не можете загружать файлы в эту папку, так как оно для ролей: ") + roles)
        self.extra_context = {"form": form}
        return self.get(self.request)

    def form_valid(self, form: forms.DocumentForm | forms.FolderForm) -> HttpResponse:
        if (self.absolute_path / form.instance.get_name()).exists():
            return self.exists_response(form)
        form.instance.uploaded_by = self.request.user
        if not self.is_root:
            folder = models.Folder.objects.get(path=self.kwargs["path"])
            if self.request.user.role not in folder.for_roles.all():
                return self.user_role_not_in_roles(folder, form)
            form.instance.parent = folder
        super().form_valid(form)
        self.object.for_roles.add(self.request.user.role)
        self.object.save()
        if isinstance(self.object, models.Folder):
            self.object.absolute_path.mkdir(parents=True)
        return HttpResponseRedirect(self.object.get_absolute_url())


class ChoiceUpdateView(mixins.ChoiceMixin, mixins.UserUploadedRequiredMixin, generic.UpdateView):
    folder_template_name = "p1/documents/update_folder.html"
    document_template_name = "p1/documents/update_document.html"
    folder_form_class = forms.FolderForm
    document_form_class = forms.DocumentForm

    def get_object(self, queryset=None):
        return self.instance

    def form_valid(self, form: forms.FolderForm | forms.DocumentForm):
        is_folder = self.is_folder
        if is_folder:
            shutil.move(self.object.absolute_path, self.object.absolute_path.with_name(form.cleaned_data["name"]))

        elif "document_file" in form.changed_data:
            self.object.absolute_path.unlink(missing_ok=True)
        response = super().form_valid(form)
        if is_folder:
            self.object.update_children_path()
        self.object.for_roles.add(self.request.user.role)
        return response


class ChoiceDeleteView(mixins.ChoiceMixin, mixins.UserUploadedRequiredMixin, generic.DeleteView):
    folder_template_name = "p1/documents/delete_folder.html"
    document_template_name = "p1/documents/delete_document.html"

    def get_object(self, queryset=None):
        return self.instance

    def get_success_url(self) -> str:
        return self.object.back_url()
