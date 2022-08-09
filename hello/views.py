from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, FindTrend
from .Main import *
import re

# Create your views here.
def index(request):
    plot_div = ['<body></body>', ['<body></body>', '<body></body>']]
    if request.method == 'POST':
        # create an instance of our form, and fill it with the POST data
        message = [x.strip() for x in re.split(',+', request.POST.get('Term'))]
        start = request.POST.get('Start')
        end = request.POST.get('End')
        google = request.POST.get('google')
        youtube = request.POST.get('youtube')
        twitter = request.POST.get('twitter')
        numbers = int(request.POST.get('numbers'))
        plot_div = get_graph(message, start + " " + end, google, youtube, twitter, numbers)
    # if the form is not valid, we let execution continue to the return
    # statement below, and display the form again (with errors).

    else:
    # this must be a GET request, so create an empty form
        new_form = FindTrend()
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html", {'plot_div': plot_div[0], 'twitter_plot1': (plot_div[1])[0], 'twitter_plot2': (plot_div[1])[1]}) 


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
