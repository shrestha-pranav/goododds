# payments/views.py

from payments.models import Credits

from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import FormView, TemplateView

from django.db import transaction

from .forms import PlayGameForm

import random

class PlayGameView(FormView):
    template_name = 'play.html'
    form_class = PlayGameForm
    success_url = reverse_lazy('game:play')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if settings.ENABLE_USER_ACTIVATION and not self.request.user.is_active:
            context['activated'] = False
            context['num_credits'] = 0
        else:
            context['activated'] = True
        
            try:
                usr_credits = get_object_or_404(Credits, user=self.request.user)
                context['num_credits'] = usr_credits.num_credits
            except Exception as e:
                print("User credits not retreived in profile", e)
                context['num_credits'] = 0

        
        print("Result page : ", context.get('result_page', None))
        context['result_page'] = False
        return context

    def form_valid(self, form, **kwargs):

        bet_amount = int(form.data['amount'])
        raw_odds   = form.data['odds']
        bet_odds   = [int(i) for i in raw_odds.split(":")]

        locked_usr_credits = Credits.objects.select_for_update().filter(user=self.request.user)
        with transaction.atomic():
            usr_credits = locked_usr_credits.first()
            
            if bet_amount > usr_credits.num_credits:
                return HttpResponseRedirect(self.get_success_url())

            if random.randint(0, bet_odds[1]-1) < bet_odds[0]:
                usr_credits.num_credits += int(bet_amount * (bet_odds[1] / bet_odds[0]-1))
            else:
                usr_credits.num_credits -= bet_amount
            
            usr_credits.save()

        return HttpResponseRedirect(self.get_success_url())

# class PlayGameView(TemplateView):
#     template_name = 'play.html'

#     def dispatch(self, request, *args, **kwargs):
#         # Redirect to the index page if the user already authenticated
#         if not request.user.is_authenticated:
#             return redirect(settings.LOGIN_URL)

#         # If user has not been activated
#         if settings.ENABLE_USER_ACTIVATION:
#             if request.user.is_active == False:
#                 return redirect('accounts:resend_activation_code')
        
#         try:
#             self.usr_credits = get_object_or_404(Credits, user=self.request.user)
#         except Exception as e:
#             return redirect('accounts:resend_activation_code')

#         return super().dispatch(request, *args, **kwargs)


# def results(request):
#     if request.method == 'POST':
#         amount = int(request.POST['amount'])
#         odds   = request.POST['odds']

#         print(f"Amount = {amount}\nOdds = {odds}")

#         return render(request, 'play.html', context={
#             'result_page':True,
#         })
