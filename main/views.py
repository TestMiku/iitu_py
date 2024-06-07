from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views import View, generic

from main.models import AvhUser, Chapter

from . import forms, models
from .forms import CustomPasswordChangeForm


class ChaptersTemplateView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        parent = self.kwargs.get("pk")
        if self.request.user.is_authenticated:
            if parent is not None:
                parent = get_object_or_404(
                    models.ChapterGroup,
                    Q(roles=self.request.user.role) | Q(is_default=True),
                    pk=parent,
                    is_active=True,
                )
            return super().get_context_data(
                chapter_group=parent,
                chapter_groups=models.ChapterGroup.objects.filter(
                    Q(roles=self.request.user.role) | Q(is_default=True),
                    parent=parent,
                    is_active=True,
                ).distinct(),
                chapters=models.Chapter.objects.filter(
                    Q(roles=self.request.user.role) | Q(is_default=True),
                    parent=parent,
                    is_active=True,
                ).distinct(),
                **kwargs
            )
        else:
            if parent is not None:
                parent = get_object_or_404(
                    models.ChapterGroup, pk=parent, is_default=True, is_active=True
                )
            return super().get_context_data(
                chapter_group=parent,
                chapter_groups=models.ChapterGroup.objects.filter(
                    parent=parent, is_default=True, is_active=True
                ),
                chapters=models.Chapter.objects.filter(
                    parent=parent, is_default=True, is_active=True
                ),
                **kwargs
            )


class ChapterGroupCreateView(generic.CreateView):
    template_name = "main/chapter_group_create.html"
    form_class = forms.ChapterGroupForm

    def form_valid(self, form: forms.ChapterGroupForm):
        form.instance.parent_id = self.request.GET.get("parent")
        return super().form_valid(form)


class SearchChaptersListView(generic.TemplateView):
    template_name = "main/search.html"

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            return super().get_context_data(
                matched_chapters=models.Chapter.objects.filter(
                    Q(roles=self.request.user.role) | Q(is_default=True),
                    title__iregex=self.request.GET["query"],
                    is_active=True,
                ).distinct(),
                matched_chapter_groups=models.ChapterGroup.objects.filter(
                    Q(roles=self.request.user.role) | Q(is_default=True),
                    title__iregex=self.request.GET["query"],
                    is_active=True,
                ).distinct(),
            )
        return super().get_context_data(
            matched_chapters=models.Chapter.objects.filter(
                is_default=True,
                title__iregex=self.request.GET["query"],
                is_active=True,
            ),
            matched_chapter_groups=models.ChapterGroup.objects.filter(
                is_default=True,
                title__iregex=self.request.GET["query"],
                is_active=True,
            ),
        )


# Create your views here.
def main_tables(request):
    if not request.user.is_authenticated:
        return redirect("login")

    return render(request, "index.html")


def chapters(request):
    if not request.user.is_authenticated:
        chapters = Chapter.objects.filter(is_default=True, is_active=True)
        return render(request, "index.html", {"chapters": chapters})
    else:
        if request.user.role:
            chapters = request.user.role.chapters.all()
        else:
            chapters = []
        return render(request, "index.html", {"chapters": chapters})


class LoginView(View):
    template_name = "login.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            next_url = request.GET.get("next", "")
            if user is not None:
                login(request, user)
                if next_url:
                    return redirect(next_url)
                return redirect("/")

        messages.error(request, "Неверный логин или пароль")
        return redirect('login')


@login_required
def change_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            print("success")
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("password_change_done")
        else:
            print(form.errors)
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "change_password.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "main/profile.html")


# def profile(request, email):
#     user = AvhUser.objects.filter(email=email)
#     if not user:
#         return HttpResponse("<h1>Нет профиля</h1>")
#
#     return render(request, "main/profile_index.html")


@login_required
def profile_edit(request):
    if request.method == "POST":
        user = request.user

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        work_number = request.POST.get("work_number")
        phone_number = request.POST.get("phone_number")
        send_notifications_to_email = request.POST.get("send_notifications_to_email") == 'on'
        avatar = request.FILES.get("avatar")

        user.first_name = first_name
        user.last_name = last_name
        user.work_number = work_number
        user.phone_number = phone_number
        user.send_notifications_to_email = send_notifications_to_email
        if avatar:
            user.avatar = avatar

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if old_password and new_password and confirm_password:
            if user.check_password(old_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                    update_session_auth_hash(request, user)  # Обновляем сессию для предотвращения выхода пользователя
                    # messages.success(request, "Пароль успешно изменен")
                else:
                    pass
                    # messages.error(request, "Новый пароль и подтверждение пароля не совпадают")
            else:
                pass
                # messages.error(request, "Старый пароль введен неверно")

        skills = []
        skill_names = request.POST.getlist('skill_name')
        skill_levels = request.POST.getlist('skill_level')
        for name, level in zip(skill_names, skill_levels):
            if name and level:
                skills.append({"name": name, "level": level})

        user.skills = skills
        user.save()

        # messages.success(request, "Профиль успешно обновлен")
        return redirect("profile_view")

    return render(request, "main/profile_edit.html")


def OneSignalSDKWorker(request):
    path = "static/notifications/OneSignalSDKWorker.js"
    with open(path, "r") as file:
        content = file.read()
    response = HttpResponse(content, content_type="application/javascript")
    return response


@login_required
def send_notifications_to_email_1(request):
    print("send_notifications_to_email_1")
    user = AvhUser.objects.get(email=request.user.email)
    user.send_notifications_to_email = True
    user.save()
    print(user.send_notifications_to_email)
    return redirect("profile_view")

@login_required
def send_notifications_to_email_0(request):
    print("send_notifications_to_email_0")
    user = AvhUser.objects.get(email=request.user.email)
    user.send_notifications_to_email = False
    user.save()
    print(user.send_notifications_to_email)
    return redirect("profile_view")