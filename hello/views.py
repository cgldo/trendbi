from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
from hello import form
# Create your views here.
def index(request):
    new_form = form()
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html", {'form': new_form}) 


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
