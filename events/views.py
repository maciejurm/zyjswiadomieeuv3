from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Event
from .forms import EventForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def event_list(request):
    events = Event.objects.filter(active=True)
    return render(request, 'event/list.html',
                {'events': events})

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'event/detail.html',
                {'event': event})

@login_required(login_url='/account/login/')
def event_add(request):
    if request.method == 'POST':
        event_add = EventForm(request.POST, request.FILES)
        if event_add.is_valid():
            new_event = event_add.save(commit=False)
            new_event.author = request.user
            new_event.save()
            event_add.save_m2m()
            messages.success(request, 'Wydarzenie zostało przesłane. Pojawi się po akceptacji moderatora.')
        else:
            messages.error(request, 'Błąd! Sprawdź czy wypełniłeś/aś poprawnie wszystkie pola.')
    else:
        event_add = EventForm()

    return render(request, 'event/add.html',
                {'event_add': event_add})