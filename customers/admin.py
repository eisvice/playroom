from django.contrib import admin
from customers.models import User, Playground, Customer 

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_owner")

class PlaygroundAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")

class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "playground", "name", "gender", "customer_type", "hours", "status")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Playground, PlaygroundAdmin)
admin.site.register(Customer, CustomerAdmin)