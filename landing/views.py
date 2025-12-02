from django.http import HttpResponse
from django.shortcuts import render
from datetime import date

# Create your views here.
def home(request):
    today = date.today()
    stack = [
        {'id': 'python', 'name': 'Pythod'},
        {'id': 'django', 'name': 'Django'},
        {'id': 'golang', 'name': 'Golang'},
        {'id': 'php', 'name': 'PHP'},
        {'id': 'js', 'name': 'JS'},
    ]
    return render(request, "landing/landing.html", {
        "name": "Carlos",
        "age": 26,
        "today": today,
        "stack": stack,
    })
    
def stack_detail(request, tool):
    return HttpResponse(f"Tecnología: {tool}")