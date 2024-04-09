from typing import Any
from django.views.generic import FormView, RedirectView
from core.utils import DataMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from users.forms import UserRegistrationForm, LoginUserForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect

@method_decorator(csrf_protect, name='dispatch')
class UsersLoginView(DataMixin, FormView):
    template_name = 'users/login.html'
    form_class = LoginUserForm
    success_url = reverse_lazy('general')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class UsersLogoutView(RedirectView):
    url = reverse_lazy('general')

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(self.url)


@method_decorator(csrf_protect, name='dispatch')
class UsersRegistrationView(DataMixin, FormView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('general')

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context(title='Registration')
        context.update(context_mixin)
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('general')