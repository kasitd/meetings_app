from django.shortcuts import render, get_object_or_404, redirect
from .models import Meeting, Room
from .forms import MeetingForm
import re
from django.contrib import messages
from django.utils import timezone


def index(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    return render(request, "meetings/index.html", {"meeting": meeting})


def new(request):
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            meeting = form.save()
            return redirect("index", id=meeting.pk)
    else:
        form = MeetingForm()
    return render(request, "meetings/new.html", {"form": form})


def home(request):
    if request.user.is_authenticated:
        user_meetings = Meeting.objects.meetings_for_user(request.user)

        meetings_today = user_meetings.filter(date=timezone.datetime.today())
        meetings_future = user_meetings.filter(date=timezone.datetime.today())
        context = {"meetings_today": meetings_today,
                   "meetings_future": meetings_future}
        return render(request, "meetings/home.html", context)
    else:
        return render(request, "meetings/home.html")


def is_valid_queryparam(param):
    return param != '' and param is not None


def get_room_elements(room):
    return re.split("nr: |, |piętro: ", room)[-3], re.split("nr: |, |piętro: ", room)[-1]



def search_form(request):
    qs = Meeting.objects.all()
    rooms = Room.objects.all()
    if request.method == "GET":
        title_contains_query = request.GET.get('title_contains')
        author_query = request.GET.get('author')
        date_min_query = request.GET.get('date_min')
        date_max_query = request.GET.get('date_max')
        room_query = request.GET.get('room')
        time_min_query = request.GET.get('time_min')
        time_max_query = request.GET.get('time_max')
        if is_valid_queryparam(title_contains_query):
            qs = qs.filter(title__icontains=title_contains_query)

        if is_valid_queryparam(author_query):
            qs = qs.filter(author__username__icontains=author_query)

        if is_valid_queryparam(date_min_query):
            qs = qs.filter(date__gte=date_min_query)

        if is_valid_queryparam(date_max_query):
            qs = qs.filter(date__lte=date_max_query)

        if is_valid_queryparam(room_query) and room_query != 'Wybierz salę':
            number, floor = get_room_elements(room_query)
            qs = qs.filter(room__number=number).filter(room__floor=floor)

        if is_valid_queryparam(time_min_query):
            qs = qs.filter(start_time__gte=time_min_query)

        if is_valid_queryparam(time_max_query):
            qs = qs.filter(end_time__lte=time_max_query)

        return render(request, 'meetings/search_form.html',
                      context={
                          'queryset': qs,
                          'rooms': rooms})


def edit_object(request, id):
    obj = Meeting.objects.get(id=id)
    form = MeetingForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.instance.author = request.user
        meeting = form.save()
        messages.success(request, 'Zaktualizowano spotkanie')
        return redirect("index", id=meeting.pk)
    else:
        context = {'form': form, 'error': 'Nie udało się zaktualizować spotkania'}
        return render(request, "meetings/edit.html", context)


def delete_object(request, id):
    meeting = Meeting.objects.get(id=id)
    if request.method == 'POST':
        meeting.delete()
        return redirect("confirmation")
    return render(request, "meetings/delete.html",
                  context={"meeting":meeting})


def confirm_delete(request):
    return render(request, "meetings/confirmation.html")

