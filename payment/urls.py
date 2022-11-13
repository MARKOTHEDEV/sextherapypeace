from django.urls import path
from . import views

urlpatterns =[

    path('',views.indexView,name='indexView'),
    path('webhook',views.payment_webhook)

]