import json,requests
from django.conf import settings
import os
from decimal import Decimal
from django.core.exceptions import ValidationError


def convert_naira_to_kobo(naira):
    naira = float(naira)*100
    kobo = int(naira)
    return kobo




def get_amount_by_percent(percent,amount): 
    "this function gets the amount of a percent on a money"
    return Decimal(percent/100) *(amount)

class InitPayment:
    'this class handles the initializing of payment it bassically proccess payment and sends back payment link so user can use'


    def __init__(self,email,amount,meta_data=dict()) -> None:
        self.email=email
        self.amount=amount
        self.meta_data= meta_data
        self.url = 'https://api.paystack.co/transaction/initialize/'


    def create_payment_link(self):
        headers = {
            'Authorization': f'Bearer '+os.environ['PAYSTACK_SECRET'],
            'Content-Type' : 'application/json',
            'Accept': 'application/json',}
        body = {
            "email":self.email,
            "amount": convert_naira_to_kobo(self.amount),
            "metadata":self.meta_data,}

        try:
            resp = requests.post(self.url,headers=headers,data=json.dumps(body))
        except requests.ConnectionError:
            return  ValidationError(message="Network Error please try again in few minutes",code=503)
               
        if resp.status_code ==200:
            data = resp.json()
            return data

        raise ValidationError(message='Some Error Occured Please Try Again',code=503)
        