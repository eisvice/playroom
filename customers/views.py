import calendar
import json
from json import JSONDecodeError
from django.views.generic import ListView
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from customers.models import User, Playground, Customer, PlaygroundDetail
from django.template.loader import render_to_string
from django.db.models import Min, Max, Sum, Q
from django.views.decorators.http import require_POST, require_safe
from datetime import datetime, timedelta, date


class Customer1:
    id_counter = 100
    
    def __init__(self, gender="male", customer_type="newcommer"):
        Customer1.id_counter += 1
        self.id = Customer1.id_counter
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
        return f"Customer1: id={self.id}, gender={self.gender}, is_new_customer={self.customer_type}, hours={self.hours}, duration={self.duration}, start_time={self.start_time}, end_time={self.end_time}, status={self.status}"


customer = ''
customers = []


class HistoryDayView(ListView):
    model = PlaygroundDetail
    template_name = "customers/history.html"
    context_object_name = "customs"
    paginate_by = 5
    ordering = "-date"
    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "customers/history-list.html"
        else:
            return self.template_name
        

"""HOME PAGE VIEWS"""
def index(request):
    customers = Customer.objects.filter(Q(status='active') | Q(status='await'))
    context = {"count": customers}
    return render(request, "customers/index.html", context)

@require_POST
def add_customer(request):
    if request.POST["add-customer"]:
        post_string_value = request.POST["add-customer"]
        pairs = post_string_value.split("&")
        new_customer = {}
        for pair in pairs:
            key, value = pair.split("=")
            new_customer[key] = value
        if (new_customer["gender"] == "male" or new_customer["gender"] == "female") and (new_customer["customer_type"] == "newcomer" or new_customer["customer_type"] == "returning"):
            if not PlaygroundDetail.objects.filter(date=date.today()):
                PlaygroundDetail.objects.create(
                    playground = Playground.objects.get(pk=request.user.id),
                    user = request.user
                )
            playground_detail = PlaygroundDetail.objects.filter(date=date.today(), user=request.user)[0]
            customer = Customer(
                gender = new_customer["gender"],
                customer_type = new_customer["customer_type"],
                playground = playground_detail.playground,
                playground_detail = playground_detail
            )
            customer.cost = float(playground_detail.rate) * customer.hours
            customer.save()

            button_group_html = render_to_string("customers/buttongroup.html")
            customer_html = render_to_string("customers/oob-customer.html", {"c": customer})
            return HttpResponse(button_group_html + customer_html)
    return HttpResponseBadRequest("Some button returned invalid data")
        
@require_POST
def delete_customer(request, id):
    customer = Customer.objects.get(pk=id)
    customer.delete()
    return HttpResponse(f"Deleted {id}", status=200)

@require_POST
def add_hour(request, id):
    customer = Customer.objects.get(pk=id)
    customer.hours += 1
    customer.end_time = customer.start_time + timedelta(hours=float(customer.hours))
    customer.save(update_fields=["hours", "end_time"])
    return HttpResponse(f"{str(timedelta(hours=float(customer.hours))).zfill(8)}", status=200)

def update_info(request, id):
    global customers
    if request.method == "GET":
        customer = Customer.objects.get(pk=id)
        return JsonResponse(customer.serialize(), status=200)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            print(data)
        except JSONDecodeError:
            data = ""
        if len(data) == 1 and data["status"]:
            for c in customers:
                if id == c.id:
                    c.status = data["status"]
                    break
            return JsonResponse({"message": f"User has status '{c.status}'"}, status=201)
        elif len(data) > 1:
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
            context = {"count": customers}
            return render(request, "customers/index.html", context)

@require_POST
def finish(request, id):
    customer = Customer.objects.get(pk=id)
    playground_detail = PlaygroundDetail.objects.filter(id=customer.playground_detail.id, user=request.user)[0]
    customer.status = "finished"
    customer.cost = float(customer.hours * playground_detail.rate)
    customer.save(update_fields=["status", "cost"])
    customers_day_total = Customer.objects.filter(playground_detail=playground_detail, status="finished").aggregate(Sum("cost"))
    playground_detail.total_amount = float(customers_day_total["cost__sum"])
    playground_detail.save(update_fields=["total_amount"])
    return HttpResponse(f"User {customer.name} has finished", status=200)


"""HISTORY PAGE VIEWS"""
@require_safe
def history_detail(request, id):
    playground_detail = PlaygroundDetail.objects.get(pk=id)
    rows = Customer.objects.filter(playground_detail=playground_detail, status="finished").order_by("-end_time")
    print(playground_detail.id)
    return render(request, "customers/history-detail.html", {"rows": rows})

@require_POST
def history_update_details(request, id):
    customer = Customer.objects.get(pk=id)
    playground_detail = PlaygroundDetail.objects.get(id=customer.playground_detail.id)
    try:
        price = float(request.POST["price"])
        if price > 0:
            customer.cost = price
            customer.save(update_fields=["cost"])
            customers_day_total = Customer.objects.filter(playground_detail=playground_detail, status="finished").aggregate(Sum("cost"))
            playground_detail.total_amount = float(customers_day_total["cost__sum"])
            playground_detail.save(update_fields=["total_amount"])
        else:
            error = "Price must be greater than 0"
    except ValueError:
        error = "Price must be numeric"
    if 'error' in locals():
        return render(request, "customers/history-list.html", {"customs": [playground_detail], "error": error})
    return render(request, "customers/history-list.html", {"customs": [playground_detail]})
    

"""CHART PAGE VIEWS"""
@require_safe
def charts_view(request):
    details_min_date = PlaygroundDetail.objects.aggregate(Min("date"))
    details_max_date = PlaygroundDetail.objects.aggregate(Max("date"))
    details_min_date_month = details_min_date["date__min"].month
    details_max_date_month = details_max_date["date__max"].month
    today = datetime.today()

    gender_set = Customer.objects.filter(end_time__month=today.month, end_time__year=today.year, status='finished')
    newcomer_f = newcomer_m = returning_f = returning_m = 0
    for g in gender_set:
        if g.customer_type == "newcomer" and g.gender == "female":
            newcomer_f += 1
        elif g.customer_type == "newcomer" and g.gender == "male":
            newcomer_m += 1
        elif g.customer_type == "returning" and g.gender == "female":
            returning_f += 1
        elif g.customer_type == "returning" and g.gender == "male":
            returning_m += 1
    gender_set_count = [newcomer_f, newcomer_m, returning_f, returning_m]                
    
    query_set = PlaygroundDetail.objects.filter(date__month=today.month, date__year=today.year)
    query_set_dates = []
    query_set_price = []
    for q in query_set:
        query_set_dates.append(q.date)
        query_set_price.append(q.total_amount)
    cal = calendar.Calendar()
    cal_list = []
    cal_sum = []
    for i in cal.itermonthdates(today.year, today.month):
        if i.month == today.month:
            cal_list.append(i.day)
            try:
                k = query_set_dates.index(i)
                cal_sum.append(float(query_set_price[k]))
            except ValueError:
                cal_sum.append(0)
    return render(request, "customers/charts.html", {
        "cal_list": cal_list,
        "cal_sum": cal_sum,
        "gender_set_count": gender_set_count,
        "gender_set": gender_set,
        "today": today,
    })


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