from django import forms
from .models import DiaryEntry, Category

class DiaryEntryForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class DiaryEntryForm(forms.ModelForm):
        class Meta:
            model = DiaryEntry
            fields = ['title', 'content', 'categories']

