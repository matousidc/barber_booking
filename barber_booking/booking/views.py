# run with: python manage.py runserver 8080
import os
import json
from dotenv import load_dotenv
import requests
from django import forms
from django.shortcuts import render, get_list_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic, View
from datetime import datetime
from .models import TimeSlot, User

load_dotenv(override=True)
FASTAPI_URL = os.getenv("BACKEND_URL")


# Create your views here.
class IndexView(generic.View):
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


class BookingForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    selected_day = forms.IntegerField()


class ShowSchedule(generic.View):
    """Shows schedule for a given week as a html template"""
    template_name = "booking/schedule.html"

    def get(self, request, week: int):
        schedule = get_list_or_404(TimeSlot, week=week)  # raises exception by itself
        context = {"is_booked": ["Booked" if x.booked_slot else "Available" for x in schedule][:5], "week": week}
        return render(request, self.template_name, context=context)


class BookSlot(View):
    form_class = BookingForm

    def post(self, request, week: int):
        form = self.form_class(request.POST)
        print(form.__dict__)
        if form.is_valid():
            # print("==========================================", form.day_idx)
            time_slot = TimeSlot.objects.get(day=form.cleaned_data['selected_day'], week=week)
            # request to book_slot API endpoint
            user_data = {"name": form.cleaned_data['name'], "email": form.cleaned_data['email']}
            r = requests.put(f"{FASTAPI_URL}/book_slot/?time_slot_id={time_slot.id}", json=user_data)
            user_info = r.json()
            user_info.pop("user_id")
            user_info.pop("id")
        else:
            raise Http404("Submitted form is broken, go back end try again")
        return redirect("booking:confirm_booking", user_info=user_info)


class ConfirmBooking(generic.View):
    template_name = "booking/booking_confirmed.html"

    def get(self, request, *args, **kwargs):
        user_info = self.kwargs["user_info"]
        user_info = json.dumps(user_info)
        return render(request, self.template_name, context={"context": user_info})
