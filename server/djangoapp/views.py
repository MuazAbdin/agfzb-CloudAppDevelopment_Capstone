from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_by_id, get_dealers_by_state,\
                      get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        
        context['message'] = "Invalid username or password. Sign-up if you have not yet."
        return render(request, 'djangoapp/registration.html', context)
    
    return render(request, 'djangoapp/registration.html', context)  

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    
    if request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")

        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        
        context['message'] = "User already exists."
        return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request, **kwargs):
    context = {}
    if request.method == "GET":
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/56f3b8d0-67b3-486d-a25b-d042a169fabe/dealership-package/get-dealership"
        context['dealerships'] = get_dealers_from_cf(url)
        # context['dealerships'] = get_dealer_by_id(url, dealer_id=4)
        # context['dealerships'] = get_dealers_by_state(url, dealer_state='CA')
        # url = "https://us-south.functions.appdomain.cloud/api/v1/web/56f3b8d0-67b3-486d-a25b-d042a169fabe/dealership-package/get-review"
        # context['dealerships'] = get_dealer_reviews_from_cf(url, 15)
        
    return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/56f3b8d0-67b3-486d-a25b-d042a169fabe/dealership-package/get-dealership"
        dealer = get_dealer_by_id(dealer_url, dealer_id=dealer_id)[0]
        context["dealer"] = dealer

        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/56f3b8d0-67b3-486d-a25b-d042a169fabe/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id=dealer_id)
        print(reviews)
        context["reviews"] = reviews

    return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {}
    dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/56f3b8d0-67b3-486d-a25b-d042a169fabe/dealership-package/get-dealership"
    dealer = get_dealer_by_id(dealer_url, dealer_id=dealer_id)[0]
    context["dealer"] = dealer
    
    if request.method == 'GET':
        # Get cars for the dealer
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            # print(request.POST)
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id) if int(car_id) > 0 else None
            
            payload = {
                'time': datetime.utcnow().isoformat(),
                'name': username,
                'id': car_id,
                'dealership': dealer_id,
                'review': request.POST["content"],
                'purchase': "purchasecheck" in request.POST and request.POST["purchasecheck"] == 'on',
                'purchase_date': request.POST["purchasedate"] if "purchasedate" in request.POST else '',
                'car_make': car.car_make.name if car else '',
                'car_model': car.name if car else '',
                'car_year': int(car.year.strftime("%Y")) if car else ''
            }

            new_payload = {'review': payload}
            review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/56f3b8d0-67b3-486d-a25b-d042a169fabe/dealership-package/post-review"
            post_request(review_url, new_payload, id=dealer_id)
            
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


