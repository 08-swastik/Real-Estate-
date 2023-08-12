from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from property_form.models import Property
from django.contrib.auth.decorators import login_required
from negotiation.models import Negotiation
from django.conf import settings
import stripe

# from paypal.standard.forms import PayPalPaymentsForm

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', None)



# Create your views here.
def property_detail(request,property_id):

    property_obj = get_object_or_404(Property, id=property_id)
    user = request.user

    
    highest_bidded_price = None
    highest_bid = Negotiation.objects.filter(property_id=property_id).order_by('-requested_price').first()

    if highest_bid:
        highest_bidded_price = highest_bid.requested_price

    accepted_negotiation = Negotiation.objects.filter(user = request.user,property=property_obj, status='accepted').first()
    actual_price = property_obj.price
    new_price = None
    
    if accepted_negotiation:
        new_price = accepted_negotiation.requested_price

        
    if hasattr(user, 'seller'):
        seller_or_client = user.seller
    elif hasattr(user, 'client'):
        seller_or_client = user.client
    
    is_sold = property_obj.status == 'sold'

    if request.method == 'POST':
        return redirect('property_description_trade:checkout', property_id=property_id)
    

    context = {

        'highest_bidded_price': highest_bidded_price,
        'property_image': property_obj.pictures.url,
        'property_address': property_obj.address,
        'property_price': actual_price,
        'special_price' : new_price,
        'bhk': property_obj.bhk,
        'city': property_obj.city,
        'property_sqft': property_obj.square_feet,
        'property_overview': property_obj.overview,
        'isAuthenticated': request.user.is_authenticated,
        'seller_or_client' : seller_or_client,
        'property_id': property_id,
        'property_obj' : property_obj,
        'is_sold': is_sold,

    }

    return render(request,'property_description_trade/property_description.html', context)

    

# @login_required(login_url='authentication:signin')
def confirmation(request,property_id,billing_name) :

    property = get_object_or_404(Property, id=property_id)

    negotiation = Negotiation.objects.filter(user = request.user ,property=property, status='accepted').first()

    
    property_price = negotiation.requested_price if negotiation  else property.price

    property.status = 'sold'
    property.save()

    context = {
        'property': property,
        'property_price': property_price,
        'billing_name': billing_name,

    }


    return render(request,'property_description_trade/confirmation.html',context)








@login_required(login_url='authentication:signin')
def checkout(request,property_id) :

    property = get_object_or_404(Property, id=property_id)

    

    negotiation = Negotiation.objects.filter(user = request.user ,property=property, status='accepted').first()

    
    property_price = negotiation.requested_price if negotiation  else property.price

    try:

        unit_amount_in_cents = int(property_price * 10000000)

        checkout_session = stripe.checkout.Session.create(
            line_items =[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': unit_amount_in_cents,  
                        'product_data': {
                            'name': property.address,  
                            # 'images': [property.pictures.url],
                            
                        },
                    },
                    'quantity': 1,
                }
            ],
            mode = 'payment',
            payment_method_types=['card'],
            success_url = 'http://localhost:8000/confirmation/',
            # cancel_url='http://localhost:8000/cancel/',
            
            # logo=static('images/logo.png'),
        )
        return HttpResponse(checkout_session.url)
        # return redirect(checkout_session.url, code= 303)
    
    except Exception as e:

        return render(request, 'property_description_trade/error.html' ,{'error_message':str(e)})

    # return redirect('property_description_trade:property_detail', property_id=property_id)   


def success(request):
    return HttpResponse("payment successful")


# def checkout(request, property_id):
#     property_obj = get_object_or_404(Property, id=property_id)
#     actual_price = property_obj.price

#     host = request.get_host()


#     paypal_dict = {
#         'business': settings.PAYPAL_RECEIVER_EMAIL,
#         'amount': actual_price,
#         'item_name': property_obj.address,
#         'invoice': f'property_{property_id}',  # Set a unique invoice ID for each payment
#         'currency_code': 'INR',
#         'return_url': 'http://{}{}'.format(host,reverse('paypal-ipn')),
#                                              # Replace with your IPN URL
#         # 'return_url': request.build_absolute_uri('/payment/success/'),  # Replace with your success URL
#         # 'cancel_return': request.build_absolute_uri('/payment/cancel/'),  # Replace with your cancel URL
#          'brand_name': 'Your Brand Name',
#         'enable_smart_payment_buttons': True,
#         'landing_page': 'billing',
#     }

#     form = PayPalPaymentsForm(initial=paypal_dict)

#     context = {
#         'property_image': property_obj.pictures.url,
#         'property_address': property_obj.address,
#         'property_price': actual_price,
#         'property_id': property_id,
#         'form': form,
#     }

#     return render(request, 'property_description_trade/checkout.html', context)