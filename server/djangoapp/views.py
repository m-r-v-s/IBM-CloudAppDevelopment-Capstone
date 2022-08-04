from functools import reduce
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.views import generic
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
# class IndexView(generic.ArchiveIndexView):
#     template_name = "djangoapp/index.html"
#     context_object_name = 'index'

# Create an `about` view to render a static about page
def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')
# Create a `login_request` view to handle sign in request



def login_request(request):
    context = {}
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username = username, password = password)

    if user is not None:
        login(request,user)
        return redirect('djangoapp:index')
    else:
        context['message'] = "Invalid username or password."
        return render(request, 'djangoapp/login.html', context)



# Create a `logout_request` view to handle sign out request
def logout_request(request):
        logout(request)
        return redirect('djangoapp:index')
    

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == "GET": 
        return render(request, 'djangoapp/registration.html', context)
    else:
        user_exists = False
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username = username)
            user_exists = False
        except:
            logger.error("Registration Procedure Failure. Repeat.")
        if not user_exists:
            user = User.objects.create_user(username = username, password = password, first_name = first_name, last_name = last_name)
            login(request,user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "User already exists."
            return render(request,'djangoapp/registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    else:
        return redirect('djangoapp:index')


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

