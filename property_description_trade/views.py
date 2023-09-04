from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from property_form.models import Property
from django.contrib.auth.decorators import login_required
from negotiation.models import Negotiation
from .models import ConfirmationData
from django.conf import settings
from django.template.loader import get_template
import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from django.core.mail import EmailMessage
from negotiation.negotiation_utils import expiry_check
from weasyprint import HTML


stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', None)

endpoint_secret = getattr(settings,'ENDPOINT_SECRET', None)



def property_detail(request,property_id):

    property_obj = get_object_or_404(Property, id=property_id)
    user = request.user
    

    if hasattr(request, 'user') and request.user.is_authenticated:

        expiry_check(request.user)
    
    
    highest_bid = Negotiation.objects.filter(property_id=property_id).order_by('-requested_price').first()

    if highest_bid:
        highest_bidded_price = highest_bid.requested_price
        print(highest_bidded_price)
    else:
        highest_bidded_price = None

    print(highest_bidded_price)

    

    accepted_negotiation = Negotiation.objects.filter(user = request.user,property=property_obj, status='accepted').first()
    actual_price = property_obj.price
    new_price = None
    
    if accepted_negotiation:
        new_price = accepted_negotiation.requested_price

        
    if hasattr(user, 'seller'):
        seller_or_client = user.seller.username
        first_name = user.seller.first_name
        last_name = user.seller.last_name
        email = user.seller.email
        phone = user.seller.phone_number

    elif hasattr(user, 'client'):
        seller_or_client = user.client.username
        first_name = user.client.first_name
        last_name = user.client.last_name
        email = user.client.email
        phone = user.client.phone_number
    

    is_sold = property_obj.status == 'sold'

    if request.method == 'POST':
        return redirect('property_description_trade:checkout', property_id=property_id)
    

    context = {
        'first_name' : first_name,
        'last_name' : last_name,
        'email' : email,
        'phone_number' : phone,
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

    


def confirmation(request) :

    property_id = request.GET.get('property_id')

    confirmation_data = ConfirmationData.objects.get(property_id=property_id)

    print(confirmation_data) 
    email = confirmation_data.email
    name = confirmation_data.name
    amount_total = confirmation_data.amount_total/100


    property_obj = get_object_or_404(Property, id=property_id)
    seller_email = property_obj.seller.email
    address = property_obj.address

    pdf = render_to_pdf("property_description_trade/invoice_template.html", {
            'name': name,
            'email': email,
            'amount': amount_total,
            'address' : address

        })
    
    send_confirmation_email(seller_email, pdf.content)
    send_confirmation_email(email, pdf.content)

    property_obj.status = 'sold'
    property_obj.save()
    
    print(property_id)
    return render(request,'property_description_trade/confirmation.html',{
        'property_id': property_id,
    })
    
def download_pdf(request,property_id):

    print(property_id)
    confirmation_data = ConfirmationData.objects.get(property_id=property_id)



     
    email = confirmation_data.email
    name = confirmation_data.name
    amount_total = confirmation_data.amount_total/100
    address = confirmation_data.property.address
    context = {
        'email': email,
        'name' : name,
        'amount' : amount_total,
        'address' : address
    }

    print(email,name,amount_total,address)
    pdf = render_to_pdf("property_description_trade/invoice_template.html", context)
    if pdf:
        response = HttpResponse(pdf, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="invoice.pdf"'
        return response
    return HttpResponse("Error generating PDF")

   
def send_confirmation_email(email, pdf_content):
    
    subject = 'Confirmation Email'
    message = 'Thank you for your purchase. Your order has been confirmed.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    email_message = EmailMessage(
        subject, message, from_email, recipient_list,
        
    )
    email_message.attach('confirmation.pdf', pdf_content, 'application/pdf')

    # Send the email
    email_message.send()

    


def render_to_pdf(template_path, context_dict):
    template = get_template(template_path)
    html = template.render(context_dict)
    pdf_file = HTML(string=html).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="your_pdf_file.pdf"'
    return response


@login_required(login_url='authentication:signin')
def checkout(request,property_id) :

    property = get_object_or_404(Property, id=property_id)

    negotiation = Negotiation.objects.filter(user = request.user ,property=property, status='accepted').first()
    

    property_price = negotiation.requested_price if negotiation  else property.price

    try:
        print(property_price)
        unit_amount_in_cents = int(property_price * 10000000)
        print(unit_amount_in_cents)
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
            
           
        )
        
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