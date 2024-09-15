import json 
from django.http import HttpResponse
from django.shortcuts import render
from  django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from basket.basket import Basket
from orders.views import payment_confirmation
from django.conf import settings
import os
import stripe

def order_placed(request): 
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')

@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.','')
    total = int(total)

    #set the api key for stripe payment. 
    stripe.api_key = settings.SECRET_KEY
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        payment_method="pm_card_threeDSecure2Required",
        # automatic_payment_methods={
        #     "enabled": True,
        #     },
        # return_url="http://127.0.0.1:8000/payment/orderplaced/",
        # confirm=True,
        metadata={'userid':request.user.id}
    )
    return render(request,'payment/home.html', {'client_secret': intent.client_secret,'STRIPE_PUBLISHABLE_KEY' : os.environ.get('STRIPE_PUBLISHABLE_KEY')}) 

@csrf_exempt
def stripe_webhook(request): 
    payload = request.body
    event = None 

    try: 
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e: 
        print(e)
        return HttpResponse(status=400)

    if event.type == 'payment_intent.succeeded': 
        payment_confirmation(event.data.object.client_secret)
    else: 
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)
        
