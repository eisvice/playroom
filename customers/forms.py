from django import forms
from .models import Customer

PAYMENT_CHOICES = {
    "cash": "Cash",
    "card": "Card"
}

BANK_CHOICES = {
    "sberbank": "Sberbank",
    "tinkoff": "Tinkoff"
}


class CustomerForm(forms.Form):
    payment = forms.ChoiceField(choices=PAYMENT_CHOICES)
    bank = forms.ChoiceField(choices=BANK_CHOICES)


class CustomerModelForm(forms.ModelForm):
    payment = forms.CharField(max_length=10, widget=forms.Select(choices=PAYMENT_CHOICES))
    bank = forms.CharField(max_length=20, required=False, widget=forms.Select(choices=BANK_CHOICES))

    class Meta:
        model = Customer
        fields = ["id", "gender", "customer_type", "name", "hours", "payment", "bank", "start_time", "end_time"]
