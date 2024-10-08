import json
import calendar
from json import JSONDecodeError
from django.utils import timezone
from datetime import timedelta, date
from django.db import IntegrityError
from django.db.models import Min, Sum, Q
from django.core.paginator import Paginator
from django.urls import reverse, reverse_lazy
from .forms import CustomerForm, CustomerModelForm
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST, require_safe
from customers.models import User, Playground, Customer, PlaygroundDetail
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponseForbidden


class ChangePasswordView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "customers/change-password.html"
    success_url = reverse_lazy("index")


"""HOME PAGE VIEWS"""
def index(request):
    # Get the current time zone from a browser
    current_tz = timezone.get_current_timezone()
    print("time zone in the index view", current_tz)
    if request.user.is_authenticated and not request.user.is_permission_given:
        return render(request, "customers/index.html", {"message": "Please wait untill you are being given a permission to see this site"})
    elif request.user.is_authenticated:
        context = {"server_tz": current_tz}
        return render(request, "customers/index.html", context)
    else:
        return HttpResponseRedirect("login")
    
def customers_list(request):
    customers = Customer.objects.filter(playground=request.user.playground.id).filter(Q(status='active') | Q(status='await'))
    context = {"customers": customers}
    return render(request, "customers/customers.html", context)
    
def edit_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)
    if request.method == "POST":
        form = CustomerModelForm(request.POST, instance=customer)
        if form.is_valid():
            customer_info = form.save(commit=False)
            customer_info.end_time = customer_info.start_time + timedelta(hours=float(customer_info.hours))
            if customer.bank == "":
                customer.bank = None
            customer_info.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': "customerChanged"
                }
            )
    else:
        form = CustomerModelForm(instance=customer)
    return render(request, 'customers/customer-form.html', {
        'form': form,
        'customer': customer,
    })

@require_POST
def add_customer(request):
    if request.POST["add-customer"]:
        post_string_value = request.POST["add-customer"]
        pairs = post_string_value.split("&")
        playground = Playground.objects.get(pk=request.user.playground.id)
        new_customer = {}
        for pair in pairs:
            key, value = pair.split("=")
            new_customer[key] = value
        if (new_customer["gender"] == "male" or new_customer["gender"] == "female") and (new_customer["customer_type"] == "newcomer" or new_customer["customer_type"] == "returning"):
            if not PlaygroundDetail.objects.filter(date=date.today(), playground=playground):
                print(f"Create a new day instance. Expected date is {date.today()}")
                playground_detail = PlaygroundDetail.objects.create(
                    playground = Playground.objects.get(pk=request.user.playground.id),
                )
                playground_detail.save()
            else:
                print("Date already exists in the db")
                playground_detail = PlaygroundDetail.objects.filter(date=date.today(), playground=playground)[0]
            customer = Customer(
                gender = new_customer["gender"],
                customer_type = new_customer["customer_type"],
                playground = playground,
                playground_detail = playground_detail
            )
            customer.cost = float(playground_detail.rate) * customer.hours
            customer.save()

            button_group_html = render_to_string("customers/buttongroup.html")
            customer_html = render_to_string("customers/oob-customer.html", {"customer": customer})
            return HttpResponse(button_group_html + customer_html)
    return HttpResponseBadRequest("Some button returned invalid data")

@require_POST
def delete_customer(request, id):
    current_tz = timezone.get_current_timezone()
    customer = Customer.objects.get(pk=id)
    customer.status = "deleted"
    customer.end_time = timezone.now().astimezone(current_tz)
    print(f"Deletion time of user {customer.id}-{customer.name} is {customer.end_time}")
    customer.save(update_fields=["status", "end_time"])
    return HttpResponse(f"Deleted {id}", status=200)

@require_POST
def add_hour(request, id):
    customer = Customer.objects.get(pk=id)
    if float(customer.hours) == 0.5:
        customer.hours = float(customer.hours) + 0.5
    else:
        customer.hours += 1
    customer.end_time = customer.start_time + timedelta(hours=float(customer.hours))
    customer.save(update_fields=["hours", "end_time"])
    return HttpResponse(f"{str(timedelta(hours=float(customer.hours))).zfill(8)}", status=200)

def update_info(request, id):
    customer = Customer.objects.get(pk=id)
    if request.method == "GET":
        return JsonResponse(customer.serialize(), status=200)
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            data = ""
        if len(data) == 1 and data["status"]:
            customer.status = data["status"]
            customer.save(update_fields=["status"])
            return JsonResponse({"message": "allright"})

@require_POST
def finish(request, id):
    current_tz = timezone.get_current_timezone()
    customer = Customer.objects.get(pk=id)
    playground = Playground.objects.get(pk=request.user.playground.id)
    playground_detail = PlaygroundDetail.objects.filter(id=customer.playground_detail.id, playground=playground)[0]
    customer.status = "finished"

    if customer.hours == 0.25:
        customer.cost = 200
    elif customer.hours == 0.5:
        customer.cost = 300
    else:
        customer.cost = float(customer.hours * playground_detail.rate)

    if timezone.now().astimezone(current_tz) < customer.end_time:
        customer.end_time = timezone.now().astimezone(current_tz)
        customer.save(update_fields=["status", "cost", "end_time"])
    else:
        customer.save(update_fields=["status", "cost"])

    print(f"Customer {customer.id}-{customer.name} has finished")
    customers_day_total = Customer.objects.filter(playground_detail=playground_detail, status="finished").aggregate(Sum("cost"))
    playground_detail.total_amount = float(customers_day_total["cost__sum"])
    playground_detail.save(update_fields=["total_amount"])
    return HttpResponse(f"User {customer.name} has finished", status=200)


"""HISTORY PAGE VIEWS"""
@require_safe
def history_view(request):
    if request.user.is_owner:
        playground_detail = PlaygroundDetail.objects.filter(playground=request.user.playground).order_by("-date")
    elif request.user.is_permission_given:
        playground_detail = PlaygroundDetail.objects.filter(playground=request.user.playground).order_by("-date")[:1]
    else:
        return HttpResponseRedirect(reverse("index"))
    paginator = Paginator(playground_detail, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.htmx:
        return render(request, "customers/history-list.html", {"page_obj": page_obj})
    else:
        return render(request, "customers/history.html", {"page_obj": page_obj})

@require_safe
def history_detail(request, id):
    playground_detail = PlaygroundDetail.objects.get(pk=id)
    rows = Customer.objects.filter(playground_detail=playground_detail).filter(Q(status='finished') | Q(status='deleted')).order_by("-end_time")
    payment_distro = rows.filter(status='finished').values("bank").annotate(Sum("cost")).order_by()
    return render(request, "customers/history-detail.html", {
        "rows": rows,
        "payment_distro": payment_distro,
        "form": CustomerForm(),
        })

@require_POST
def history_update_details(request, id):
    customer = Customer.objects.get(pk=id)
    playground_detail = PlaygroundDetail.objects.get(id=customer.playground_detail.id)
    try:
        price = float(request.POST["price"])
        payment = request.POST["payment"]
        bank = request.POST.get('bank', None)
        if price > 0:
            customer.cost = price
            customer.payment = payment
            customer.bank = bank
            customer.save(update_fields=["cost", "payment", "bank"])
            customers_day_total = Customer.objects.filter(playground_detail=playground_detail, status="finished").aggregate(Sum("cost"))
            playground_detail.total_amount = float(customers_day_total["cost__sum"])
            playground_detail.save(update_fields=["total_amount"])
        else:
            error = "Price must be greater than 0"
    except ValueError:
        error = "Price must be numeric"
    if 'error' in locals():
        return render(request, "customers/history-list.html", {"page_obj": [playground_detail], "error": error})
    return render(request, "customers/history-list.html", {"page_obj": [playground_detail]})


"""CHART PAGE VIEWS"""
@require_safe
def charts_view(request):
    if request.user.is_authenticated:
        playground = Playground.objects.get(pk=request.user.playground.id)
        details_min_date_dict = PlaygroundDetail.objects.filter(playground=playground).aggregate(Min("date", default=date.today()))
        details_min_date = details_min_date_dict["date__min"]
        today = date.today()
        months = ((today.year - details_min_date.year)*12 + today.month - details_min_date.month)
        months_list = [month for month in range(months+1)]
        paginator = Paginator(months_list, 1)
        page_number = request.GET.get("page")
        try:
            current_date = date(date.today().year, date.today().month-int(page_number)+1, date.today().day)
        except TypeError:
            current_date = today
        page_obj = paginator.get_page(page_number)
        gender_set = Customer.objects.filter(playground=playground, end_time__month=current_date.month, end_time__year=current_date.year, status='finished')
        # customer and gender division piechart
        newcomer_f = gender_set.filter(customer_type="newcomer", gender="female").count()
        newcomer_m = gender_set.filter(customer_type="newcomer", gender="male").count()
        returning_f = gender_set.filter(customer_type="returning", gender="female").count()
        returning_m = gender_set.filter(customer_type="returning", gender="male").count()
        gender_set_count = [newcomer_f, newcomer_m, returning_f, returning_m]
        # payment method piechart
        cash = gender_set.filter(payment="cash").aggregate(Sum("cost", default=0))
        bank1 = gender_set.filter(payment="card", bank="sberbank").aggregate(Sum("cost", default=0))
        bank2 = gender_set.filter(payment="card", bank="tinkoff").aggregate(Sum("cost", default=0))
        payment_set_count = [float(cash["cost__sum"]), float(bank1["cost__sum"]), float(bank2["cost__sum"])]
        # income by day barchart
        query_set = PlaygroundDetail.objects.filter(playground=playground, date__month=current_date.month, date__year=current_date.year)
        query_set_dates = []
        query_set_price = []
        for q in query_set:
            query_set_dates.append(q.date)
            query_set_price.append(q.total_amount)
        cal = calendar.Calendar()
        cal_list = []
        cal_sum = []
        for i in cal.itermonthdates(current_date.year, current_date.month):
            if i.month == current_date.month:
                cal_list.append(i.day)
                try:
                    k = query_set_dates.index(i)
                    cal_sum.append(float(query_set_price[k]))
                except ValueError:
                    cal_sum.append(0)
        return render(request, "customers/charts.html", {
            "cal_list": cal_list,
            "cal_sum": cal_sum,
            "month_total": sum(cal_sum),
            "gender_set_count": gender_set_count,
            "gender_set": gender_set,
            "payment_set_count": payment_set_count,
            "current_date": current_date,
            "page_obj": page_obj,
        })
    else:
        return HttpResponseForbidden("You are not authorized to see this page")


"""NOTIFICATION VIEWS"""
def notification(request):
    if request.user.is_owner:
        playground = Playground.objects.get(pk=request.user.playground.id)
        notifications = User.objects.filter(playground=playground, is_permission_given=False)
        employees = User.objects.filter(playground=playground, is_permission_given=True, is_owner=False)
        if request.htmx:
            counter = notifications.count()
            return HttpResponse(counter if counter > 0 else "")
        elif request.method == "GET":
            return render(request, "customers/notifications.html", {
                "notifications": notifications,
                "employees": employees,
                })
    else:
        return HttpResponseForbidden()

@require_POST
def notification_update(request, id):
    if not User.objects.get(pk=id).is_owner:
        user = User.objects.get(pk=id)
    else:
        HttpResponseBadRequest()
    if "authorize" in request.POST:
        user.is_permission_given = True
        user.save(update_fields=["is_permission_given"])
    elif "unauthorize" in request.POST:
        user = User.objects.get(pk=id)
        user.is_permission_given = False
        user.save(update_fields=["is_permission_given"])
    playground = Playground.objects.get(pk=request.user.playground.id)
    notifications = User.objects.filter(playground=playground, is_permission_given=False)
    employees = User.objects.filter(playground=playground, is_permission_given=True, is_owner=False)
    return render(request, "customers/notifications-notification.html", {
        "notifications": notifications,
        "employees": employees,
        })


"""ENTERING VIEWS"""
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
        is_owner = request.POST.get('is_owner', False)
        if is_owner == "on":
            is_owner = True
        playroom = request.POST["playroom"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "customers/register.html", {
                "message": "Passwords must match."
            })
        # Attempt to create new user
        if is_owner == True:
            try:
                Playground.objects.filter(name__iexact=playroom.lower())[0]
                return render(request, "customers/register.html", {
                    "message": "Playroom name already taken"
                })
            except (ObjectDoesNotExist, IndexError):
                playground = Playground.objects.create(name=playroom)
                playground.save()
                is_permission_given = True
        elif is_owner == False:
            try:
                playground = Playground.objects.filter(name__iexact=playroom.lower())[0]
                is_permission_given = False
            except (ObjectDoesNotExist, IndexError):
                return render(request, "customers/register.html", {
                    "message": "Playroom with this name doesn't exist"
                })
        try:
            user = User.objects.create(
                username=username,
                password=make_password(password),
                playground = playground,
                is_owner = is_owner,
                is_permission_given = is_permission_given
                )
            user.save()
        except IntegrityError:
            return render(request, "customers/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "customers/register.html")