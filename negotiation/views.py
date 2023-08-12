from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from property_form.models import Property
from .models import Negotiation


def negotiation_form(request, property_id):

    if request.method == 'POST':

        user = request.user
        requested_price = request.POST.get('requested_price')

        if hasattr(user, 'seller'):
            seller_or_client = user.seller
        elif hasattr(user, 'client'):
            seller_or_client = user.client

        email = seller_or_client.email
        first_name = seller_or_client.first_name
        last_name = seller_or_client.last_name
        phone_number = seller_or_client.phone_number

        property_obj = get_object_or_404(Property, id=property_id)

        negotiation = Negotiation.objects.create(
            user=user,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            requested_price=requested_price,
            property=property_obj,
        )

        negotiation.save()
        return redirect('home')


def available_negotiations(request, property_id):
    if request.method == 'POST':
        negotiations = Negotiation.objects.filter(
            property_id=property_id).order_by('-requested_price')
        original_price = None

        for negotiation in negotiations:
            status = request.POST.get(str(negotiation.id))
            if status in ['pending', 'rejected', 'accepted']:
                negotiation.status = status

                if status == 'accepted':
                    negotiation.accepted_time = timezone.now()

                negotiation.save()

        return redirect('home')

    else:
        if property_id:
            negotiations = Negotiation.objects.filter(
                property_id=property_id).order_by('-requested_price')
            property_obj = Property.objects.get(id=property_id)
            original_price = property_obj.price

    return render(request, 'negotiations/available_negotiations.html', {
        'negotiations': negotiations,
        'original_price': original_price,
        'property_obj': property_obj,
    })


def my_offers(request):
    today = timezone.now().date()
    accepted_negotiations = Negotiation.objects.filter(
        user=request.user, status='accepted', accepted_time__isnull=False,
        accepted_time__date__gte=today - timezone.timedelta(days=2)
    )
    
    negotiated_offers = []
    
    for negotiation in accepted_negotiations:
        days_left = 2 - (today - negotiation.accepted_time.date()).days
        negotiated_offers.append({'negotiation': negotiation, 'days_left': days_left})

        if days_left <= 0:
            negotiation.delete()
    
    return render(request, 'negotiations/my_offers.html', {'negotiated_offers': negotiated_offers})
def my_offers(request):
    today = timezone.now().date()
    accepted_negotiations = Negotiation.objects.filter(
        user=request.user, status='accepted', accepted_time__isnull=False,
        accepted_time__date__gte=today - timezone.timedelta(days=2)
    )
    
    negotiated_offers = []
    
    for negotiation in accepted_negotiations:
        days_left = 2 - (today - negotiation.accepted_time.date()).days
        negotiated_offers.append({'negotiation': negotiation, 'days_left': days_left})

        if days_left <= 0:
            negotiation.delete()
    
    return render(request, 'negotiations/my_offers.html', {'negotiated_offers': negotiated_offers})

def my_offers(request):
    today = timezone.now().date()
    accepted_negotiations = Negotiation.objects.filter(
        user=request.user, status='accepted'
    )

    negotiated_offers = []

    for negotiation in accepted_negotiations:
        if negotiation.accepted_time and negotiation.accepted_time.date() >= today - timezone.timedelta(days=2):
            days_left = 2 - (today - negotiation.accepted_time.date()).days
            negotiated_offers.append({'negotiation': negotiation, 'days_left': days_left})
        else:
            negotiation.delete()

    return render(request, 'negotiations/my_offers.html', {'negotiated_offers': negotiated_offers})




def my_negotiations(request):
    negotiations = Negotiation.objects.filter(user=request.user)
    return render(request, 'negotiations/my_negotiations.html', {'negotiations': negotiations})


def delete_offers(request, negotiation_id):
    negotiation = get_object_or_404(Negotiation, id=negotiation_id)
    if request.method == 'POST':

        negotiation.delete()

        return redirect('negotiation:my_offers')
