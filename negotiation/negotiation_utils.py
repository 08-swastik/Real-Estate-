from django.utils import timezone
from .models import Negotiation

def expiry_check(user):
    today = timezone.now()
    accepted_negotiations = Negotiation.objects.filter(
        user=user, status='accepted', property__status='available'
    )

    for negotiation in accepted_negotiations:
        time_difference = today - negotiation.accepted_time

        if time_difference.total_seconds() > 48 * 3600:  
            negotiation.delete()


