from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class DiaryManager(models.Manager):
    def today(self):
        now = timezone.localtime()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        return self.filter(created_at__gte=start, created_at__lt=end)

    def recent(self):
        return self.filter(created_at__gte=timezone.now() - timedelta(days=7))

    def pinned(self):
        return self.filter(is_pinned=True)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DiaryEntry(models.Model):
    objects = DiaryManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    categories = models.ManyToManyField(Category, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_pinned = models.BooleanField(default=False)
    image = models.ImageField(upload_to='diary_images/', blank=True, null=True)

    def __str__(self):
        return self.title
