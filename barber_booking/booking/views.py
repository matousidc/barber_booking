import os
from dotenv import load_dotenv
import requests
from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from datetime import datetime
from .models import TimeSlot, User

load_dotenv(override=True)
FASTAPI_URL = os.getenv("BACKEND_URL")


# Create your views here.
def index(request):
    """Shows schedule for current week"""
    week_num = datetime.now().strftime("%W")
    return HttpResponseRedirect(reverse("booking:schedule", args=(week_num,)))


# def bruh(request, text):
#     return HttpResponse("you don't compare %s" % text)

class IndexView(generic.ListView):
    model = User
    template_name = "booking/index.html"
    context_object_name = "context"


def show_schedule(request, week: int):
    """Shows schedule for a given week as a html template"""
    # selected_choice = User.email.get(pk=request.POST["email"])
    schedule = get_list_or_404(TimeSlot, week=week)  # raises exception by itself
    context = {"is_booked": ["Booked" if x.booked_slot else "Available" for x in schedule][:5], "week": week}
    return render(request, "booking/schedule.html", context=context)


def book_slot(request, week: int):
    """Gets values from template, books slot in database"""
    # values from html template
    name = request.POST["name"]
    email = request.POST["email"]
    day_idx = request.POST["selected_day"]
    time_slot = TimeSlot.objects.get(day=day_idx, week=week)
    # request to book_slot api

    user_info = {"name": name, "email": email}
    r = requests.put(f"{FASTAPI_URL}/book_slot/?time_slot_id={time_slot.id}", json=user_info)
    print(r.json())
    return HttpResponseRedirect(reverse("booking:confirm_booking", args=(r.json(),)))


def confirm_booking(request, user_info: str):
    return render(request, "booking/index.html", context={"context": user_info})
