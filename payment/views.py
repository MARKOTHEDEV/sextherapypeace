from django.shortcuts import render,redirect
from .paymentUtils import InitPayment
import json
from . import forms,models
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.http import HttpResponse
from django.contrib import messages

from django.core.mail import send_mail

def indexView(request,id=None):
    if request.method == 'POST':
        form = forms.PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            email  =form.cleaned_data.get('email')
            form_number  =form.cleaned_data.get('form_number')
            print('worked data create we can process payment')
            if form_number == '1':
                init = InitPayment(
                email=email,
                amount=5000,
                meta_data={
                    'email':email,
                    'form_number':form_number
                }
            )
            else:
                init = InitPayment(
                email=email,
                amount=3000,
                meta_data={
                    'email':email,
                    'form_number':form_number})              
            response = init.create_payment_link()
            return  redirect(response['data']['authorization_url'])
        else:
            data = dict(request.POST)
            email = data.get('email')
            models.PaymentInfo.objects.filter(email=email).delete()


    return render(request,'index.html',{'word':'hello world'})




@csrf_exempt
def payment_webhook(request,pk=None):
    "this receives Payload from paystack"
    # data = json.loads(request.body)
    data = json.loads(request.body)
    meta_data =data['data']['metadata']
    if data.get('event') == 'charge.success':
        courses = {
            '1':'https://drive.google.com/file/d/11ZBmpsDEgIzyiajaYh1-TCSraeqUsA81/view?usp=share_link',
            '2':'https://drive.google.com/file/d/1GPcfIq-_saMQ_WaeZgw9L34_5rzQa0E9/view?usp=share_link',
            '3':'https://drive.google.com/file/d/1c4skbpvm60L1TVjijErg3M7y-PS7hthe/view?usp=share_link',
        }
        email = meta_data['email']
        send_mail(
        'Link to peace course!',
        f"""
        Thanks For the Purchase,

        please use this link to access the course: {courses[meta_data['form_number']]}
        """,

        'support@peaceelechi.com',
        [email],

        fail_silently=False,
        )
        me =models.PaymentInfo.objects.filter(email=email).first()
        me.payment_approved=True
        me.mail_sent=True
        me.save()


#   messages.success(request,'Hey We Have Received Your Informations and We Will Get Back To You!!')

    return HttpResponse(200)