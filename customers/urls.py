from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("customers", views.add_customer, name="customers"),
    path("customers/<int:id>", views.update_info, name="customers"),
    path("customers/delete/<int:id>", views.delete_customer, name="delete-customer"),
    path("customers/add-hour/<int:id>", views.add_hour, name="add-hour"),
    path("custoemers/finish/<int:id>", views.finish, name="finish"),
    path("history", views.history_view, name="history"),
    path("history/<int:id>", views.history_detail, name="history-detail"),
    path("history/update/<int:id>", views.history_update_details, name="history-update"),
    path("charts", views.charts_view, name="charts"),
    path("notifications", views.notification, name="notifications"),
    path("notifications/<int:id>", views.notification_update, name="notifications-update"),
] 