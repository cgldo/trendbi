from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting, FindTrend
from .Main import *
# Create your views here.
def index(request):
    
    if request.method == 'POST':
        # create an instance of our form, and fill it with the POST data
        form = FindTrend(request.POST)

        if form.is_valid():
            message=form.cleaned_data['search_term']
            plot_div = get_graph([message])
    # if the form is not valid, we let execution continue to the return
    # statement below, and display the form again (with errors).

    else:
    # this must be a GET request, so create an empty form
        new_form = FindTrend()
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html", {'form': new_form, 'plot_div': plot_div}) 


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
