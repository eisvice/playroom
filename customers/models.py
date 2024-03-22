from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    is_owner = models.BooleanField()


class Playground(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="UFO")


class ChildMock(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACT", _("Active")
        AWAIT = "AWT", _("Await")
        DELETED = "DEL", _("Deleted")
        FINISHED = "FIN", _("Finished")
    
    class Gender(models.TextChoices):
        MALE = "M", _("Male")
        FEMALE = "F", _("Female")

    playground = models.ForeignKey(Playground, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=1,
        choices=Gender,
        default=Gender.MALE
        )
    is_new_customer = models.BooleanField()
    hours = models.DecimalField(max_digits=3, decimal_places=1)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True)
    status = models.CharField(
        max_length=3,
        choices=Status,
        default=Status.ACTIVE
        )
     