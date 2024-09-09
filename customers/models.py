from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import timedelta, date
from django.utils import timezone


# Create your models here.
class Playground(models.Model):
    name = models.CharField(max_length=100)


class User(AbstractUser):
    is_owner = models.BooleanField(blank=True, null=True)
    is_permission_given = models.BooleanField(blank=True, null=True)
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE)


class PlaygroundDetail(models.Model):
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    rate = models.DecimalField(max_digits=8, decimal_places=2, default=500.0)
    total_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)


class Customer(models.Model):
    gender = models.CharField(max_length=10)
    customer_type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    hours = models.DecimalField(max_digits=4, decimal_places=2, default=1.0)
    status = models.CharField(max_length=20, default="active")
    payment = models.CharField(max_length=10, default="cash")
    bank = models.CharField(max_length=20, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    playground = models.ForeignKey(Playground, on_delete=models.CASCADE)
    playground_detail = models.ForeignKey(PlaygroundDetail, on_delete=models.CASCADE)
    
    def set_start_time(self):
        current_tz = timezone.get_current_timezone()
        self.start_time = timezone.now().astimezone(current_tz)
        print("Start time is", self.start_time)

    def set_end_time(self):
        current_tz = timezone.get_current_timezone()
        self.end_time = timezone.now().astimezone(current_tz) + timedelta(hours=self.hours)
        print("Is timezone aware (models):", timezone.is_aware(self.end_time))
        print("End time is", self.end_time)

    def set_name(self):
        self.name = self.customer_type.capitalize()
    
    def save(self, *args, **kwargs):
        if not self.start_time:
            self.set_start_time()
        if not self.end_time:
            self.set_end_time()
        if not self.name:
            self.set_name()
        super(Customer, self).save(*args, **kwargs)
        
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "payment": self.payment,
            "bank": self.bank,
            "customer_type": self.customer_type,
            "hours": self.hours,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "status": self.status,
        }
    
    def __str__(self):
        return f"id: {self.id}, name: {self.name}, gender: {self.gender}, payment: {self.payment}, bank: {self.bank}, customer type: {self.customer_type}, hours: {self.hours}, start time: {self.start_time}, end time: {self.end_time}, status: {self.status}"