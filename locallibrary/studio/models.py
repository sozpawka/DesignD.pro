from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


def upload_to_app(instance, filename):
    # media/applications/<username>/<filename>
    return f"applications/{instance.user.username}/{filename}"


def upload_to_design(instance, filename):
    # media/designs/<application_id>/<filename>
    return f"designs/{instance.id}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name=_("Категория"))
    slug = models.SlugField(max_length=140, unique=True, verbose_name=_("URL"))

    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = _("Категории")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Application(models.Model):
    STATUS_NEW = "new"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"

    STATUS_CHOICES = [
        (STATUS_NEW, "Новая"),
        (STATUS_IN_PROGRESS, "Принято в работу"),
        (STATUS_DONE, "Выполнена"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name=_("Пользователь"),
    )

    title = models.CharField(max_length=200, verbose_name=_("Название"))
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="applications",
        verbose_name=_("Категория"),
    )

    image = models.ImageField(
        upload_to=upload_to_app,
        blank=True,
        null=True,
        verbose_name=_("Фото/план помещения"),
    )

    description = models.TextField(blank=True, verbose_name=_("Описание"))
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_NEW,
        verbose_name=_("Статус"),
    )

    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))

    admin_comment = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Комментарий администратора"),
    )

    design_image = models.ImageField(
        upload_to=upload_to_design,
        blank=True,
        null=True,
        verbose_name=_("Изображение выполненного дизайна"),
    )

    class Meta:
        ordering = ["-created"]
        verbose_name = _("Заявка")
        verbose_name_plural = _("Заявки")

    def __str__(self):
        return f"{self.title} ({self.user})"

    def can_user_delete(self):
        # Пользователь может удалять только заявки в статусе new
        return self.status == self.STATUS_NEW
