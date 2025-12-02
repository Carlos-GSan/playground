from django.urls import path
from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("", views.index),
    path("<int:day>", views.days_week_whith_number),
    path("<str:day>", views.days_week, name="day-quote"),
]
