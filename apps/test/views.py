from django.shortcuts import render
import pytz
from datetime import datetime


def welcome(request):
    return render(request, "/test/templates/welcome.html")


def users_list(request):
    users = [{"name": "Arun", "age": 20}, {"name": "Katy", "age": 25},
             {"name": "Ken", "age": 35}]
    return render(request, "/test/templates/users.html", {"users": users})


def city_time(request):
    city = request.GET.get("city", "UTC")
    timezones = {
        "Almaty": "UTC+6",
        "Calgary": "UTC-7",
        "Moscow": "UTC+3",
        "UTC": "UTC+0",
    }
    tz = pytz.timezone(timezones.get(city, "UTC"))
    current_time = datetime.now(tz)
    return render(request, "/test/templates/city_time.html",
                  {"city": city, "time": current_time,
                   "cities": timezones.keys()})


def counter(request):
    cnt = request.session.get("cnt", 0)
    if "increment" in request.GET:
        cnt += 1
    elif "reset" in request.GET:
        cnt = 0
    request.session["cnt"] = cnt
    return render(request, "/test/templates/counter.html", {"cnt": cnt})
