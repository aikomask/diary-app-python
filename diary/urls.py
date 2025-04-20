from django.urls import path
from . import views
from diary.views import register

urlpatterns = [
    path('', views.home, name='home'),
    path('new/', views.create_entry, name='create_entry'),
    path('entry/<int:entry_id>/', views.view_entry, name='view_entry'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path('entry/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
    path('register/', register, name='register'),
]


