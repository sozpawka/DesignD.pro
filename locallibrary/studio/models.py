from django.db import models
from django.conf import settings

class Application(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('done', 'Выполнено'),
        ('rejected', 'Отклонено'),
    ]
    CATEGORY_CHOICES = [
        ('kvartira', 'Квартира'),
        ('dom', 'Дом'),
        ('ofis', 'Офис'),
        ('dets', 'Детская'),
        ('other', 'Другое'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='applications/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
