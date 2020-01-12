# payments/views.py
import stripe

from django.http import Http404

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import Credits

stripe.api_key = settings.STRIPE_SECRET_KEY

class AddCreditView(TemplateView):
    template_name = 'add_credit.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)

        # If user has not been activated
        if settings.ENABLE_USER_ACTIVATION:
            if request.user.is_active == False:
                return redirect('accounts:resend_activation_code')
        
        try:
            self.usr_credits = get_object_or_404(Credits, user=self.request.user)
        except Exception as e:
            return redirect('accounts:resend_activation_code')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key']   = settings.STRIPE_PUBLISHABLE_KEY
        context['user']  = self.request.user.username
        context['email'] = self.request.user.email
        context['amount_list'] = [500, 1000, 2000, 10000]
        return context

def charge(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])

        try:
            usr_credits = get_object_or_404(Credits, user=request.user)
        except Exception as e:
            print("User credits not retreived", e)
            return redirect('accounts:resend_activation_code')

        charge = stripe.Charge.create(
            amount=amount,
            currency='usd',
            description=f"Adding {amount} good odds credits!",
            source=request.POST['stripeToken']
        )

        while charge.status == 'pending':
            if charge.status == 'succeeded':
                usr_credits.num_credits = usr_credits.num_credits + amount
                usr_credits.save()


        return render(request, 'charge_credit.html', context={
            'status': charge.status,
            'amount': amount
        })
