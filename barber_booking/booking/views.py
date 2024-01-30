# run with: python manage.py runserver 8080
import os
import json
from dotenv import load_dotenv
import requests
from django import forms
from django.shortcuts import render, get_list_or_404, redirect
from django.http import Http404
from django.urls import reverse
from django.views import generic, View
from django.views.generic.edit import FormView
from datetime import datetime
from .models import TimeSlot, User

load_dotenv(override=True)
FASTAPI_URL = os.getenv("BACKEND_URL")


# Create your views here.
class IndexView(View):
    """Shows schedule for current week"""

    def get(self, request):
        week_num = datetime.now().strftime("%W")
        return redirect("booking:schedule", week=week_num)


class BruhView(generic.ListView):
    # model = User
    template_name = "booking/index.html"
    context_object_name = "context"

    def get_queryset(self):
        return User.objects.all()


class ShowSchedule(View):
    """Shows schedule for a given week as a html template"""
    template_name = "booking/schedule.html"

    def get(self, request, week: int):
        schedule = get_list_or_404(TimeSlot, week=week)  # raises exception by itself
        context = {"is_booked": ["Booked" if x.booked_slot else "Available" for x in schedule][:5], "week": week}
        return render(request, self.template_name, context=context)


class BookingForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    selected_day = forms.IntegerField()
    week_idx = forms.IntegerField()


class BookSlot(FormView):
    """Makes request to book_slot endpoint with data extracted from form"""
    form_class = BookingForm

    def form_valid(self, form):
        # expects form sent with POST
        time_slot = TimeSlot.objects.get(day=form.cleaned_data['selected_day'], week=form.cleaned_data["week_idx"])
        # request to book_slot API endpoint
        user_data = {"name": form.cleaned_data['name'], "email": form.cleaned_data['email']}
        r = requests.put(f"{FASTAPI_URL}/book_slot/?time_slot_id={time_slot.id}", json=user_data)
        user_info = r.json()
        user_info.pop("user_id")
        user_info.pop("id")
        return redirect("booking:confirm_booking", user_info=user_info)

    def form_invalid(self, form):
        raise Http404("Submitted form is broken, go back end try again")


class ConfirmBooking(View):
    """After successfully booking a slot, redirects here"""
    template_name = "booking/booking_confirmed.html"

    def get(self, request, *args, **kwargs):
        user_info = self.kwargs["user_info"]
        user_info = json.dumps(user_info)
        return render(request, self.template_name, context={"context": user_info})
