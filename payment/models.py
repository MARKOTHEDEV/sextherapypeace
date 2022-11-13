from django.db import models

# Create your models here.



class PaymentInfo(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()
    payment_approved = models.BooleanField(default=False)
    mail_sent =  models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"