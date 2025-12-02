# from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse

DAYS_QUOTES = {
    "monday": "El éxito es la suma de pequeños esfuerzos repetidos día tras día.",
    "tuesday": "La única forma de hacer un gran trabajo es amar lo que haces.",
    "wednesday": "No cuentes los días, haz que los días cuenten.",
    "thursday": "El fracaso es la oportunidad de comenzar de nuevo con más inteligencia.",
    "friday": "La vida es 10% lo que me ocurre y 90% cómo reacciono a ello.",
    "saturday": "No esperes. El tiempo nunca será justo.",
    "sunday": "Cree que puedes y ya estás a mitad de camino."
}

def index(request):
    list_items = ""
    days = list(DAYS_QUOTES.keys())

    for day in days:
        day_url = reverse("day-quote", args=[day])
        list_items += f"<li><a href='{day_url}'>{day.title()}</a></li>"

    response_data = f"<ul>{list_items}</ul>"
    return HttpResponse(response_data)

def home(request):
    return render(request, 'quotes/quotes.html', {
        "days": list(DAYS_QUOTES.keys())
    })

def days_week_whith_number(request, day):
    days = list(DAYS_QUOTES.keys())
    if day > len(days) or day < 1:
        return HttpResponseNotFound("<h1>El día no existe</h1>")
    redirect_day = days[day - 1]
    redirect_url = reverse("day-quote", args=[redirect_day])
    return HttpResponseRedirect(redirect_url)


def days_week(request, day):
    try:
        quote_text = DAYS_QUOTES[day.lower()]
        return HttpResponse(quote_text)
    except KeyError:
        raise Http404()