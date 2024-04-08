from typing import Any
from django.views.generic import DetailView
from core.utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import User

class AccountPersonalView(LoginRequiredMixin, DataMixin, DetailView):
    model = User
    context_object_name = 'user' 
    template_name = 'accounts/personal.html'
    login_url = 'users:login'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context()
        context.update(context_mixin)
        return context
    
    def get_object(self, queryset=None):
        return self.request.user 
    