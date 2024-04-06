from typing import Any
from django.views.generic import CreateView, FormView
from core.utils import DataMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from users.forms import UserRegistrationForm

class Login(DataMixin, CreateView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('general')
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Login')
        context.update(context_mixin)
        return context


@method_decorator(csrf_protect, name='dispatch')
class UserRegistrationView(DataMixin, FormView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('general')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Registration')
        context.update(context_mixin)
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    