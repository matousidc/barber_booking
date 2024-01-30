from django.urls import path
from . import views

app_name = "booking"
urlpatterns = [path("", views.IndexView.as_view(), name="index"),
               path("bruh/", views.BruhView.as_view(), name='bruh'),
               path("schedule/<int:week>/", views.ShowSchedule.as_view(), name="schedule"),
               path("schedule/choice/", views.BookSlot.as_view(), name="book_slot"),
               path("schedule/booked/<str:user_info>/", views.ConfirmBooking.as_view(), name="confirm_booking")]
