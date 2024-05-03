from django import forms
from decimal import Decimal
from .models import Customer
from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = {
    "female": "Female",
    "male": "Male"
}

CUSTOMER_TYPE_CHOICES = {
    "newcomer": "Newcomer",
    "returning": "Returning"
}

HOURS_CHOICES = (
    (Decimal("0.50"), "30 minutes"),
    (Decimal("1.00"), "1 hour"),
) + tuple((Decimal(f"{i:.2f}"), f"{i} hours") for i in range(2, 11))


PAYMENT_CHOICES = {
    "cash": "Cash",
    "card": "Card"
}

BANK_CHOICES = {
    "": "",
    "sberbank": "Sberbank",
    "tinkoff": "Tinkoff"
}


class CustomerForm(forms.Form):
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES)
    bank = forms.ChoiceField(choices=BANK_CHOICES)


class CustomerModelForm(forms.ModelForm):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    gender = forms.CharField(max_length=10, widget=forms.Select(choices=GENDER_CHOICES))
    customer_type = forms.CharField(max_length=20, widget=forms.Select(choices=CUSTOMER_TYPE_CHOICES))
    hours = forms.ChoiceField(choices=HOURS_CHOICES)
    payment = forms.CharField(max_length=10, widget=forms.Select(choices=PAYMENT_CHOICES))
    bank = forms.CharField(max_length=20, required=False, widget=forms.Select(choices=BANK_CHOICES))

    class Meta:
        model = Customer
        fields = ["name", "gender", "payment", "bank", "customer_type", "hours", "start_time", "end_time"]
        labels = {
            "name": _("Change Name"),
            "gender": _("Change gender"),
            "customer_type": _("Type"),
            "hours": _("Duration"),
        }
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def clean_hours(self):
        hours = self.cleaned_data.get('hours')
        return Decimal(hours)
