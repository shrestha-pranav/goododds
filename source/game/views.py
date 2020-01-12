# payments/views.py
from django.http import Http404

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, render, redirect

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from payments.models import Credits

from django import forms
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

class PlayGameForm(forms.Form):
    amount = forms.CharField(label=_('Amount'))
    odds   = forms.CharField(label=_('Odds'))

class PlayGameView(FormView):
    template_name = 'play.html'
    form_class = PlayGameForm
    success_url = 'game:play'

    def form_valid(self, form):
        return super().form_valid(form)
    #     request = self.request
    #     user = form.save(commit=False)

    #     if settings.DISABLE_USERNAME:
    #         # Set a temporary username
    #         user.username = get_random_string()
    #     else:
    #         user.username = form.cleaned_data['username']

    #     if settings.ENABLE_USER_ACTIVATION:
    #         user.is_active = False

    #     # Create a user record
    #     user.save()

    #     # Change the username to the "user_ID" form
    #     if settings.DISABLE_USERNAME:
    #         user.username = f'user_{user.id}'
    #         user.save()

    #     if settings.ENABLE_USER_ACTIVATION:
    #         code = get_random_string(20)

    #         act = Activation()
    #         act.code = code
    #         act.user = user
    #         act.save()

    #         send_activation_email(request, user.email, code)

    #         messages.success(
    #             request, _('You are signed up. To activate the account, follow the link sent to the mail.'))
    #     else:
    #         raw_password = form.cleaned_data['password1']

    #         user = authenticate(username=user.username, password=raw_password)
    #         login(request, user)

    #         usr_credits = Credits()
    #         usr_credits.user = user
    #         usr_credits.num_credits = 1000
    #         usr_credits.save()

    #         messages.success(request, _('You are successfully signed up!'))

    #     return redirect('index')

class PlayGameView(TemplateView):
    template_name = 'play.html'

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

        
        context['result_page'] = False
        return context

def results(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        odds   = request.POST['odds']

        print(f"Amount = {amount}\nOdds = {odds}")

        return render(request, 'play.html', context={
            'result_page':True,
        })
