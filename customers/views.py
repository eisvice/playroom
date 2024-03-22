import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse
from customers.models import User, Playground, ChildMock
from datetime import datetime, timedelta
from django.template.loader import render_to_string
from django import forms

from .models import User


class Customer:
    id_counter = 5
    
    def __init__(self, gender="male", customer_type="newcommer"):
        Customer.id_counter += 1
        self.id = Customer.id_counter
        self.gender = gender
        self.customer_type = customer_type
        self.name = customer_type.capitalize()
        self.hours = 10
        self.start_time = datetime.now()
        self.status = "active"
        self.update_duration_and_time()
        
    def update_duration_and_time(self):
        self.duration = str(timedelta(seconds=self.hours)).zfill(8)
        self.end_time = self.start_time + timedelta(seconds=self.hours)
        
    def add_hour(self):
        self.hours += 10
        self.update_duration_and_time()

    def change_time(self, hours, minutes, seconds):
        total_duration = hours*3600 + minutes*60 + seconds
        self.hours = total_duration
        self.update_duration_and_time()
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "customer_type": self.customer_type,
            "duration": self.duration,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
        }

    def __str__(self):
        return f"Customer: id={self.id}, gender={self.gender}, is_new_customer={self.customer_type}, hours={self.hours}, duration={self.duration}, start_time={self.start_time}, end_time={self.end_time}, status={self.status}"

GENDER_CHOICES = ["Male", "Female"]
CUSTOMER_TYPE_CHOICES = ["Newcommer", "Loyal"]
DURATION_CHOICES = {
    "0.5": "30 min",
    "1": "1 hour",
    "2": "2 hour",
    "3": "3 hour",
    "4": "4 hour",
    "5": "5 hour",
    "6": "6 hour",
    "7": "7 hour",
}

class CustomerForm(forms.Form):
    name = forms.CharField(label="Your name")
    # gender = forms.ChoiceField(choices=GENDER_CHOICES)
    # customer_type = forms.ChoiceField(choices=CUSTOMER_TYPE_CHOICES)
    # duration = forms.ChoiceField(choices=DURATION_CHOICES)
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()

c1 = Customer()
c1.id = 1
c1.gender = "male"
c1.customer_type = "newcommer"
c1.name = "John"
c1.hours = 60
c1.duration = "00:01:00"
c1.start_time = "2024-03-22T17:38:59.254704"
c1.end_time = "2024-03-22T17:39:59.254704"
c1.status = "await"

c2 = Customer()
c2.id = 2
c2.gender = "male"
c2.customer_type = "loyal"
c2.name = "Bob"
c2.hours = 10
c2.duration = "00:00:10"
c2.start_time = "2024-03-22T17:40:00.254704"
c2.end_time = "2024-03-22T17:40:10.254704"
c2.status = "await"

c3 = Customer()
c3.id = 3
c3.gender = "female"
c3.customer_type = "newcommer"
c3.name = "Mag"
c3.hours = 30
c3.duration = "00:00:30"
c3.start_time = "2024-03-22T17:40:10.254704"
c3.end_time = "2024-03-22T17:40:40.254704"
c3.status = "await"

c4 = Customer()
c4.id = 4
c4.gender = "female"
c4.customer_type = "loyal"
c4.name = "Jane"
c4.hours = 20
c4.duration = "00:00:20"
c4.start_time = "2024-03-22T17:40:59.254704"
c4.end_time = "2024-03-22T17:41:19.254704"
c4.status = "await"

c5 = Customer()
c5.id = 5
c5.gender = "female"
c5.customer_type = "newcommer"
c5.name = "Alice"
c5.hours = 60
c5.duration = "00:01:00"
c5.start_time = "2024-03-22T17:41:59.254704"
c5.end_time = "2024-03-22T17:42:59.254704"
c5.status = "await"


customer = ''
customers = [c1, c2, c3, c4, c5]

def index(request):
    global customers, customer
    if request.method == "POST":
        if "add-new-boy" in request.POST:
            customer = Customer(gender="male", customer_type="newcommer")
        elif "add-new-girl" in request.POST:
            customer = Customer(gender="female", customer_type="newcommer")
        elif "add-old-boy" in request.POST:
            customer = Customer(gender="male", customer_type="loyal")
        elif "add-old-girl" in request.POST:
            customer = Customer(gender="female", customer_type="loyal")
        customers.append(customer)

        context = {"count": customers}
        print(request.POST)
        print(customers)
        for c in customers:
            print(c)
        button_group_html = render_to_string("customers/buttongroup.html")
        customer_html = render_to_string("customers/oob-customer.html", {"c": customer})
        
        return HttpResponse(button_group_html + customer_html)
    for c in customers:
        print(c)
    context = {"count": customers}
    return render(request, "customers/index.html", context)


def delete_customer(request, id):
    for c in customers:
        if c.id == id:
            customers.remove(c)
            break
    for c in customers:
        print(c)
    return HttpResponse(f"Deleted {id}", status=200)


def add_hour(request, id):
    for c in customers:
        if c.id == id:
            c.add_hour()
            end_time = c.duration
            break
        print(c)
    return HttpResponse(f"{end_time}", status=200)


def delete_customers(request):
    global customers
    if request.method == "POST":
        if "clear" in request.POST:
            Customer.id_counter = 0
            customers = []
    return render(request, "customers/customers.html")


def find_customer(request, id):
    global customers
    if request.method == "GET":
        for c in customers:
            if id == c.id:
                customer = c
                break
        return JsonResponse(c.serialize(), status=200)
    elif request.method == "POST":
        data = json.loads(request.body)
        print(data)
        if len(data) == 1 and data["status"]:
            for c in customers:
                if id == c.id:
                    c.status = data["status"]
                    break
            return JsonResponse({"message": f"User has status '{c.status}'"}, status=201)
        else:
            duration_str = data["duration"]
            time_obj = datetime.strptime(duration_str, "%H:%M:%S")
            for c in customers:
                if id == c.id:
                    customer = c
                    c.name = data["name"]
                    c.gender = data["gender"]
                    c.customer_type = data["customer_type"]
                    c.duration = time_obj.second
                    c.change_time(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)
                    break
            # return JsonResponse({"message": "User information has been updated"}, status=201)
            # return JsonResponse({"message": f"User inforamtion has been updated"}, status=201)
            context = {"count": customers}
            return render(request, "customers/index.html", context)


def finish(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST is allowed"}, status=422)
    for c in customers:
        if c.id == id:
            c.status = 'finished'
            break
        print(c)
    return HttpResponse(f"User {c.id} has finished", status=200)


# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "customers/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "customers/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "customers/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "customers/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "customers/register.html")