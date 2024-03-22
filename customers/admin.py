from django.contrib import admin
from customers.models import User, Playground, ChildMock 

class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_owner")

class PlaygroundAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")

class ChildMockAdmin(admin.ModelAdmin):
    list_display = ("id", "playground", "gender", "is_new_customer", "hours", "status")

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Playground, PlaygroundAdmin)
admin.site.register(ChildMock, ChildMockAdmin)