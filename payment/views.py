from django.shortcuts import render
from  django.contrib.auth.decorators import login_required
from basket.basket import Basket
import stripe

@login_required
def BasketView(request):
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.','')
    total = int(total)

    #set the api key for stripe payment. 
    stripe.api_key = 'sk_test_51PwI262KjvVWWPPokhq8qTod2TTL6SvG591IPkumNqkUFcFFu4RYWhy8M5VMrztwmf1DbxHa6Lu14nF3x8ODWr3j00g98Wweec'
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
    return render(request,'payment/home.html', {'client_secret': intent.client_secret}) 
