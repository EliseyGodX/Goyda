from typing import Any
from django.views.generic import FormView, RedirectView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.utils import DataMixin
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from users.forms import UserRegistrationForm, LoginUserForm, UsersPasswordChangeForm
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from users.models import User
from django.utils.translation import gettext_lazy as _


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
    
    
class UsersListView(DataMixin, ListView):
    model = User
    context_object_name = 'users'
    template_name = 'users/users.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context()
        context.update(context_mixin)
        return context
    
    
class UsersPasswordChangeView(LoginRequiredMixin, DataMixin, PasswordChangeView):
    form_class = UsersPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('general')
    login_url = 'users:login'

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context_mixin = self.get_default_context()
        context.update(context_mixin)
        return context
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"]) 
        if commit:
            user.save()