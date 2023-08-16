from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from property_form.models import Property
from django.contrib.auth.decorators import login_required
from negotiation.models import Negotiation
from .models import ConfirmationData
from django.conf import settings
import stripe
import json,os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

# from paypal.standard.forms import PayPalPaymentsForm

stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', None)

endpoint_secret = getattr(settings,'ENDPOINT_SECRET', None)



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
def confirmation(request) :


    property_id = request.GET.get('property_id')
    

    try:
        
        confirmation_data = ConfirmationData.objects.get(property_id=property_id)
        email = confirmation_data.email
        name = confirmation_data.name
        payment_status = confirmation_data.payment_status
        amount_total = confirmation_data.amount_total

    except ConfirmationData.DoesNotExist:

        email = name = payment_status = amount_total = None
        



    return render(request,'property_description_trade/confirmation.html',{
        'property_id': property_id,
        'email': email,
        'name': name,
        'payment_status': payment_status,
        'amount_total': amount_total,
    })



    # property = get_object_or_404(Property, id=property_id)

    # negotiation = Negotiation.objects.filter(user = request.user ,property=property, status='accepted').first()

    
    # property_price = negotiation.requested_price if negotiation  else property.price

    # property.status = 'sold'
    # property.save()

    # context = {
    #     'property': property,
    #     'property_price': property_price,
    #     'billing_name': billing_name,

    # }





@login_required(login_url='authentication:signin')
def checkout(request,property_id) :

    property = get_object_or_404(Property, id=property_id)

    

    negotiation = Negotiation.objects.filter(user = request.user ,property=property, status='accepted').first()

    
    property_price = negotiation.requested_price if negotiation  else property.price

    try:

        unit_amount_in_cents = int(property_price * 1000000)
        success_url = f'{settings.NGROK_URL}/confirmation/?property_id={property_id}'
        cancel_url = f'{settings.NGROK_URL}/error/'

        checkout_session = stripe.checkout.Session.create(
            line_items =[
                {
                    'price_data': {
                        'currency': 'inr',
                        'unit_amount': unit_amount_in_cents,  
                        'product_data': {
                            'name': property.address,  
                            'images': [f'{settings.NGROK_URL}{property.pictures.url}'],
                            
                        },
                    },
                    'quantity': 1,
                }
            ],
            mode = 'payment',
            payment_method_types=['card'],
            success_url = success_url,
            cancel_url= cancel_url,

            metadata={
            'property_id': property_id,  
            }
            
            # logo=static('images/logo.png'),
        )
        # return HttpResponse(checkout_session.url)
        return redirect(checkout_session.url, code= 303)
    
    except Exception as e:

        return render(request, 'property_description_trade/error.html' ,{'error_message':str(e)})

      

def error(request):

    return render(request,'property_description_trade/error.html')   



@csrf_exempt
def webhook(request):

    payload = request.body
    event = None
    sig_header = request.headers['STRIPE_SIGNATURE']
    
    
    try:
        
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

    except ValueError as e:
        # Invalid payload
        return JsonResponse({"error": str(e)}, status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return JsonResponse({"error": str(e)}, status=400)

    if event.type == "checkout.session.completed":
        
        value = event.data.object
        

        email = value['customer_details']['email']
        name = value['customer_details']['name']
        payment_status = value['payment_status']
        amount_total = value['amount_total']
        property_id = value['metadata']['property_id']


        property = get_object_or_404(Property, id=property_id)


        confirmation_data = ConfirmationData(
            property=property,
            email=email,
            name=name,
            payment_status=payment_status,
            amount_total=amount_total
        )


        confirmation_data.save()



        return JsonResponse({"status": "success"})    
        
    return JsonResponse({"status": "ignored"})

        

    


        

        



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