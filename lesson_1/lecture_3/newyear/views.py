import datetime

from django.shortcuts import render

# Create your views here.
def index(request):
    now = datetime.datetime.now() #actual day
    return render(request, "newyear/index.html", {
        "newyear": now.month == 1 and now.day == 1 #newyear day
    })
