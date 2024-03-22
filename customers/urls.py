from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete-customers/", views.delete_customers, name="delete-customers"),
    path("customers/delete/<int:id>", views.delete_customer, name="delete-customer"),
    path("customers/add-hour/<int:id>", views.add_hour, name="add-hour"),
    path("customers/<int:id>", views.find_customer, name="customers"),
    path("custoemers/finish/<int:id>", views.finish, name="finish"),
] 