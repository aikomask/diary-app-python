from django.contrib import admin
from .models import DiaryEntry, Category

admin.site.register(DiaryEntry)
admin.site.register(Category)