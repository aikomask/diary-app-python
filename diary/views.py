from django.shortcuts import render, redirect, get_object_or_404
from .models import DiaryEntry
from .forms import DiaryEntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматически войти после регистрации
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'diary/register.html', {'form': form})

@login_required
def home(request):
    query = request.GET.get('q')
    entries = DiaryEntry.objects.filter(user=request.user)

    if query:
        entries = entries.filter(title__icontains=query)

    entries = entries.order_by('-created_at')
    count = entries.count() 

    return render(request, 'diary/home.html', {'entries': entries, 'query': query, 'count': count})

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('home')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary/create_entry.html', {'form': form})

@login_required
def view_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user)
    return render(request, 'diary/view_entry.html', {'entry': entry})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user) 
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('view_entry', entry_id=entry.id)
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diary/edit_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('home')
    return render(request, 'diary/delete_entry.html', {'entry': entry})


