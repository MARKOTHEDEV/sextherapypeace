from django import forms
from . import models



class PaymentForm(forms.ModelForm):

    class Meta:
        model = models.PaymentInfo
        fields = ['first_name','last_name','email','payment_approved','mail_sent']

