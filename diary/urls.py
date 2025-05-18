from django.urls import path
from . import views
from diary.views import register
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.create_entry, name='create_entry'),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('register/', register, name='register'),
    path('entry/<int:entry_id>/export/', views.export_entry_pdf, name='export_entry_pdf'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('stats/', views.diary_stats, name='diary_stats'),
    path('chart/', views.chart_view, name='chart'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


