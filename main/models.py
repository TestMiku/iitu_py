import pytz
from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)


class AvhRole(models.Model):
    name = models.CharField(max_length=50)
    is_admin = models.BooleanField(_("Admin"), default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Отдел")
        verbose_name_plural = _("Отделы")

class AvhUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    avatar = models.ImageField(
        upload_to="avatars/", default="default/user_avatar.webp", blank=True
    )
    role = models.ForeignKey(
        "main.AvhRole",
        verbose_name=_("Роль"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    work_number = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    send_notifications_to_email = models.BooleanField(
        verbose_name=_("Получать уведомления по почте при изменениях"),
        default=False,
    )
    skills = models.JSONField(default=list, blank=True)  # JSON поле для хранения навыков
    html_info = models.TextField(
        _("Информация для HTML"),
        null=True,
        blank=True,
        default="""
                """,
    )
    record = models.TextField(blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    @property
    def avh_user_id_from_email(self) -> str | None:
        avh_user_id = self.email.split("@")[0]
        if not avh_user_id.isdigit():
            return None
        return avh_user_id

    def __str__(self):
        return f"{self.get_full_name()} {self.email}"

    class Meta:
        verbose_name = _("Сотрудник")
        verbose_name_plural = _("Сотрудники")
        ordering = ["first_name", "last_name", "email"]

    @property
    def get_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"{self.email}"


class AvhObject(models.Model):
    created_by = models.ForeignKey(
        "main.AvhUser",
        related_name="%(class)s_created_by",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
        blank=True,
    )
    modified_by = models.ForeignKey(
        "main.AvhUser",
        related_name="%(class)s_modified_by",
        on_delete=models.CASCADE,
        editable=False,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(
        "main.AvhUser",
        related_name="%(class)s_deleted_by",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )

    def created_at_format(self):
        utc_plus_6 = pytz.timezone("Asia/Almaty")
        created_at_formatted = self.created_at.astimezone(utc_plus_6).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
        return created_at_formatted

    def modified_at_format(self):
        utc_plus_6 = pytz.timezone("Asia/Almaty")
        modified_at_formatted = self.modified_at.astimezone(utc_plus_6).strftime(
            "%d.%m.%Y %H:%M:%S"
        )
        return modified_at_formatted

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        if user:
            if not self.pk:
                self.created_by = user
            else:
                self.modified_by = user
        super().save(*args, **kwargs)


class ChapterGroup(AvhObject):
    title = models.CharField(_("Название"), max_length=50)
    color = ColorField(default="#4e73df")
    is_default = models.BooleanField(_("Общедоступный"), default=False)
    short_description = models.TextField(_("Описание"), blank=True, null=True)
    parent = models.ForeignKey(
        "ChapterGroup",
        verbose_name=_("Родительская группа"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    roles = models.ManyToManyField(
        AvhRole, related_name="chapter_groups", verbose_name=_("Роли"), blank=True
    )

    def get_parent_url(self) -> str:
        return (
            reverse("chapters")
            if self.parent is None
            else self.parent.get_absolute_url()
        )

    def get_absolute_url(self) -> str:
        return reverse("chapters_with_parent", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.title


class Chapter(AvhObject):
    title = models.CharField(_("Название"), max_length=50)
    link = models.CharField(_("Ссылка"), max_length=5000)
    color = ColorField(default="#4e73df")
    short_description = models.TextField(_("Описание"), blank=True, null=True)
    icon = models.CharField(
        _("Иконка в формате HTML"),
        max_length=5000,
        default='<i class="fas fa-info-circle fa-2x text-gray-500"></i>',
    )
    is_default = models.BooleanField(_("Общедоступный"), default=False)
    roles = models.ManyToManyField(
        AvhRole, related_name="chapters", verbose_name=_("Роли"), blank=True
    )
    parent = models.ForeignKey(
        "ChapterGroup",
        verbose_name=_("Родительская группа"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def get_parent_url(self) -> str:
        return (
            reverse("chapters")
            if self.parent is None
            else self.parent.get_absolute_url()
        )

    def __str__(self):
        return self.title  # + " - " + self.link

    class Meta:
        verbose_name = _("Раздел")
        verbose_name_plural = _("Разделы сайта")
