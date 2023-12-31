from django.urls import path
from . import views

app_name = "booking"
urlpatterns = [path("", views.index, name="index"),
               # path("bruh/<str:text>/", views.bruh, name="bruh"),
               path("bruh/", views.IndexView.as_view(), name='bruh'),
               path("schedule/<int:week>/", views.show_schedule, name="schedule"),
               path("schedule/choice/<int:week>/", views.book_slot, name="book_slot"),
               path("schedule/booked/<str:user_info>/", views.confirm_booking, name="confirm_booking")]
