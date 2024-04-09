from django.urls import path
from users.accounts.views import AccountsPersonalView, AccountsEditView
app_name = 'accounts'

urlpatterns = [
    path('personal/', AccountsPersonalView.as_view(), name='personal'),
    path('edit/', AccountsEditView.as_view(), name='edit'),
]