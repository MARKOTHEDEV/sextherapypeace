from django.shortcuts import render,redirect
from .paymentUtils import InitPayment
import json
from . import forms,models
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from django.contrib import messages
from django.http import HttpResponse



def indexView(request):
    if request.method == 'POST':
        form = forms.PaymentForm()
        if form.is_valid():
            form.save()
            email  =form.cleaned_data.get('email')
            print('worked data create we can process payment')
            init = InitPayment(
            email=email,
            amount=5000,
            meta_data={
                'email':email
            }
        )
            response = init.create_payment_link()
            # order.paystack = response['data']['reference']
            return  redirect(response['data']['authorization_url'])
        else:
            data = dict(request.POST)
            email = data.get('email')
            models.PaymentInfo.objects.filter(email=email).delete()
            messages.add_message(request, messages.error, 'Something went wrong please check your internet and try again')
        # return render(request,'index.html',{'word':'hello world'})

    return render(request,'index.html',{'word':'hello world'})




@csrf_exempt
def payment_webhook(request,pk=None):
    "this receives Payload from paystack"
    # data = json.loads(request.body)
    data = json.loads(request.body)
    meta_data =data['data']['metadata']
    if data.get('event') == 'charge.success':
        email = meta_data['email']
        me =models.PaymentInfo.objects.filter(email=email).first()
        me.payment_approved=True
        me.save()

    return HttpResponse(200)