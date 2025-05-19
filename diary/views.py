from django.db.models import Q, Avg, Count
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from weasyprint import HTML
import tempfile
from django.utils.dateformat import format

from .models import DiaryEntry, Category
from .forms import DiaryEntryForm

from django.contrib.auth import logout
from django.shortcuts import redirect

def toggle_theme(request):
    current = request.session.get('theme', 'light')
    request.session['theme'] = 'pink' if current == 'light' else 'light'
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def logout_view(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    theme = request.session.get('theme', 'light')
    return render(request, 'diary/register.html', {'form': form, 'theme': theme})

@login_required
def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    date_filter = request.GET.get('date')
    theme = request.session.get('theme', 'light')

    entries = DiaryEntry.objects.filter(user=request.user)

    if category_id:
        entries = entries.filter(categories__id=category_id)

    if date_filter:
        try:
            target_date = timezone.datetime.strptime(date_filter, "%Y-%m-%d").date()
            entries = entries.filter(created_at__date=target_date)
        except ValueError:
            pass

    if query:
        entries = entries.filter(Q(title__icontains=query))

    entries = entries.order_by('-is_pinned', '-created_at')
    count = entries.count()
    categories = Category.objects.all()

    return render(request, 'diary/home.html', {
        'entries': entries,
        'query': query,
        'count': count,
        'categories': categories,
        'active_category': int(category_id) if category_id else None,
        'active_date': date_filter,
        'theme': theme,
    })


@login_required
def create_entry(request):
    theme = request.session.get('theme', 'light')
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = DiaryEntryForm()
    return render(request, 'diary/create_entry.html', {'form': form, 'theme': theme})


@login_required
def view_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user)
    theme = request.session.get('theme', 'light')
    return render(request, 'diary/view_entry.html', {'entry': entry, 'theme': theme})


@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user)
    theme = request.session.get('theme', 'light')
    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, request.FILES, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('view_entry', entry_id=entry.id)
    else:
        form = DiaryEntryForm(instance=entry)
    return render(request, 'diary/edit_entry.html', {'form': form, 'entry': entry, 'theme': theme})


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(DiaryEntry, pk=entry_id, user=request.user)
    theme = request.session.get('theme', 'light')
    if request.method == 'POST':
        entry.delete()
        return redirect('home')
    return render(request, 'diary/delete_entry.html', {'entry': entry, 'theme': theme})


@login_required
def export_entry_pdf(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id, user=request.user)
    html_string = render_to_string('diary/entry_pdf.html', {'entry': entry})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{entry.title}.pdf"'

    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(tmp.name)
        tmp.seek(0)
        response.write(tmp.read())

    return response


@login_required
def diary_stats(request):
    stats = {
        "total_entries": DiaryEntry.objects.count(),
        "avg_length": DiaryEntry.objects.aggregate(Avg("content"))["content__avg"] or 0,
        "today_entries": DiaryEntry.objects.today().count(),
        "recent_entries": DiaryEntry.objects.recent().count(),
        "pinned_entries": DiaryEntry.objects.pinned().count()
    }
    return render(request, "diary/stats.html", {"stats": stats})

@login_required
def chart_view(request):
    raw_data = (
        DiaryEntry.objects
        .annotate(day=TruncDay("created_at"))
        .values("day")
        .annotate(count=Count("id"))
        .order_by("day")
    )

    labels = [format(item["day"], "Y-m-d") for item in raw_data]
    counts = [item["count"] for item in raw_data]

    return render(request, "diary/chart.html", {
        "labels": labels,
        "counts": counts
    })

