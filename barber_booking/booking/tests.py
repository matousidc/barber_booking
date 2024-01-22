# python manage.py test booking
from django.test import TestCase
from django.urls import reverse
from .models import TimeSlot, User


def create_single_timeslot():
    time_slot = TimeSlot(1, 2023, 48, 1, 0)
    time_slot.save()


# Create your tests here.
class ShowScheduleViewTests(TestCase):
    def test_one_timeslot(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        create_single_timeslot()
        time_slots = TimeSlot.objects.filter(week=48)
        print(time_slots)
        print(time_slots[0].id)
        response = self.client.get(reverse("booking:schedule", args=(48,)))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No polls are available.")
        self.assertEqual(response.context["week"], 48)
        self.assertEqual(len(response.context["is_booked"]), len(time_slots))
