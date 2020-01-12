from django.views.generic import TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings

from payments.models import Credits

class IndexPageView(TemplateView):
    template_name = 'main/index.html'

class ChangeLanguageView(TemplateView):
    template_name = 'main/change_language.html'

class ProfileView(TemplateView):
    template_name = 'main/profile.html'

    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_URL)
        
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

        
        return context
