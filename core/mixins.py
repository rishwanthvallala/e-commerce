from django.conf import settings
from djstripe.models import APIKey
from djstripe.enums import APIKeyType
import stripe
import razorpay

class StripeMixin:
    def setup_stripe(self):
        """Configure Stripe with API keys from djstripe"""
        try:
            # Get Stripe keys from djstripe
            publishable_key = APIKey.objects.get(type=APIKeyType.publishable).secret
            secret_key = APIKey.objects.get(type=APIKeyType.secret).secret
            
            # Configure stripe with secret key
            stripe.api_key = secret_key
            
            return publishable_key, secret_key
        except APIKey.DoesNotExist:
            raise Exception("Stripe API keys not configured properly")

    def get_stripe_context(self):
        """Get Stripe publishable key for templates"""
        publishable_key, _ = self.setup_stripe()
        return {"stripe_publishable_key": publishable_key}

class RazorpayMixin:
    def setup_razorpay(self):
        """Configure Razorpay with API keys from settings"""
        key_id = settings.RAZORPAY_KEY_ID
        key_secret = settings.RAZORPAY_KEY_SECRET
        
        # Configure Razorpay with key_id and key_secret
        razorpay_client = razorpay.Client(auth=(key_id, key_secret))
        print(razorpay_client, key_id, key_secret, "Razorpay")
        return razorpay_client

    def get_razorpay_context(self):
        """Get Razorpay key_id for templates"""
        key_id = settings.RAZORPAY_KEY_ID
        return {"razorpay_key_id": key_id}