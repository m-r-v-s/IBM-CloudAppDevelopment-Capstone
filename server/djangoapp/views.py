from functools import reduce
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarDealer, CarModel, CarMake, DealerReview
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.views import generic
import logging
import json
from .restapis import get_dealers_from_cf, get_dealer_from_cf_by_id,\
     get_dealer_reviews_from_cf, post_request
from requests import request
import datetime




logger = logging.getLogger(__name__)



def about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


def contact(request):
    return render(request, 'djangoapp/contact.html')



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



def logout_request(request):
        logout(request)
        return redirect('djangoapp:index')
    

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



def get_dealerships(request):
    context = dict()
    dealerID_parameter = request.GET.get('dealerID', None)
    state_parameter = request.GET.get('state', None)
    if request.method == "GET" and dealerID_parameter is not None:
        url = "https://fb5ccb64.eu-de.apigw.appdomain.cloud/api/dealerships"
        dealership = get_dealer_from_cf_by_id(url, dealer_id = dealerID_parameter)
        context["dealership"] = dealership
        dealer_name = dealership.short_name
        return render(request, 'djangoapp/index.html', context=context)
    elif request.method == "GET" and state_parameter is not None:
        url = "https://fb5ccb64.eu-de.apigw.appdomain.cloud/api/dealerships"
        dealerships = get_dealers_from_cf(url, state = state_parameter)
        context["dealerships"] = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return render(request, 'djangoapp/index.html', context=context)
    elif request.method == "GET":
        url = "https://fb5ccb64.eu-de.apigw.appdomain.cloud/api/dealerships"
        dealerships = get_dealers_from_cf(url)
        context["dealerships"] = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return render(request, 'djangoapp/index.html', context=context)


def get_dealer_details_query(request):
    context = dict()
    if request.method == "GET":
        dealerID_parameter = request.GET.get("dealerID")
        context["dealerID"] = dealerID_parameter
        url = "https://fb5ccb64.eu-de.apigw.appdomain.cloud/api/reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealerID = int(dealerID_parameter))
        review_contents = []
        for review_obj in dealer_reviews:
           review_contents.append(' \n'.join("Review:" + review_obj.review + "\tSentiment:" + review_obj.sentiment))
        context["dealer_reviews"] = dealer_reviews
        return render(request, 'djangoapp/dealer_details.html', context)

def get_dealer_details_url(request, dealerID):
    context = dict()
    if request.method == "GET":
        if not dealerID:
            dealerID_parameter = request.GET.get("dealerID")
        else:
            dealerID_parameter = int(dealerID) #= request.GET.get("dealerID", None) | 
            context["dealerID"] = dealerID_parameter
        url = "https://fb5ccb64.eu-de.apigw.appdomain.cloud/api/reviews"
        dealer_reviews = get_dealer_reviews_from_cf(url, dealerID = dealerID_parameter)
        review_contents = []
        for review_obj in dealer_reviews:
           review_contents.append(' \n'.join("Review:" + review_obj.review + "\tSentiment:" + review_obj.sentiment))
        context["dealer_reviews"] = dealer_reviews
        return render(request, 'djangoapp/dealer_details.html', context)

def add_review(request, dealerID):
    context = dict()
    review = dict()
    api_url = "https://fb5ccb64.eu-de.apigw.appdomain.cloud/api/reviews/post"
    current_user = request.user
    time_ = datetime.date.today().isoformat()
    if request.method == "GET" and current_user.is_authenticated:
        cars = CarModel.objects.all()
        context["cars"] = cars
        context["dealerID"] = dealerID
        print(context)
        return render(request, 'djangoapp/add_review.html', context)

    elif request.method == "POST" and current_user.is_authenticated:
        form = request.POST
        review["dealerID"] = dealerID
        if form["purchasecheck"] == "on":
            review["purchase"] = True
            review["content"] = form["content"]
            review["car"] = form["car"]
            review["date"] = form["purchasedate"]
            review["time"] = time_
        else:
            review["purchase"] = False
            review["content"] = form["content"]
            review["time"] = time_
        result = post_request(url = api_url, json_payload=review)
        print(result)
        return redirect('djangoapp:details-url', dealerID = dealerID)
